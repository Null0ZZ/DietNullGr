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
baseDecayIntervalTick = 20
baseDecayPerSecond = 1.0 / 180.0
hungerDecayFactor = 0.2
dataSaveIntervalTick = 600
respawnValue = 20.0
dehydrationDamageIntervalTick = 80
dehydrationDamage = 1.0
easyDehydrationMinHealth = 10.0
normalDehydrationMinHealth = 1.0

playerEatDrinkEvent = "PlayerEatFoodServerEvent"
actorUseDrinkEvent = "ActorUseItemServerEvent"

drinkItemValues = {
    "minecraft:milk_bucket": {
        "event": playerEatDrinkEvent,
        "defaultValue": 8.0,
        "auxValues": {}
    },
    # 水瓶与可饮用药水共用同一物品 ID；水瓶使用附加值 0，其余药水暂用默认补水量。
    "minecraft:potion": {
        "event": actorUseDrinkEvent,
        "defaultValue": 4.0,
        "auxValues": {
            0: 6.0
        }
    }
}

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
    "name": "启用口渴值（开启后口渴会持续消耗，低值限制冲刺，耗尽时受伤；关闭后隐藏口渴条并停止这些影响）",
    "control": "toggle",
    "default": True,
    "priority": 15,
    "groupId": ""
}
