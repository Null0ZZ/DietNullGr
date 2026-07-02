# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.Diet.config as config


# 将 Diet 原版 0.0-1.0 的营养值限制在合法范围，所有读写入口都经过这里，避免存档值越界。
def clampDietValue(value):
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


# 创建五类食物组的默认玩家数据，新玩家和死亡重置都会走同一套默认值。
def createDefaultValues():
    values = {}
    for groupId in config.groupOrder:
        values[groupId] = config.groups[groupId]['defaultValue']
    return values


# 从 ModAttr 读取玩家饮食数据，ModAttr 负责跨存档恢复，内存数据只做本次会话的快速缓存。
def loadPlayerData(playerId, compFactory, minecraftEnum):
    compModAttr = compFactory.CreateModAttr(playerId)
    compAttr = compFactory.CreateAttr(playerId)
    values = {}
    for groupId in config.groupOrder:
        values[groupId] = clampDietValue(compModAttr.GetAttr(config.attrPrefix + groupId, config.groups[groupId]['defaultValue']))
    return {
        'values': values,
        'active': compModAttr.GetAttr(config.attrPrefix + 'active', True),
        'eaten': compModAttr.GetAttr(config.attrPrefix + 'eaten', ''),
        'prevHunger': compAttr.GetAttrValue(minecraftEnum.AttrType.HUNGER)
    }


