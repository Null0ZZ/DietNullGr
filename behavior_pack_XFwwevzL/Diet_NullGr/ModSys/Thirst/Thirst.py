# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.Thirst.config as config


# 口渴真值始终限制在服务端定义的合法区间，外部玩法可以直接传入增减后的数值。
def clampThirstValue(value):
    if value < 0.0:
        return 0.0
    if value > config.maxValue:
        return config.maxValue
    return float(value)


# HUD 只消费 0 到 20 的离散格数，向上取整可以保留不足一点时的半格提示。
def getDisplayValue(value):
    displayValue = clampThirstValue(value) / config.maxValue * config.displayMaxValue
    roundedValue = int(displayValue)
    if displayValue > roundedValue:
        roundedValue += 1
    return roundedValue


# 从 ModAttr 恢复玩家口渴数据，关闭系统时仍保留原值，重新开启后可继续使用。
def loadPlayerData(playerId, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    return {
        'value': clampThirstValue(compModAttr.GetAttr(config.attrValue, config.defaultValue)),
        'enabled': bool(compModAttr.GetAttr(config.attrEnabled, True))
    }


# 数值与开关都在变动后立即持久化，避免退出游戏前丢失服务端真值。
def savePlayerData(playerId, data, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    compModAttr.SetAttr(config.attrValue, data['value'], needRestore=True)
    compModAttr.SetAttr(config.attrEnabled, data['enabled'], needRestore=True)


# 客户端只接收视觉表现所需字段，浮点真值继续留在服务端供玩法逻辑使用。
def buildClientData(data):
    return {
        'displayValue': getDisplayValue(data['value']),
        'visible': data['enabled'],
        'critical': data['enabled'] and data['value'] <= config.criticalValue
    }


# 所有口渴 HUD 更新统一走同一事件，避免外部接口直接操作客户端 UI。
def syncToClient(serverSys, playerId, data):
    serverSys.NotifyToClient(playerId, config.syncEvent, buildClientData(data))


# 口渴模块只同步自己的设置项，客户端设置管理器负责把分批数据合并为同一页控件。
def syncSettingToClient(serverSys, playerId, data):
    serverSys.NotifyToClient(playerId, config.settingEventSync, {
        'values': {
            config.settingEnabledKey: data['enabled']
        }
    })
