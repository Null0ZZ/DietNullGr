# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.Diet.config as config

runtimeFoodGroups = {}


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


# 创建五类营养追踪开关的默认状态，通用设置和服务端计算共用这份结构。
def createDefaultTracking():
    tracking = {}
    for groupId in config.groupOrder:
        tracking[groupId] = True
    return tracking


# 从 ModAttr 读取玩家饮食数据，ModAttr 负责跨存档恢复，内存数据只做本次会话的快速缓存。
def loadPlayerData(playerId, compFactory, minecraftEnum):
    compModAttr = compFactory.CreateModAttr(playerId)
    compAttr = compFactory.CreateAttr(playerId)
    values = {}
    tracking = {}
    for groupId in config.groupOrder:
        values[groupId] = clampDietValue(compModAttr.GetAttr(config.attrPrefix + groupId, config.groups[groupId]['defaultValue']))
        tracking[groupId] = compModAttr.GetAttr(config.attrPrefix + 'track_' + groupId, True)
    return {
        'values': values,
        'tracking': tracking,
        'active': compModAttr.GetAttr(config.attrPrefix + 'active', True),
        'eaten': compModAttr.GetAttr(config.attrPrefix + 'eaten', ''),
        'prevHunger': compAttr.GetAttrValue(minecraftEnum.AttrType.HUNGER)
    }


# 每次进食、衰减、死亡惩罚或命令修改后立即写回，避免退出游戏前数据丢失。
def savePlayerData(playerId, data, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    for groupId in config.groupOrder:
        compModAttr.SetAttr(config.attrPrefix + groupId, data['values'][groupId], needRestore=True)
        compModAttr.SetAttr(config.attrPrefix + 'track_' + groupId, data['tracking'][groupId], needRestore=True)
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
            'value': data['values'][groupId],
            'tracked': data['tracking'][groupId]
        })
    return {
        'active': data['active'],
        'groups': groupList,
        'effectsText': buildEffectsText(data)
    }


# 服务端和客户端只通过这一条同步事件交换饮食数据，UI 打开、进食、衰减都会复用同一链路。
def syncToClient(serverSys, playerId, data):
    serverSys.NotifyToClient(playerId, "DietSyncData", buildClientData(data))


# 把通用设置状态压成客户端控件需要的键值，避免客户端直接推断服务端存档字段。
def buildSettingValues(data):
    values = {
        config.settingActiveKey: data['active']
    }
    for groupId in config.groupOrder:
        values[config.settingGroupKeys[groupId]] = data['tracking'][groupId]
    return values


# 通用设置控件和饮食面板共享服务端数据，任意数据变更后都从这里回填客户端控件默认值。
def syncSettingToClient(serverSys, playerId, data):
    serverSys.NotifyToClient(playerId, config.settingEventSync, {
        'values': buildSettingValues(data)
    })


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


# 校验外部联动传入的食物组，并按配置顺序去重，保证 UI、衰减和效果判断读取顺序一致。
def normalizeFoodGroupIds(foodGroupIds):
    selectedGroups = {}
    for groupId in foodGroupIds:
        if groupId not in config.groups:
            print("[DietNullGr] 未知饮食类别: {}".format(groupId))
            return []
        selectedGroups[groupId] = True
    normalizedGroupIds = []
    for groupId in config.groupOrder:
        if groupId in selectedGroups:
            normalizedGroupIds.append(groupId)
    return normalizedGroupIds


# 外部模组手动注册物品饮食分类，适合不想改物品 JSON 或需要运行时决定分类的联动。
def registerFoodGroups(itemName, foodGroupIds):
    normalizedGroupIds = normalizeFoodGroupIds(foodGroupIds)
    if not normalizedGroupIds:
        return False
    runtimeFoodGroups[itemName] = normalizedGroupIds
    return True


# 移除外部运行时注册的物品分类，只影响联动接口写入的数据，不会删掉本模组内置表。
def removeRegisteredFood(itemName):
    if itemName not in runtimeFoodGroups:
        return False
    del runtimeFoodGroups[itemName]
    return True


# 外部模组扩展 tag 到饮食分类的映射，便于一个自定义 tag 批量覆盖多种食物。
def registerDietTag(tagName, foodGroupIds):
    normalizedGroupIds = normalizeFoodGroupIds(foodGroupIds)
    if not normalizedGroupIds:
        return False
    config.dietTagGroups[tagName] = normalizedGroupIds
    return True


# 进食时统一合并内置表、外部注册表和物品 JSON tag，三种联动方式共享同一套增量计算。
def getFoodGroupIds(itemName, itemAuxValue, compItem):
    selectedGroups = {}
    if itemName in config.foodGroups:
        for groupId in config.foodGroups[itemName]:
            selectedGroups[groupId] = True
    if itemName in runtimeFoodGroups:
        for groupId in runtimeFoodGroups[itemName]:
            selectedGroups[groupId] = True
    itemTags = compItem.GetItemTags(itemName, itemAuxValue)
    for tagName in itemTags:
        if tagName in config.dietTagGroups:
            for groupId in config.dietTagGroups[tagName]:
                selectedGroups[groupId] = True
    foodGroupIds = []
    for groupId in config.groupOrder:
        if groupId in selectedGroups:
            foodGroupIds.append(groupId)
    return foodGroupIds


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
def applyFoodGain(data, itemName, itemAuxValue, hunger, nutrition, compItem):
    foodGroupIds = getFoodGroupIds(itemName, itemAuxValue, compItem)
    if not foodGroupIds:
        return False
    trackedFoodGroupIds = []
    for groupId in foodGroupIds:
        if data['tracking'][groupId]:
            trackedFoodGroupIds.append(groupId)
    if not trackedFoodGroupIds:
        return False
    gainValues = calculateGain(hunger, nutrition, trackedFoodGroupIds)
    for groupId in trackedFoodGroupIds:
        data['values'][groupId] = clampDietValue(data['values'][groupId] + gainValues[groupId])
    addEatenFood(data, itemName)
    return True