# 每次进食、衰减、死亡惩罚或命令修改后立即写回，避免退出游戏前数据丢失。
def savePlayerData(playerId, data, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    for groupId in config.groupOrder:
        compModAttr.SetAttr(config.attrPrefix + groupId, data['values'][groupId], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'active', data['active'], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'eaten', data['eaten'], needRestore=True)


# 把内部数据转换为客户端 UI 直接可消费的结构，减少客户端重复读取配置。
def buildClientData(data):
    groupList = []
    for groupId in config.groupOrder:
        groupConfig = config.groups[groupId]
        groupList.append({
            'id': groupId,
            'name': groupConfig['name'],
            'tooltip': groupConfig['tooltip'],
            'icon': groupConfig['icon'],
            'color': groupConfig['color'],
            'value': data['values'][groupId]
        })
    return {
        'active': data['active'],
        'groups': groupList,
        'effectsText': buildEffectsText(data)
    }


# 服务端和客户端只通过这一条同步事件交换饮食数据，UI 打开、进食、衰减都会复用同一链路。
def syncToClient(serverSys, playerId, data):
    serverSys.NotifyToClient(playerId, "DietSyncData", buildClientData(data))


# 普通玩家反馈统一走聊天提示，命令和进食记录保持同一种表现。
def sendMessage(playerId, compFactory, message, color):
    compMsg = compFactory.CreateMsg(playerId)
    compMsg.NotifyOneMessage(playerId, message, color)


# 记录玩家已经吃过的食物，后续扩展 tooltip 隐藏规则时可以直接复用这份数据。
def addEatenFood(data, itemName):
    if data['eaten'] == "":
        data['eaten'] = itemName
        return
    eatenList = data['eaten'].split(";")
    if itemName in eatenList:
        return
    eatenList.append(itemName)
    data['eaten'] = ";".join(eatenList)


# 复刻上游 DietApiImpl.calculate：按饥饿值、营养值和食物组数量计算本次进食增量。
def calculateGain(hunger, nutrition, foodGroupIds):
    groupCount = len(foodGroupIds)
    quality = (hunger + (hunger * nutrition)) / float(groupCount)
    gain = (quality * 0.25) / (quality + 15.0)
    gain *= (1.0 - config.gainPenaltyPerGroup / 100.0) ** (groupCount - 1)
    values = {}
    for groupId in foodGroupIds:
        value = gain * config.groups[groupId]['gainMultiplier']
        value = round(value * 200.0) / 200.0
        if value < 0.005:
            value = 0.005
        values[groupId] = value
    return values


# 玩家真正吃下食物后调用，未分类食物不改动数据，已分类食物按组叠加到 100% 上限。
def applyFoodGain(data, itemName, hunger, nutrition):
    if itemName not in config.foodGroups:
        return False
    foodGroupIds = config.foodGroups[itemName]
    gainValues = calculateGain(hunger, nutrition, foodGroupIds)
    for groupId in foodGroupIds:
        data['values'][groupId] = clampDietValue(data['values'][groupId] + gainValues[groupId])
    addEatenFood(data, itemName)
    return True


# 复刻 PlayerDietTracker.decay：饥饿条下降时，所有已有值按 exp(value) 曲线共同衰减。
def applyHungerDecay(data, foodDiff):
    activeCount = 0
    for groupId in config.groupOrder:
        if data['values'][groupId] > 0.0:
            activeCount += 1
    if activeCount <= 0:
        return
    scale = float(foodDiff) / float(activeCount)
    scale *= (1.0 - config.decayPenaltyPerGroup / 100.0) ** (activeCount - 1)
    for groupId in config.groupOrder:
        value = data['values'][groupId]
        decay = (config.expBase ** value) * scale * config.groups[groupId]['decayMultiplier'] / 100.0
        if decay > 0.0:
            data['values'][groupId] = clampDietValue(value - decay)


# 上游默认死亡惩罚为 AMOUNT 扣除 100%，这里等价为复活后回到各组默认值。
def applyDeathPenalty(data):
    for groupId in config.groupOrder:
        value = data['values'][groupId] - config.deathPenaltyLoss
        if value < config.deathPenaltyMin:
            value = config.groups[groupId]['defaultValue']
        data['values'][groupId] = clampDietValue(value)


# 判断当前数值命中的饮食效果，服务端施加效果和 UI 文案共用同一套条件。
def getMatchedEffects(data):
    values = data['values']
    matched = []
    balanced = True
    for groupId in ["proteins", "fruits", "vegetables", "grains"]:
        if values[groupId] < 0.8:
            balanced = False
    if balanced:
        matched.append("balanced")
    if values['sugars'] >= 0.8:
        matched.append("sugarRush")
    return matched


# 将命中的饮食效果翻译成 UI 文本，空效果时明确显示暂无奖励。
def buildEffectsText(data):
    matched = getMatchedEffects(data)
    if not matched:
        return "当前没有饮食效果"
    texts = []
    for effectId in matched:
        texts.append(config.effectDescriptions[effectId])
    return "\n".join(texts)


# 每 4 秒刷新一次短时状态效果，持续时间略长于刷新周期，避免效果闪断。
def applyEffects(playerId, data, compFactory):
    matched = getMatchedEffects(data)
    if not matched:
        return
    compEffect = compFactory.CreateEffect(playerId)
    if "balanced" in matched:
        compEffect.AddEffectToEntity("health_boost", 6, 0, True)
        compEffect.AddEffectToEntity("strength", 6, 0, True)
        compEffect.AddEffectToEntity("resistance", 6, 0, True)
    if "sugarRush" in matched:
        compEffect.AddEffectToEntity("speed", 6, 0, True)
        compEffect.AddEffectToEntity("hunger", 6, 2, True)


# 处理 /diet 系列命令；命令属于玩家输入边界，这里会返回错误消息而不是让解析异常打断服务端。
def handleCommand(command, data):
    text = command
    if text.startswith("/"):
        text = text[1:]
    parts = text.split()
    if not parts or parts[0] != "diet":
        return {'handled': False, 'changed': False, 'openUi': False, 'message': '', 'color': '§f'}
    result = {'handled': True, 'changed': False, 'openUi': False, 'message': '', 'color': '§a'}
    if len(parts) == 1 or parts[1] == "open":
        result['openUi'] = True
        result['message'] = "已打开均衡饮食界面"
        return result
    action = parts[1]
    if action == "reset":
        data['values'] = createDefaultValues()
        result['changed'] = True
        result['message'] = "均衡饮食数据已重置"
        return result
    if action == "pause":
        data['active'] = False
        result['changed'] = True
        result['message'] = "均衡饮食已暂停"
        return result
    if action == "resume":
        data['active'] = True
        result['changed'] = True
        result['message'] = "均衡饮食已恢复"
        return result
    if action == "export":
        result['message'] = buildExportText(data)
        return result
    if action == "get" and len(parts) >= 3:
        groupId = parts[-1]
        if groupId not in config.groups:
            result['color'] = '§c'
            result['message'] = "未知食物组: {}".format(groupId)
            return result
        result['message'] = "{} = {}%".format(config.groups[groupId]['name'], int(data['values'][groupId] * 100.0))
        return result
    if action in ["set", "add", "subtract"] and len(parts) >= 4:
        groupId = parts[-2]
        if groupId not in config.groups:
            result['color'] = '§c'
            result['message'] = "未知食物组: {}".format(groupId)
            return result
        try:
            amount = float(parts[-1])
        except ValueError:
            result['color'] = '§c'
            result['message'] = "数值必须是数字"
            return result
        if amount > 1.0:
            amount = amount / 100.0
        if action == "set":
            data['values'][groupId] = clampDietValue(amount)
        elif action == "add":
            data['values'][groupId] = clampDietValue(data['values'][groupId] + amount)
        else:
            data['values'][groupId] = clampDietValue(data['values'][groupId] - amount)
        result['changed'] = True
        result['message'] = "{} = {}%".format(config.groups[groupId]['name'], int(data['values'][groupId] * 100.0))
        return result
    result['color'] = '§c'
    result['message'] = "用法: /diet open|get|set|add|subtract|reset|pause|resume|export"
    return result


# 导出当前玩家五组百分比，便于测试和服主管理时直接复制日志结果。
def buildExportText(data):
    texts = []
    for groupId in config.groupOrder:
        texts.append("{}:{}%".format(groupId, int(data['values'][groupId] * 100.0)))
    return "Diet[" + ", ".join(texts) + "]"
