# -*- coding: utf-8 -*-

ssname = "Thirst_Core_ServerSys"
csname = "Thirst_Core_ClientSys"
ssPath = "Diet_NullGr.ModSys.Thirst.Thirst_ss.ServerSys"
csPath = "Diet_NullGr.ModSys.Thirst.Thirst_cs.ClientSys"

serverSysKey = {
    ssname: ssPath
}

clientSysKey = {
    csname: csPath
}

uiKey = "thirst_hud"
uiName = "thirst_hud.main"
uiPath = "Diet_NullGr.ModSys.Thirst.ThirstHUD.ThirstHUD"

maxValue = 20.0
defaultValue = 20.0
displayMaxValue = 20
criticalValue = 6.0

attrValue = "diet_nullgr_thirst_value"
attrEnabled = "diet_nullgr_thirst_enabled"
syncEvent = "ThirstSyncData"
clientReadyEvent = "ThirstClientReady"
settingEnabledKey = "thirst_enabled"
settingEventUpdate = "DietSettingUpdate"
settingEventSync = "DietSettingSync"

flashInterval = 0.12
flashToggleCount = 6

settingDef = {
    "key": settingEnabledKey,
    "name": "启用口渴值",
    "control": "toggle",
    "default": True,
    "priority": 15,
    "groupId": ""
}
