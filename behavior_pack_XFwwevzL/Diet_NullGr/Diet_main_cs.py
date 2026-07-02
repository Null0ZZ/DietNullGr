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
        self.ListenForEvent(engineNamespace, engineSystemName, "UiInitFinished", self, self.UiInitFinished)
        self.ListenForEvent(com.modName, com.ssname, "DietSyncData", self, self.DietSyncData)
        self.ListenForEvent(com.modName, com.ssname, "OpenDietScreen", self, self.OpenDietScreen)
        print("[DietNullGr] client ready")

    def UiInitFinished(self, args):
        clientApi.RegisterUI(com.modName, config.uiKey, config.uiPath, config.uiName)
        # 客户端 UI 初始化完成后主动向服务端要一次数据，避免先打开界面时看到旧值。
        self.NotifyToServer("DietClientReady", {})

    def DietSyncData(self, args):
        self.dietData = args
        uiNode = clientApi.GetUI(com.modName, config.uiKey)
        # 热重载后 UI 管理器可能残留上一轮界面对象，只有本系统打开过的界面才接收同步刷新。
        if self.uiNode and uiNode:
            uiNode.UpdateDietData(args)

    def OpenDietScreen(self, args):
        if self.dietData is None:
            self.NotifyToServer("DietClientReady", {})
            return
        uiNode = clientApi.GetUI(com.modName, config.uiKey)
        if self.uiNode and uiNode:
            uiNode.UpdateDietData(self.dietData)
            return
        self.uiNode = clientApi.PushScreen(com.modName, config.uiKey, {"dietData": self.dietData})

    def Destroy(self):
        pass
