# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Thirst.config as config

ClientSystem = clientApi.GetClientSystemCls()
engineNamespace = clientApi.GetEngineNamespace()
engineSystemName = clientApi.GetEngineSystemName()


class ClientSys(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.thirstData = None
        self.uiNode = None
        self.ListenForEvent(engineNamespace, engineSystemName, "UiInitFinished", self, self.UiInitFinished)
        self.ListenForEvent(com.modName, config.ssname, config.syncEvent, self, self.ThirstSyncData)
        print("[DietNullGr] thirst client ready")

    def UiInitFinished(self, args):
        clientApi.RegisterUI(com.modName, config.uiKey, config.uiPath, config.uiName)
        self.uiNode = clientApi.CreateUI(com.modName, config.uiKey, {'isHud': 1})
        if self.thirstData is not None:
            self.uiNode.UpdateThirstData(self.thirstData)
        # HUD 创建后主动请求真值，补齐服务端数据早于 UI 初始化到达时的时序缺口。
        self.NotifyToServer(config.clientReadyEvent, {})

    def ThirstSyncData(self, args):
        displayValue = args['displayValue']
        visible = args['visible']
        style = args['style']
        critical = args['critical']
        self.thirstData = {
            'displayValue': displayValue,
            'visible': visible,
            'style': style,
            'critical': critical
        }
        if self.uiNode:
            self.uiNode.UpdateThirstData(self.thirstData)

    def Destroy(self):
        pass
