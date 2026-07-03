# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as config

ClientSystem = clientApi.GetClientSystemCls()
engineNamespace = clientApi.GetEngineNamespace()
engineSystemName = clientApi.GetEngineSystemName()


class DietClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.dietData = None
        self.uiNode = None
        self.buttonUiNode = None
        self.pendingOpenDietScreen = False
        self.ListenForEvent(engineNamespace, engineSystemName, "UiInitFinished", self, self.UiInitFinished)
        self.ListenForEvent(engineNamespace, engineSystemName, "HudButtonChangedClientEvent", self, self.HudButtonChangedClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ScreenSizeChangedClientEvent", self, self.ScreenSizeChangedClientEvent)
        self.ListenForEvent(com.modName, com.ssname, "DietSyncData", self, self.DietSyncData)
        self.ListenForEvent(com.modName, com.ssname, "OpenDietScreen", self, self.OpenDietScreen)
        print("[DietNullGr] client ready")

    def UiInitFinished(self, args):
        clientApi.RegisterUI(com.modName, config.uiKey, config.uiPath, config.uiName)
        clientApi.RegisterUI(com.modName, config.buttonUiKey, config.buttonUiPath, config.buttonUiName)
        self.buttonUiNode = clientApi.CreateUI(com.modName, config.buttonUiKey, {'isHud': 1})
        # 客户端 UI 初始化完成后主动向服务端要一次数据，避免先打开界面时看到旧值。
        self.NotifyToServer("DietClientReady", {})

    def DietSyncData(self, args):
        self.dietData = args
        uiNode = clientApi.GetUI(com.modName, config.uiKey)
        # 热重载后 UI 管理器可能残留上一轮界面对象，只有本系统打开过的界面才接收同步刷新。
        if self.uiNode and uiNode:
            uiNode.UpdateDietData(args)
        if self.pendingOpenDietScreen:
            self.OpenDietScreen({})

    def OpenDietScreen(self, args):
        if self.dietData is None:
            self.pendingOpenDietScreen = True
            self.NotifyToServer("DietClientReady", {})
            return
        self.pendingOpenDietScreen = False
        uiNode = clientApi.GetUI(com.modName, config.uiKey)
        if self.uiNode and uiNode:
            uiNode.UpdateDietData(self.dietData)
            return
        self.uiNode = clientApi.PushScreen(com.modName, config.uiKey, {"dietData": self.dietData})

    def HudButtonChangedClientEvent(self, args):
        changedList = args['changedList']
        if self.buttonUiNode:
            self.buttonUiNode.CorrectCurrentButtonPos()

    def ScreenSizeChangedClientEvent(self, args):
        beforeX = args['beforeX']
        beforeY = args['beforeY']
        afterX = args['afterX']
        afterY = args['afterY']
        if self.buttonUiNode:
            self.buttonUiNode.CorrectCurrentButtonPos()

    def Destroy(self):
        pass