# 复刻 PlayerDietTracker.decay：饥饿条下降时，所有已有值按 exp(value) 曲线共同衰减。
def applyHungerDecay(data, foodDiff):
    activeCount = 0
    for groupId in config.groupOrder:
        if data['tracking'][groupId] and data['values'][groupId] > 0.0:
            activeCount += 1
    if activeCount <= 0:
        return
    scale = float(foodDiff) / float(activeCount)
    scale *= (1.0 - config.decayPenaltyPerGroup / 100.0) ** (activeCount - 1)
    for groupId in config.groupOrder:
        if not data['tracking'][groupId]:
            continue
        value = data['values'][groupId]
        decay = (config.expBase ** value) * scale * config.groups[groupId]['decayMultiplier'] / 100.0
        if decay > 0.0:
            data['values'][groupId] = clampDietValue(value - decay)


# 上游默认死亡惩罚为 AMOUNT 扣除 100%，这里等价为复活后回到各组默认值。
def applyDeathPenalty(data):
    for groupId in config.groupOrder:
        if not data['tracking'][groupId]:
            continue
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
        if not data['tracking'][groupId] or values[groupId] < 0.8:
            balanced = False
    if balanced:
        matched.append("balanced")
    if data['tracking']['sugars'] and values['sugars'] >= 0.8:
        matched.append("sugarRush")
    return matched


# 将命中的饮食效果翻译成 UI 文本，空效果时明确显示暂无奖励。
def buildEffectsText(data):
    if not data['active']:
        return "均衡饮食已关闭"
    trackedCount = 0
    for groupId in config.groupOrder:
        if data['tracking'][groupId]:
            trackedCount += 1
    if trackedCount <= 0:
        return "所有营养追踪已关闭"
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


# 百分比反馈统一经过 0-100 限制，命令消息和导出结果保持同一种显示。
def formatDietPercent(value):
    return int(clampDietValue(value) * 100.0)


# 通用设置只改动服务端可信数据，再由服务端同步回填 UI，避免客户端开关状态和实际计算状态分叉。
def applySetting(data, settingKey, value):
    value = bool(value)
    result = {'changed': False, 'message': '', 'color': '§a'}
    if settingKey == config.settingActiveKey:
        if data['active'] == value:
            return result
        data['active'] = value
        result['changed'] = True
        if value:
            result['message'] = "均衡饮食已开启。目标：{}".format(config.settingTargetText)
        else:
            result['message'] = "均衡饮食已关闭。目标：{}".format(config.settingTargetText)
        return result
    for groupId in config.groupOrder:
        if settingKey != config.settingGroupKeys[groupId]:
            continue
        if data['tracking'][groupId] == value:
            return result
        data['tracking'][groupId] = value
        result['changed'] = True
        if value:
            result['message'] = "{}饮食追踪已开启。目标：{}".format(config.groups[groupId]['name'], config.settingTargetText)
        else:
            result['message'] = "{}饮食追踪已关闭。目标：{}".format(config.groups[groupId]['name'], config.settingTargetText)
        return result
    result['color'] = '§c'
    result['message'] = "未知设置项: {}".format(settingKey)
    return result


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
        result['message'] = "均衡饮食数据已重置。目标：{}".format(config.settingTargetText)
        return result
    if action == "pause":
        data['active'] = False
        result['changed'] = True
        result['message'] = "均衡饮食已关闭。目标：{}".format(config.settingTargetText)
        return result
    if action == "resume":
        data['active'] = True
        result['changed'] = True
        result['message'] = "均衡饮食已开启。目标：{}".format(config.settingTargetText)
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
        result['message'] = "{}饮食指数为 {}%。目标：{}".format(config.groups[groupId]['name'], formatDietPercent(data['values'][groupId]), config.settingTargetText)
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
        amountPercent = formatDietPercent(amount)
        if action == "set":
            data['values'][groupId] = clampDietValue(amount)
            result['message'] = "{}饮食指数已设置为 {}%。目标：{}".format(config.groups[groupId]['name'], formatDietPercent(data['values'][groupId]), config.settingTargetText)
        elif action == "add":
            data['values'][groupId] = clampDietValue(data['values'][groupId] + amount)
            result['message'] = "{}饮食指数已提高 {}%。目标：{}".format(config.groups[groupId]['name'], amountPercent, config.settingTargetText)
        else:
            data['values'][groupId] = clampDietValue(data['values'][groupId] - amount)
            result['message'] = "{}饮食指数已降低 {}%。目标：{}".format(config.groups[groupId]['name'], amountPercent, config.settingTargetText)
        result['changed'] = True
        return result
    result['color'] = '§c'
    result['message'] = "用法: /diet open|get|set|add|subtract|reset|pause|resume|export"
    return result


# 导出当前玩家五组百分比，便于测试和服主管理时直接复制日志结果。
def buildExportText(data):
    texts = []
    for groupId in config.groupOrder:
        if data['tracking'][groupId]:
            texts.append("{}:{}%".format(groupId, formatDietPercent(data['values'][groupId])))
        else:
            texts.append("{}:关闭".format(groupId))
    return "Diet[" + ", ".join(texts) + "]"
