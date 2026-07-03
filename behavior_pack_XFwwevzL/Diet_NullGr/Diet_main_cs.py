# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as config

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
engineNamespace = clientApi.GetEngineNamespace()
engineSystemName = clientApi.GetEngineSystemName()


class DietClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.dietData = None
        self.uiNode = None
        self.buttonUiNode = None
        self.pendingOpenDietScreen = False
        self.settingInst = None
        self.settingRegistered = False
        self.settingRegisteredKeys = []
        self.settingSyncing = False
        self.settingSyncValues = {}
        self.settingCallbacks = {
            config.settingActiveKey: self.DietActiveSettingChanged,
            config.settingGroupKeys['fruits']: self.DietFruitsSettingChanged,
            config.settingGroupKeys['grains']: self.DietGrainsSettingChanged,
            config.settingGroupKeys['proteins']: self.DietProteinsSettingChanged,
            config.settingGroupKeys['vegetables']: self.DietVegetablesSettingChanged,
            config.settingGroupKeys['sugars']: self.DietSugarsSettingChanged
        }
        self.ListenForEvent(engineNamespace, engineSystemName, "UiInitFinished", self, self.UiInitFinished)
        self.ListenForEvent(engineNamespace, engineSystemName, "HudButtonChangedClientEvent", self, self.HudButtonChangedClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ScreenSizeChangedClientEvent", self, self.ScreenSizeChangedClientEvent)
        self.ListenForEvent(com.modName, com.ssname, "DietSyncData", self, self.DietSyncData)
        self.ListenForEvent(com.modName, com.ssname, "OpenDietScreen", self, self.OpenDietScreen)
        self.ListenForEvent(com.modName, com.ssname, config.settingEventSync, self, self.DietSettingSync)
        print("[DietNullGr] client ready")

    def UiInitFinished(self, args):
        self.RegisterDietSettingInst()
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

    def DietSettingSync(self, args):
        values = args['values']
        if not self.settingInst:
            return
        if not self.settingRegistered:
            self.RegisterDietSettingControls(values)
            return
        for settingKey in values:
            if settingKey not in self.settingRegisteredKeys:
                continue
            self.SyncDietSettingToggle(settingKey, values[settingKey])

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

    # RegisterSettingInst 必须在 UiInitFinished 后调用，设置控件则等服务端状态回来后再注册默认值。
    def RegisterDietSettingInst(self):
        compNeteaseWindow = compFactory.CreateNeteaseWindow(levelId)
        self.settingInst = compNeteaseWindow.RegisterSettingInst(
            config.settingItemId,
            config.settingName,
            config.settingIconPath
        )

    # 通用设置控件只注册一次，后续服务端状态变化统一用 SetToggleDefault 回填。
    def RegisterDietSettingControls(self, values):
        if self.settingRegistered:
            return
        for settingDef in config.settingDefs:
            value = bool(values[settingDef['key']])
            self.settingInst.AddToggle(
                settingDef['key'],
                settingDef['name'],
                self.settingCallbacks[settingDef['key']],
                settingDef['priority'],
                value
            )
            self.settingRegisteredKeys.append(settingDef['key'])
        self.settingRegistered = True

    # AddToggle 在不同引擎版本会回传 value 或 (key, value)，每个回调固定自己的设置键再统一写回服务端。
    def DietActiveSettingChanged(self, *args):
        value = args[0] if len(args) == 1 else args[1]
        self.NotifyDietSettingChanged(config.settingActiveKey, value)

    def DietFruitsSettingChanged(self, *args):
        value = args[0] if len(args) == 1 else args[1]
        self.NotifyDietSettingChanged(config.settingGroupKeys['fruits'], value)

    def DietGrainsSettingChanged(self, *args):
        value = args[0] if len(args) == 1 else args[1]
        self.NotifyDietSettingChanged(config.settingGroupKeys['grains'], value)

    def DietProteinsSettingChanged(self, *args):
        value = args[0] if len(args) == 1 else args[1]
        self.NotifyDietSettingChanged(config.settingGroupKeys['proteins'], value)

    def DietVegetablesSettingChanged(self, *args):
        value = args[0] if len(args) == 1 else args[1]
        self.NotifyDietSettingChanged(config.settingGroupKeys['vegetables'], value)

    def DietSugarsSettingChanged(self, *args):
        value = args[0] if len(args) == 1 else args[1]
        self.NotifyDietSettingChanged(config.settingGroupKeys['sugars'], value)

    # 同步回填期间 SetToggleDefault 可能触发同一个回调，必须拦截这次回声，避免客户端把服务端状态再写回一次。
    def NotifyDietSettingChanged(self, settingKey, value):
        value = bool(value)
        if self.settingSyncing and settingKey in self.settingSyncValues and bool(self.settingSyncValues[settingKey]) == value:
            return
        self.NotifyToServer(config.settingEventUpdate, {
            'key': settingKey,
            'value': value
        })

    # 服务端才是设置真值来源，客户端控件默认值只做展示回填，finally 用来恢复同步标记而不吞掉 API 异常。
    def SyncDietSettingToggle(self, settingKey, value):
        value = bool(value)
        oldSettingSyncing = self.settingSyncing
        oldSettingSyncValues = self.settingSyncValues
        if not oldSettingSyncing:
            self.settingSyncing = True
            self.settingSyncValues = {settingKey: value}
        try:
            self.settingInst.SetToggleDefault(settingKey, value)
        finally:
            if not oldSettingSyncing:
                self.settingSyncing = False
                self.settingSyncValues = {}
            else:
                self.settingSyncing = oldSettingSyncing
                self.settingSyncValues = oldSettingSyncValues

    def Destroy(self):
        pass
