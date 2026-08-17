# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Disease.config as diseaseConfig
import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Thirst.config as thirstConfig

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
        self.settingCallbacks = {}
        for settingDef in config.settingDefs:
            self.settingCallbacks[settingDef['key']] = self.CreateDietSettingCallback(settingDef)
        # 客户端系统建立时立即注册可修改的键位映射，首次默认使用 Y 键。
        playerViewComp = compFactory.CreatePlayerView(levelId)
        playerViewComp.RegisterCustomKeyMapping(
            config.openDietScreenKeyName,
            clientApi.GetMinecraftEnum().KeyBoardType.KEY_Y,
            config.openDietScreenKeyCategory
        )
        self.ListenForEvent(engineNamespace, engineSystemName, "UiInitFinished", self, self.UiInitFinished)
        self.ListenForEvent(engineNamespace, engineSystemName, "HudButtonChangedClientEvent", self, self.HudButtonChangedClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnCustomKeyPressInGame", self, self.OnCustomKeyPressInGame)
        self.ListenForEvent(engineNamespace, engineSystemName, "ScreenSizeChangedClientEvent", self, self.ScreenSizeChangedClientEvent)
        self.ListenForEvent(com.modName, com.ssname, "DietSyncData", self, self.DietSyncData)
        self.ListenForEvent(com.modName, com.ssname, "OpenDietScreen", self, self.OpenDietScreen)
        self.ListenForEvent(com.modName, com.ssname, config.settingEventSync, self, self.DietSettingSync)
        self.ListenForEvent(com.modName, thirstConfig.ssname, config.settingEventSync, self, self.DietSettingSync)
        self.ListenForEvent(com.modName, diseaseConfig.ssname, config.settingEventSync, self, self.DietSettingSync)
        self.ListenForEvent(com.modName, com.ssname, config.lowNutritionAlertEvent, self, self.DietLowNutritionAlert)
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
        registeredKeysBefore = self.settingRegisteredKeys[:]
        if not self.settingRegistered:
            self.RegisterDietSettingControls(values)
        for settingKey in values:
            # 新控件已由 AddToggle/AddSlider 的默认值完成初始化，只回填此前存在的控件以避免触发设置回声。
            if settingKey not in registeredKeysBefore:
                continue
            self.SyncDietSettingControl(settingKey, values[settingKey])

    def DietLowNutritionAlert(self, args):
        sound = args['sound']
        volume = args['volume']
        pitch = args['pitch']
        playerId = clientApi.GetLocalPlayerId()
        customAudioComp = compFactory.CreateCustomAudio(levelId)
        customAudioComp.PlayCustomMusic(sound, (0, 0, 0), volume, pitch, False, playerId)

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

    def OnCustomKeyPressInGame(self, args):
        name = args['name']
        key = args['key']
        category = args['category']
        isDown = args['isDown']
        screenName = args['screenName']
        # 不锁死事件回传的键码，玩家在设置中重新绑定后仍通过同一映射打开界面。
        if name != config.openDietScreenKeyName or category != config.openDietScreenKeyCategory or isDown != '1':
            return
        # 与 HUD 按钮共用打开链；数据未同步时 OpenDietScreen 会先请求数据，再在同步事件中入栈。
        self.OpenDietScreen({})

    # RegisterSettingInst 必须在 UiInitFinished 后调用，设置控件则等服务端状态回来后再注册默认值。
    def RegisterDietSettingInst(self):
        compNeteaseWindow = compFactory.CreateNeteaseWindow(levelId)
        self.settingInst = compNeteaseWindow.RegisterSettingInst(
            config.settingItemId,
            config.settingName,
            config.settingIconPath
        )
        if not self.settingInst:
            return
        self.settingInst.AddButton(
            config.settingResetOpenButtonPositionKey,
            config.settingResetOpenButtonPositionName,
            config.settingResetOpenButtonPositionText,
            self.ResetOpenButtonPosition,
            config.settingResetOpenButtonPositionPriority
        )

    # 重置按钮只恢复本机 HUD 坐标，不进入服务端饮食设置同步链。
    def ResetOpenButtonPosition(self, *args):
        if self.buttonUiNode:
            self.buttonUiNode.ResetButtonPos()

    # 通用设置控件回调可能只回传 value，这里给每个控件绑定固定 key，保证写回服务端时不依赖回调参数形态。
    def CreateDietSettingCallback(self, settingDef):
        settingKey = settingDef['key']
        def DietSettingControlChanged(*args):
            value = args[0] if len(args) == 1 else args[1]
            # 下拉框回调返回选项索引，发送服务端前转换为双方约定的稳定样式字符串。
            if settingDef['control'] == config.controlDropDown:
                value = settingDef['options'][int(value)]
            self.NotifyDietSettingChanged(settingKey, value)
        return DietSettingControlChanged

    # 不同服务端模块会分批同步设置项；已注册项保持不动，只为本次数据中出现的新 key 创建控件。
    def RegisterDietSettingControls(self, values):
        if self.settingRegistered:
            return
        for settingDef in config.settingDefs:
            settingKey = settingDef['key']
            if settingKey in self.settingRegisteredKeys:
                continue
            if settingKey not in values:
                continue
            if settingDef['control'] == config.controlToggle:
                self.settingInst.AddToggle(
                    settingKey,
                    settingDef['name'],
                    self.settingCallbacks[settingKey],
                    settingDef['priority'],
                    bool(values[settingKey])
                )
            elif settingDef['control'] == config.controlSlider:
                self.settingInst.AddSlider(
                    settingKey,
                    settingDef['name'],
                    settingDef['step'],
                    self.settingCallbacks[settingKey],
                    settingDef['priority'],
                    int(values[settingKey])
                )
            elif settingDef['control'] == config.controlDropDown:
                self.settingInst.AddDropDown(
                    settingKey,
                    settingDef['name'],
                    settingDef['options'],
                    self.settingCallbacks[settingKey],
                    settingDef['priority'],
                    values[settingKey]
                )
            self.settingRegisteredKeys.append(settingKey)
        self.settingRegistered = len(self.settingRegisteredKeys) == len(config.settingDefs)

    # 同步回填期间 SetDefault 可能触发同一个回调，必须拦截这次回声，避免客户端把服务端状态再写回一次。
    def NotifyDietSettingChanged(self, settingKey, value):
        if self.settingSyncing and settingKey in self.settingSyncValues and self.settingSyncValues[settingKey] == value:
            return
        self.NotifyToServer(config.settingEventUpdate, {
            'key': settingKey,
            'value': value
        })

    # 服务端才是设置真值来源，客户端控件默认值只做展示回填，finally 用来恢复同步标记而不吞掉 API 异常。
    def SyncDietSettingControl(self, settingKey, value):
        settingDef = config.settingDefByKey[settingKey]
        oldSettingSyncing = self.settingSyncing
        oldSettingSyncValues = self.settingSyncValues
        if not oldSettingSyncing:
            self.settingSyncing = True
            self.settingSyncValues = {settingKey: value}
        try:
            if settingDef['control'] == config.controlToggle:
                self.settingInst.SetToggleDefault(settingKey, bool(value))
            elif settingDef['control'] == config.controlSlider:
                self.settingInst.SetSliderDefault(settingKey, int(value))
            elif settingDef['control'] == config.controlDropDown:
                self.settingInst.SetDropDownDefault(settingKey, value)
        finally:
            if not oldSettingSyncing:
                self.settingSyncing = False
                self.settingSyncValues = {}
            else:
                self.settingSyncing = oldSettingSyncing
                self.settingSyncValues = oldSettingSyncValues

    def Destroy(self):
        pass
