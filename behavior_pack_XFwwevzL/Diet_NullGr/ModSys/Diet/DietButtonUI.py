# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as config

ScreenNode = clientApi.GetScreenNodeCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()


class DietButtonUI(ScreenNode):
    def __init__(self, namespace, uiKey, param):
        ScreenNode.__init__(self, namespace, uiKey, param)
        self.buttonControl = None
        self.touchSeq = 0
        self.touching = False
        self.longPressTimer = None
        self.longPressed = False
        self.touchMoved = False
        self.startTouchPos = (0.0, 0.0)
        self.startButtonPos = (0.0, 0.0)
        self.startButtonGlobalPos = (0.0, 0.0)
        self.lastButtonGlobalPos = ()
        self.originCollisionBox = ()
        self.collisionBox = ()

    def Create(self):
        self.buttonControl = self.GetBaseUIControl('/root/open_button').asButton()
        self.buttonControl.AddTouchEventParams({'isSwallow': True})
        self.buttonControl.SetButtonTouchDownCallback(self.ButtonTouchDown)
        self.buttonControl.SetButtonTouchMoveCallback(self.ButtonTouchMove)
        self.buttonControl.SetButtonTouchUpCallback(self.ButtonTouchUp)
        self.buttonControl.SetButtonTouchCancelCallback(self.ButtonTouchCancel)
        iconControl = self.GetBaseUIControl('/root/open_button/icon').asItemRenderer()
        iconControl.SetUiItem(config.groups['fruits']['icon'], 0)
        self.RestoreButtonPos()
        self.CorrectCurrentButtonPos()

    def Creat(self):
        self.Create()

    # 按下时启动长按计时，只有持续按住到计时完成后，后续移动才会改变按钮位置。
    def ButtonTouchDown(self, args):
        touchPosX = args['TouchPosX']
        touchPosY = args['TouchPosY']
        self.CancelLongPressTimer()
        self.touchSeq += 1
        self.touching = True
        self.longPressed = False
        self.touchMoved = False
        self.startTouchPos = (touchPosX, touchPosY)
        self.startButtonPos = self.buttonControl.GetPosition()
        self.startButtonGlobalPos = self.buttonControl.GetGlobalPosition()
        self.lastButtonGlobalPos = self.startButtonGlobalPos
        self.InitCollisionBox()
        compGame = compFactory.CreateGame(levelId)
        self.longPressTimer = compGame.AddTimer(config.buttonLongPressSeconds, self.LongPressReady, self.touchSeq)

    # 拖动前先确认已经长按成功；未长按时移动超过阈值会取消点击，避免滑动误打开主界面。
    def ButtonTouchMove(self, args):
        touchPosX = args['TouchPosX']
        touchPosY = args['TouchPosY']
        if not self.touching:
            return
        touchPos = (touchPosX, touchPosY)
        if self.TouchMovedTooFar(touchPos):
            self.touchMoved = True
            if not self.longPressed:
                self.CancelLongPressTimer()
        if not self.longPressed:
            self.buttonControl.SetPosition(self.startButtonPos)
            return
        dx = touchPos[0] - self.startTouchPos[0]
        dy = touchPos[1] - self.startTouchPos[1]
        pos = (self.startButtonPos[0] + dx, self.startButtonPos[1] + dy)
        self.buttonControl.SetPosition(self.LimitButtonPos(pos))

    # 弹起时根据交互链路决定是打开主界面、保存拖动位置，还是还原误触移动。
    def ButtonTouchUp(self, args):
        if not self.touching:
            return
        shouldOpenUi = not self.HandleTouchUpGuard()
        if shouldOpenUi:
            clientSys = clientApi.GetSystem(com.modName, com.csname)
            clientSys.OpenDietScreen({})

    # 取消事件可能发生在屏幕切换或输入中断时，已进入拖动则保存，否则回滚到按下前位置。
    def ButtonTouchCancel(self, args):
        if not self.touching:
            return
        self.CancelLongPressTimer()
        if self.longPressed:
            self.SaveButtonPos()
        else:
            self.buttonControl.SetPosition(self.startButtonPos)
        self.ResetTouchState()

    # 长按计时完成后才允许拖动；如果期间发生移动或新触摸序列，旧计时回调直接失效。
    def LongPressReady(self, touchSeq):
        if touchSeq != self.touchSeq:
            return
        if not self.touching:
            return
        if self.touchMoved:
            return
        self.longPressTimer = None
        self.longPressed = True

    # 每次屏幕尺寸或原生 HUD 位置变化后，都把按钮重新压回安全区域。
    def CorrectCurrentButtonPos(self):
        if not self.buttonControl:
            return
        self.lastButtonGlobalPos = self.buttonControl.GetGlobalPosition()
        self.InitCollisionBox()
        pos = self.CorrectButtonGlobalPos(self.buttonControl.GetGlobalPosition())
        self.buttonControl.SetPosition(pos)
        self.SaveButtonPos()

    # 客户端配置用于保存 HUD 按钮位置，换存档时也沿用玩家自己的按钮布局。
    def RestoreButtonPos(self):
        compConfig = compFactory.CreateConfigClient(levelId)
        data = compConfig.GetConfigData(config.buttonConfigKey, True)
        if config.buttonPosKey not in data:
            return False
        pos = data[config.buttonPosKey]
        if len(pos) != 2:
            return False
        self.buttonControl.SetPosition((pos[0], pos[1]))
        return True

    # 拖动结束和屏幕纠正后立即保存，避免退出游戏前丢失玩家调整。
    def SaveButtonPos(self):
        compConfig = compFactory.CreateConfigClient(levelId)
        data = compConfig.GetConfigData(config.buttonConfigKey, True)
        pos = self.buttonControl.GetPosition()
        data[config.buttonPosKey] = [pos[0], pos[1]]
        compConfig.SetConfigData(config.buttonConfigKey, data, True)

    # 长按计时属于输入事务的一部分，提前取消可以避免旧回调污染下一次触摸。
    def CancelLongPressTimer(self):
        if not self.longPressTimer:
            return
        compGame = compFactory.CreateGame(levelId)
        compGame.CancelTimer(self.longPressTimer)
        self.longPressTimer = None

    # 释放或取消后清理触摸事务状态，下一次按下重新建立位置快照。
    def ResetTouchState(self):
        self.touching = False
        self.longPressed = False
        self.touchMoved = False
        self.startTouchPos = (0.0, 0.0)
        self.startButtonPos = (0.0, 0.0)
        self.startButtonGlobalPos = (0.0, 0.0)
        self.lastButtonGlobalPos = ()

    # 点击容忍少量手指抖动；超过阈值但未长按时不打开 UI。
    def TouchMovedTooFar(self, touchPos):
        dx = touchPos[0] - self.startTouchPos[0]
        dy = touchPos[1] - self.startTouchPos[1]
        limit = config.buttonClickMoveLimit
        return dx * dx + dy * dy >= limit * limit

    # 弹起守卫统一处理“点击/拖动/误滑”分流，避免同一次触摸既拖动又打开 UI。
    def HandleTouchUpGuard(self):
        self.CancelLongPressTimer()
        shouldBlockClick = self.longPressed or self.touchMoved
        if self.longPressed:
            self.SaveButtonPos()
        else:
            self.buttonControl.SetPosition(self.startButtonPos)
        self.ResetTouchState()
        return shouldBlockClick

    # 安全区来自当前屏幕视口；老运行时没有接口时退化为只依赖原生区域和无限边界。
    def GetSafeArea(self):
        if hasattr(clientApi, 'GetScreenViewInfo'):
            viewInfo = clientApi.GetScreenViewInfo()
            return (
                viewInfo[2],
                viewInfo[3],
                viewInfo[2] + viewInfo[0],
                viewInfo[3] + viewInfo[1]
            )
        return (0.0, 0.0, 32767.0, 32767.0)

    # 收集原生 HUD 热区和安全区外边界，拖动纠正时把这些区域视为不可进入区域。
    def InitOriginCollisionBox(self):
        collisionBox = []
        controls = (
            'pause', 'chat', 'fold_menu', 'emote',
            'camera_view', 'walkstate',
            'sneak_new_controls', 'jump_new_controls', 'sprint', 'default_move_stick_area',
            'destroy_or_attack', 'build_or_interact',
            'sneak', 'jump', 'ascend', 'descend',
            'move_left', 'move_up', 'move_right', 'move_down'
        )
        if hasattr(clientApi, 'GetOriginAreaOffset'):
            for name in controls:
                area = clientApi.GetOriginAreaOffset('binding.area.' + name)
                if area != (.0, .0, .0, .0):
                    collisionBox.append(area)
        safeArea = self.GetSafeArea()
        collisionBox += [
            (-32768.0, -32768.0, 32767.0, safeArea[1]),
            (-32768.0, -32768.0, safeArea[0], 32767.0),
            (-32768.0, safeArea[3], 32767.0, 32767.0),
            (safeArea[2], -32768.0, 32767.0, 32767.0)
        ]
        self.originCollisionBox = tuple(collisionBox)

    # 按钮中心点用于碰撞判断，所以需要按按钮半尺寸扩展所有不可进入区域。
    def InitCollisionBox(self):
        self.InitOriginCollisionBox()
        buttonSize = self.buttonControl.GetSize()
        halfX = buttonSize[0] / 2
        halfY = buttonSize[1] / 2
        self.collisionBox = tuple(
            (c[0] - halfX, c[1] - halfY, c[2] + halfX, c[3] + halfY)
            for c in self.originCollisionBox
        )

    # 将全局坐标换算成按钮父控件坐标，确保保存和 SetPosition 使用同一个坐标系。
    def GlobalToButtonPos(self, globalPos):
        buttonPos = self.buttonControl.GetPosition()
        buttonGlobalPos = self.buttonControl.GetGlobalPosition()
        return (
            buttonPos[0] + globalPos[0] - buttonGlobalPos[0],
            buttonPos[1] + globalPos[1] - buttonGlobalPos[1]
        )

    # 在候选点中选离目标最近的安全点，用于碰撞投影后的最终吸附。
    def GetNearestButtonPos(self, posList, pos):
        return min(posList, key=lambda x: (x[0] - pos[0]) ** 2 + (x[1] - pos[1]) ** 2)

    # 计算拖动线段碰到不可进入区域时的边界点，没有碰撞则保留目标点。
    def GetCollisionPos(self, pos, newPos):
        x1, y1 = pos
        x2, y2 = newPos
        collisionPos = []
        a, b, c, d = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        for x3, y3, x4, y4 in self.collisionBox:
            if (x2 < x1 and x3 >= x1) or (x2 > x1 and x4 <= x1) or (y2 < y1 and y3 >= y1) or (y2 > y1 and y4 <= y1):
                continue
            for x5, y5, x6, y6, px, py in (
                (x3, y3, x4, y3, x2, y3),
                (x3, y3, x3, y4, x3, y2),
                (x3, y4, x4, y4, x2, y4),
                (x4, y3, x4, y4, x4, y2)
            ):
                divisor = (x1 - x2) * (y5 - y6) - (y1 - y2) * (x5 - x6)
                if not divisor:
                    continue
                x7 = ((x1 * y2 - y1 * x2) * (x5 - x6) - (x1 - x2) * (x5 * y6 - y5 * x6)) / divisor
                y7 = ((x1 * y2 - y1 * x2) * (y5 - y6) - (y1 - y2) * (x5 * y6 - y5 * x6)) / divisor
                if a - 1e-6 < x7 < b + 1e-6 and c - 1e-6 < y7 < d + 1e-6 \
                and x3 - 1e-6 < x7 < x4 + 1e-6 and y3 - 1e-6 < y7 < y4 + 1e-6 \
                and not any(e[0] + 1e-6 < x7 < e[2] - 1e-6 and e[1] + 1e-6 < y7 < e[3] - 1e-6 for e in self.collisionBox) \
                and (((x5 != x7 or y5 != y7) and (x6 != x7 or y6 != y7)) or (x2 != x1 and y2 != y1)):
                    collisionPos.append((x7, y7, px, py))
        if collisionPos:
            return self.GetNearestButtonPos(collisionPos, newPos)
        return newPos

    # 把全局目标位置纠正到安全区和原生 HUD 热区之外，再转回按钮本地坐标。
    def CorrectButtonGlobalPos(self, globalPos):
        if not self.collisionBox:
            self.InitCollisionBox()
        buttonSize = self.buttonControl.GetSize()
        halfX = buttonSize[0] / 2
        halfY = buttonSize[1] / 2
        centerPos = (globalPos[0] + halfX, globalPos[1] + halfY)
        if any(c[0] < centerPos[0] < c[2] and c[1] < centerPos[1] < c[3] for c in self.collisionBox):
            if self.lastButtonGlobalPos:
                lastCenterPos = (
                    self.lastButtonGlobalPos[0] + halfX,
                    self.lastButtonGlobalPos[1] + halfY
                )
                centerPos = self.GetCollisionPos(lastCenterPos, centerPos)
                if len(centerPos) == 4:
                    centerPos = self.GetCollisionPos(centerPos[:2], centerPos[2:])[:2]
            else:
                safeArea = self.GetSafeArea()
                safeArea = (
                    safeArea[0] + halfX,
                    safeArea[1] + halfY,
                    safeArea[2] - halfX,
                    safeArea[3] - halfY
                )
                centerPos = tuple(min(max(centerPos[n], safeArea[n]), safeArea[n + 2]) for n in (0, 1))
                posList = tuple(
                    self.GetCollisionPos(p, centerPos)
                    for p in (
                        (safeArea[0], centerPos[1]),
                        (centerPos[0], safeArea[1]),
                        (safeArea[2], centerPos[1]),
                        (centerPos[0], safeArea[3])
                    )
                    if not any(c[0] < p[0] < c[2] and c[1] < p[1] < c[3] for c in self.collisionBox)
                )
                if posList:
                    centerPos = self.GetNearestButtonPos(posList, centerPos)
        if not any(c[0] < centerPos[0] < c[2] and c[1] < centerPos[1] < c[3] for c in self.collisionBox):
            self.lastButtonGlobalPos = (centerPos[0] - halfX, centerPos[1] - halfY)
            return self.GlobalToButtonPos(self.lastButtonGlobalPos)
        return self.buttonControl.GetPosition()

    # 拖动时使用按下瞬间的全局位置作为基准，避免锚点坐标系变化造成跳动。
    def LimitButtonPos(self, pos):
        globalPos = (
            self.startButtonGlobalPos[0] + pos[0] - self.startButtonPos[0],
            self.startButtonGlobalPos[1] + pos[1] - self.startButtonPos[1]
        )
        return self.CorrectButtonGlobalPos(globalPos)

    def Destroy(self):
        self.CancelLongPressTimer()
