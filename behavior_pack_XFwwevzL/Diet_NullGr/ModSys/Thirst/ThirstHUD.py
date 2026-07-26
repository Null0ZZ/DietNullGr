# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.ModSys.Thirst.config as config

ScreenNode = clientApi.GetScreenNodeCls()
ViewBinder = clientApi.GetViewBinderCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()


class ThirstHUD(ScreenNode):
    def __init__(self, namespace, uiKey, param):
        ScreenNode.__init__(self, namespace, uiKey, param)
        self.displayValue = config.displayMaxValue
        self.flashOldValue = config.displayMaxValue
        self.flashDisplayValue = config.displayMaxValue
        self.visible = False
        self.style = config.defaultStyle
        self.critical = False
        self.flashVisible = False
        self.flashTimer = None
        self.flashSteps = 0
        self.created = False
        self.hasData = False

    def Create(self):
        self.created = True
        self.UpdateScreen(True)

    def Creat(self):
        self.Create()

    # 每个图标承载两点口渴值，索引从左到右，但阈值反向计算以复刻原版饥饿条从左侧开始消失。
    def GetSlotState(self, value, index):
        fullValue = (10 - index) * 2
        if value >= fullValue:
            return 2
        if value == fullValue - 1:
            return 1
        return 0

    # 服务端数据先刷新最终状态，再启动短闪烁链；新变化会取消旧计时，防止两轮动画交叉污染显示。
    def UpdateThirstData(self, data):
        newDisplayValue = data['displayValue']
        shouldFlash = self.created and self.hasData and newDisplayValue != self.displayValue
        if shouldFlash:
            self.CancelFlashTimer()
            self.flashOldValue = self.displayValue
            self.flashDisplayValue = max(self.displayValue, newDisplayValue)
            self.flashVisible = True
            self.flashSteps = config.flashToggleCount
        self.displayValue = newDisplayValue
        self.visible = data['visible']
        self.style = data['style']
        self.critical = data['critical']
        self.hasData = True
        self.UpdateScreen(True)
        if shouldFlash:
            compGame = compFactory.CreateGame(levelId)
            self.flashTimer = compGame.AddTimer(config.flashInterval, self.ToggleFlash)

    # 一轮闪烁由多个单次计时器串联，结束后强制隐藏覆盖层，保证静止状态只保留当前水滴。
    def ToggleFlash(self):
        self.flashTimer = None
        self.flashVisible = not self.flashVisible
        self.flashSteps -= 1
        if self.flashSteps <= 0:
            self.flashVisible = False
        self.UpdateScreen(True)
        if self.flashSteps > 0:
            compGame = compFactory.CreateGame(levelId)
            self.flashTimer = compGame.AddTimer(config.flashInterval, self.ToggleFlash)

    # 取消旧计时是“数据变化→闪烁→清理”事务的结束步骤，热重载和连续变化都复用这一入口。
    def CancelFlashTimer(self):
        if not self.flashTimer:
            return
        compGame = compFactory.CreateGame(levelId)
        compGame.CancelTimer(self.flashTimer)
        self.flashTimer = None

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#thirst_hud.visible")
    def bindVisible(self):
        return self.visible

    # 每个格子只挂载一种外观容器，状态绑定继续共用，切换样式时不需要重建 HUD。
    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "thirst_slots", "#thirst_hud.water_drop_style_visible")
    def bindWaterDropStyleVisible(self, index):
        return self.style == config.styleWaterDrop

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "thirst_slots", "#thirst_hud.square_style_visible")
    def bindSquareStyleVisible(self, index):
        return self.style == config.styleSquare

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "thirst_slots", "#thirst_hud.full_visible")
    def bindFullVisible(self, index):
        return self.GetSlotState(self.displayValue, index) == 2

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "thirst_slots", "#thirst_hud.half_visible")
    def bindHalfVisible(self, index):
        return self.GetSlotState(self.displayValue, index) == 1

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "thirst_slots", "#thirst_hud.flash_full_visible")
    def bindFlashFullVisible(self, index):
        oldState = self.GetSlotState(self.flashOldValue, index)
        currentState = self.GetSlotState(self.displayValue, index)
        flashState = self.GetSlotState(self.flashDisplayValue, index)
        return self.flashVisible and oldState != currentState and flashState == 2

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "thirst_slots", "#thirst_hud.flash_half_visible")
    def bindFlashHalfVisible(self, index):
        oldState = self.GetSlotState(self.flashOldValue, index)
        currentState = self.GetSlotState(self.displayValue, index)
        flashState = self.GetSlotState(self.flashDisplayValue, index)
        return self.flashVisible and oldState != currentState and flashState == 1

    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "thirst_slots", "#thirst_hud.critical_visible")
    def bindCriticalVisible(self, index):
        return self.critical and self.GetSlotState(self.displayValue, index) > 0

    def Destroy(self):
        self.created = False
        self.CancelFlashTimer()
