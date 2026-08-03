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


# 创建配置化效果的默认开关状态，通用设置和效果刷新共用同一份开关。
def createDefaultEffectSettings():
    effectSettings = {}
    for effectId in config.effectOrder:
        effectSettings[effectId] = config.dietEffects[effectId]['defaultEnabled']
    return effectSettings


# 低值提醒需要比较衰减前后是否跨过阈值，复制当前值可以避免衰减函数额外承担事件语义。
def copyDietValues(data):
    values = {}
    for groupId in config.groupOrder:
        values[groupId] = data['values'][groupId]
    return values


# 从 ModAttr 读取玩家饮食数据，ModAttr 负责跨存档恢复，内存数据只做本次会话的快速缓存。
def loadPlayerData(playerId, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    values = {}
    tracking = {}
    effectSettings = {}
    penaltySettings = {}
    for groupId in config.groupOrder:
        values[groupId] = clampDietValue(compModAttr.GetAttr(config.attrPrefix + groupId, config.groups[groupId]['defaultValue']))
        tracking[groupId] = compModAttr.GetAttr(config.attrPrefix + 'track_' + groupId, True)
    for effectId in config.effectOrder:
        effectSettings[effectId] = compModAttr.GetAttr(config.attrPrefix + 'effect_' + effectId, config.dietEffects[effectId]['defaultEnabled'])
    for penaltyId in config.penaltyOrder:
        penaltySettings[penaltyId] = compModAttr.GetAttr(config.attrPrefix + 'penalty_' + penaltyId, config.dietPenalties[penaltyId]['enabled'])
    deathPenaltyMethod = compModAttr.GetAttr(config.attrPrefix + 'death_penalty_method', config.deathPenaltyMethodDefault)
    if deathPenaltyMethod not in config.deathPenaltyMethodOrder:
        deathPenaltyMethod = config.deathPenaltyMethodDefault
    targetDietValue = clampDietValue(compModAttr.GetAttr(config.attrPrefix + 'target_value', config.targetDietValue))
    if targetDietValue <= 0.0:
        targetDietValue = 0.01
    return {
        'values': values,
        'tracking': tracking,
        'effectSettings': effectSettings,
        'penaltySettings': penaltySettings,
        'targetDietValue': targetDietValue,
        'lowPenaltyEnabled': compModAttr.GetAttr(config.attrPrefix + 'low_penalty_enabled', config.lowPenaltyEnabled),
        'nutritionPenaltyValue': clampDietValue(compModAttr.GetAttr(config.attrPrefix + 'nutrition_penalty_value', config.nutritionPenaltyValue)),
        'nutritionPenaltyWarningOffset': clampDietValue(compModAttr.GetAttr(config.attrPrefix + 'nutrition_penalty_warning_offset', config.nutritionPenaltyWarningOffset)),
        'deathPenaltyMethod': deathPenaltyMethod,
        'deathPenaltyLoss': clampDietValue(compModAttr.GetAttr(config.attrPrefix + 'death_penalty_loss', config.deathPenaltyLoss)),
        'deathPenaltyMin': clampDietValue(compModAttr.GetAttr(config.attrPrefix + 'death_penalty_min', config.deathPenaltyMin)),
        'active': compModAttr.GetAttr(config.attrPrefix + 'active', True),
        'eaten': compModAttr.GetAttr(config.attrPrefix + 'eaten', '')
    }


# 每次进食、衰减、死亡惩罚或命令修改后立即写回，避免退出游戏前数据丢失。
def savePlayerData(playerId, data, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    for groupId in config.groupOrder:
        compModAttr.SetAttr(config.attrPrefix + groupId, data['values'][groupId], needRestore=True)
        compModAttr.SetAttr(config.attrPrefix + 'track_' + groupId, data['tracking'][groupId], needRestore=True)
    for effectId in config.effectOrder:
        compModAttr.SetAttr(config.attrPrefix + 'effect_' + effectId, data['effectSettings'][effectId], needRestore=True)
    for penaltyId in config.penaltyOrder:
        compModAttr.SetAttr(config.attrPrefix + 'penalty_' + penaltyId, data['penaltySettings'][penaltyId], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'target_value', data['targetDietValue'], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'low_penalty_enabled', data['lowPenaltyEnabled'], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'nutrition_penalty_value', data['nutritionPenaltyValue'], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'nutrition_penalty_warning_offset', data['nutritionPenaltyWarningOffset'], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'death_penalty_method', data['deathPenaltyMethod'], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'death_penalty_loss', data['deathPenaltyLoss'], needRestore=True)
    compModAttr.SetAttr(config.attrPrefix + 'death_penalty_min', data['deathPenaltyMin'], needRestore=True)
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
            'icon': groupConfig['icon'],
            'color': groupConfig['color'],
            'value': data['values'][groupId],
            'tracked': data['tracking'][groupId]
        })
    return {
        'active': data['active'],
        'groups': groupList
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
    values[config.settingTargetValueKey] = formatDietPercent(data['targetDietValue'])
    for effectId in config.effectOrder:
        values[config.dietEffects[effectId]['settingKey']] = data['effectSettings'][effectId]
    values[config.settingLowPenaltyEnabledKey] = data['lowPenaltyEnabled']
    values[config.settingNutritionPenaltyValueKey] = formatDietPercent(data['nutritionPenaltyValue'])
    values[config.settingNutritionPenaltyWarningOffsetKey] = formatDietPercent(data['nutritionPenaltyWarningOffset'])
    for penaltyId in config.penaltyOrder:
        values[config.dietPenalties[penaltyId]['settingKey']] = data['penaltySettings'][penaltyId]
    values[config.settingDeathPenaltyMethodKey] = config.deathPenaltyMethodNames[data['deathPenaltyMethod']]
    values[config.settingDeathPenaltyLossKey] = formatDietPercent(data['deathPenaltyLoss'])
    values[config.settingDeathPenaltyMinKey] = formatDietPercent(data['deathPenaltyMin'])
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


# 记录玩家已经吃过的食物，保留存档中的饮食历史供后续玩法复用。
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
        return {}
    trackedFoodGroupIds = []
    for groupId in foodGroupIds:
        if data['tracking'][groupId]:
            trackedFoodGroupIds.append(groupId)
    if not trackedFoodGroupIds:
        return {}
    gainValues = calculateGain(hunger, nutrition, trackedFoodGroupIds)
    for groupId in trackedFoodGroupIds:
        data['values'][groupId] = clampDietValue(data['values'][groupId] + gainValues[groupId])
    addEatenFood(data, itemName)
    return gainValues


# 复刻 PlayerDietTracker.decay：饥饿条下降时，所有已有值按 exp(value) 曲线共同衰减。
def applyHungerDecay(data, foodDiff):
    activeCount = 0
    for groupId in config.groupOrder:
        if data['tracking'][groupId] and data['values'][groupId] > 0.0:
            activeCount += 1
    if activeCount <= 0:
        return False
    scale = float(foodDiff) / float(activeCount)
    scale *= (1.0 - config.decayPenaltyPerGroup / 100.0) ** (activeCount - 1)
    changed = False
    for groupId in config.groupOrder:
        if not data['tracking'][groupId]:
            continue
        value = data['values'][groupId]
        decay = (config.expBase ** value) * scale * config.groups[groupId]['decayMultiplier'] / 100.0
        if decay > 0.0:
            data['values'][groupId] = clampDietValue(value - decay)
            changed = True
    return changed


# 死亡惩罚按玩家设置选择固定扣除、比例扣除或重置，默认值等价于上游 AMOUNT 扣除 100%。
def applyDeathPenalty(data):
    for groupId in config.groupOrder:
        if not data['tracking'][groupId]:
            continue
        originalValue = data['values'][groupId]
        if data['deathPenaltyMethod'] == config.deathPenaltyMethodReset:
            value = config.groups[groupId]['defaultValue']
        elif data['deathPenaltyMethod'] == config.deathPenaltyMethodPercent:
            value = originalValue * (1.0 - data['deathPenaltyLoss'])
        else:
            value = originalValue - data['deathPenaltyLoss']
        if data['deathPenaltyMethod'] != config.deathPenaltyMethodReset:
            if value < data['deathPenaltyMin']:
                value = data['deathPenaltyMin']
            if value > originalValue:
                value = originalValue
        data['values'][groupId] = clampDietValue(value)


# 判断单个数值是否落在效果条件区间内，配置化效果的多种匹配模式都复用这个边界判断。
def isDietValueInCondition(value, above, below):
    return value >= above and value <= below


# 计算单条效果条件的命中数量，支持 Java Diet 的 all、every、any、average、none 五种匹配语义。
def getConditionMatchCount(data, condition):
    above = condition['above']
    if condition['useTarget']:
        above = data['targetDietValue']
    below = condition['below']
    if condition['usePenaltyThreshold']:
        below = data['nutritionPenaltyValue']
    if condition['match'] == 'all':
        for groupId in condition['groups']:
            if not data['tracking'][groupId] or not isDietValueInCondition(data['values'][groupId], above, below):
                return 0
        return 1
    if condition['match'] == 'every':
        count = 0
        for groupId in condition['groups']:
            if data['tracking'][groupId] and isDietValueInCondition(data['values'][groupId], above, below):
                count += 1
        return count
    if condition['match'] == 'any':
        for groupId in condition['groups']:
            if data['tracking'][groupId] and isDietValueInCondition(data['values'][groupId], above, below):
                return 1
        return 0
    if condition['match'] == 'average':
        totalValue = 0.0
        for groupId in condition['groups']:
            if not data['tracking'][groupId]:
                return 0
            totalValue += data['values'][groupId]
        averageValue = totalValue / float(len(condition['groups']))
        if isDietValueInCondition(averageValue, above, below):
            return 1
        return 0
    if condition['match'] == 'none':
        for groupId in condition['groups']:
            if data['tracking'][groupId] and isDietValueInCondition(data['values'][groupId], above, below):
                return 0
        return 1
    return 0


# 多条件效果需要全部命中；every 条件的命中数量会作为后续效果强度增量。
def getEffectMatchMultiplier(data, effectConfig):
    multiplier = 0
    for condition in effectConfig['conditions']:
        matches = getConditionMatchCount(data, condition)
        if matches < condition['minMatches']:
            return 0
        if condition['match'] == 'every':
            multiplier += matches
    if multiplier <= 0:
        multiplier = 1
    return multiplier


# 判断当前数值命中的配置化饮食效果，服务端施加效果和 UI 文案共用同一套条件。
def getMatchedEffects(data):
    matched = []
    for effectId in config.effectOrder:
        if not data['effectSettings'][effectId]:
            continue
        multiplier = getEffectMatchMultiplier(data, config.dietEffects[effectId])
        if multiplier > 0:
            matched.append({
                'id': effectId,
                'kind': 'effect',
                'multiplier': multiplier
            })
    return matched


# 低值惩罚从玩家通用设置读取，服务端判定、UI 文案和提醒保持同一份真值。
def getMatchedPenalties(data):
    matched = []
    if not data['lowPenaltyEnabled']:
        return matched
    for penaltyId in config.penaltyOrder:
        penaltyConfig = config.dietPenalties[penaltyId]
        if not data['penaltySettings'][penaltyId]:
            continue
        multiplier = getEffectMatchMultiplier(data, penaltyConfig)
        if multiplier > 0:
            matched.append({
                'id': penaltyId,
                'kind': 'penalty',
                'multiplier': multiplier
            })
    return matched


# 奖励和低值惩罚共用同一套刷新周期，避免同一 tick 内状态效果分两套逻辑互相覆盖。
def getMatchedDietResults(data, diseaseActive=False, pauseSugarRush=False):
    matched = []
    for effectResult in getMatchedEffects(data):
        if pauseSugarRush and effectResult['id'] == 'sugarRush':
            continue
        matched.append(effectResult)
    # 疾病已经承担饮食失衡反馈，患病期间暂停普通低营养状态，避免两套惩罚叠加。
    if diseaseActive:
        return matched
    for penaltyResult in getMatchedPenalties(data):
        matched.append(penaltyResult)
    return matched


# 按服务端 Tick 间隔刷新短时状态效果，持续时间需要略长于刷新周期，避免效果闪断。
def applyEffects(playerId, data, compFactory, diseaseActive=False, pauseSugarRush=False):
    matched = getMatchedDietResults(data, diseaseActive, pauseSugarRush)
    if not matched:
        return matched
    compEffect = compFactory.CreateEffect(playerId)
    for effectResult in matched:
        if effectResult['kind'] == 'penalty':
            effectConfig = config.dietPenalties[effectResult['id']]
        else:
            effectConfig = config.dietEffects[effectResult['id']]
        for statusEffect in effectConfig['statusEffects']:
            amplifier = statusEffect['amplifier'] + (effectResult['multiplier'] - 1) * statusEffect['increment']
            compEffect.AddEffectToEntity(statusEffect['name'], statusEffect['duration'], amplifier, True)
    return matched


# 负面效果刷新时只播报低值营养类别，避免百分比和食物举例占用过多聊天区域。
def buildLowPenaltyEffectMessage(data, matchedResults):
    penaltyApplied = False
    for effectResult in matchedResults:
        if effectResult['kind'] == 'penalty':
            penaltyApplied = True
    if not penaltyApplied:
        return ""

    lowGroupNames = []
    for groupId in config.essentialGroupOrder:
        if not data['tracking'][groupId] or data['values'][groupId] > data['nutritionPenaltyValue']:
            continue
        lowGroupNames.append(config.groups[groupId]['name'])
    return "营养不足，请及时补充{}。".format("、".join(lowGroupNames))


# 百分比反馈统一经过 0-100 限制，命令消息和导出结果保持同一种显示。
def formatDietPercent(value):
    return int(clampDietValue(value) * 100.0)


# 进食增量和当前值使用同一套百分比口径，很小但有效的补充至少显示 +1%。
def formatDietGainPercent(value):
    percent = int(clampDietValue(value) * 100.0)
    if percent <= 0 and value > 0.0:
        return 1
    return percent


# 低值提前提醒线随玩家设置移动，避免通用设置改动后提示还停在旧阈值。
def getNutritionPenaltyWarningValue(data):
    return clampDietValue(data['nutritionPenaltyValue'] + data['nutritionPenaltyWarningOffset'])


# 低值提醒跟随低值惩罚开关，避免关闭惩罚后仍提示玩家担心处罚。
def isLowPenaltyAlertEnabled(data):
    if not data['lowPenaltyEnabled']:
        return False
    for penaltyId in config.penaltyOrder:
        if data['penaltySettings'][penaltyId]:
            return True
    return False


# 低值提醒文案统一区分“接近惩罚”和“已经低于惩罚”，进食反馈和衰减跨线提示共用。
def buildNutritionPenaltyWarningText(data, groupId, value):
    groupConfig = config.groups[groupId]
    thresholdPercent = formatDietPercent(data['nutritionPenaltyValue'])
    currentPercent = formatDietPercent(value)
    if value <= data['nutritionPenaltyValue']:
        return "{}营养值已低于低值惩罚阈值 {}%，当前 {}%。建议补充：{}".format(groupConfig['name'], thresholdPercent, currentPercent, groupConfig['suggestion'])
    return "{}营养值接近低值惩罚阈值 {}%，当前 {}%。建议补充：{}".format(groupConfig['name'], thresholdPercent, currentPercent, groupConfig['suggestion'])


# 进食反馈只基于本次真实增量和保存前的最新数据生成，避免继续显示物品 id 这种调试文案。
def buildFoodGainMessages(data, gainValues):
    gainTexts = []
    for groupId in config.groupOrder:
        if groupId not in gainValues:
            continue
        groupName = config.groups[groupId]['name']
        currentValue = data['values'][groupId]
        currentPercent = formatDietPercent(currentValue)
        text = "{}营养值 +{}%，当前 {}%".format(groupName, formatDietGainPercent(gainValues[groupId]), currentPercent)
        missingValue = data['targetDietValue'] - currentValue
        if missingValue > 0.0:
            missingPercent = formatDietPercent(data['targetDietValue']) - currentPercent
            text += "，距目标还差 {}%".format(missingPercent)
        gainTexts.append(text)

    warningGroupId = ""
    warningValue = 1.1
    penaltyWarningValue = getNutritionPenaltyWarningValue(data)
    if isLowPenaltyAlertEnabled(data):
        for groupId in config.essentialGroupOrder:
            if groupId in gainValues:
                continue
            if not data['tracking'][groupId]:
                continue
            value = data['values'][groupId]
            if value <= penaltyWarningValue and value < warningValue:
                warningGroupId = groupId
                warningValue = value

    result = {
        'gainMessage': "；".join(gainTexts),
        'warningMessage': ''
    }
    if warningGroupId:
        result['warningMessage'] = "提醒：" + buildNutritionPenaltyWarningText(data, warningGroupId, warningValue)
    return result


# 只在营养值跨过高值奖励线或低值提前提醒线时提示一次；补回线以上后，下次跌破才会再次触发。
def buildNutritionAlertMessages(beforeValues, data):
    messages = []
    beforeData = {
        'values': beforeValues,
        'tracking': data['tracking'],
        'effectSettings': data['effectSettings'],
        'targetDietValue': data['targetDietValue']
    }
    afterEffectIds = []
    for effectResult in getMatchedEffects(data):
        afterEffectIds.append(effectResult['id'])
    for effectResult in getMatchedEffects(beforeData):
        effectId = effectResult['id']
        if effectId in afterEffectIds:
            continue
        effectConfig = config.dietEffects[effectId]
        loweredGroups = []
        for condition in effectConfig['conditions']:
            if not condition['useTarget']:
                continue
            for groupId in condition['groups']:
                if not data['tracking'][groupId]:
                    continue
                beforeValue = beforeValues[groupId]
                value = data['values'][groupId]
                if beforeValue >= data['targetDietValue'] and value < data['targetDietValue']:
                    groupConfig = config.groups[groupId]
                    loweredGroups.append("{}营养值当前 {}%".format(groupConfig['name'], formatDietPercent(value)))
        if loweredGroups:
            messages.append("已失去{}：{}，低于目标营养值 {}%。".format(effectConfig['name'], "、".join(loweredGroups), formatDietPercent(data['targetDietValue'])))

    if isLowPenaltyAlertEnabled(data):
        penaltyWarningValue = getNutritionPenaltyWarningValue(data)
        for groupId in config.essentialGroupOrder:
            if not data['tracking'][groupId]:
                continue
            beforeValue = beforeValues[groupId]
            value = data['values'][groupId]
            if beforeValue > penaltyWarningValue and value <= penaltyWarningValue:
                messages.append(buildNutritionPenaltyWarningText(data, groupId, value))
    return messages


# 通用设置开关可能来自不同引擎版本的回调，服务端统一转换后再写入玩家数据。
def parseSettingToggle(value):
    if value == False or value == 0 or value == "False" or value == "false" or value == "0":
        return False
    return True


# 通用设置滑块是客户端输入边界，解析失败时返回负值交给调用点输出明确错误。
def parseSettingSliderPercent(value):
    try:
        percent = int(value)
    except (TypeError, ValueError):
        return -1.0
    if percent < 0:
        percent = 0
    if percent > 100:
        percent = 100
    return float(percent) / 100.0


# 死亡惩罚下拉框使用中文选项展示，服务端保存稳定的内部方法名。
def parseDeathPenaltyMethodSetting(value):
    for deathPenaltyMethod in config.deathPenaltyMethodOrder:
        if value == deathPenaltyMethod or value == config.deathPenaltyMethodNames[deathPenaltyMethod]:
            return deathPenaltyMethod
    return ""


# 通用设置只改动服务端可信数据，再由服务端同步回填 UI，避免客户端开关状态和实际计算状态分叉。
def applySetting(data, settingKey, value):
    result = {'changed': False, 'message': '', 'color': '§a'}
    if settingKey == config.settingActiveKey:
        toggleValue = parseSettingToggle(value)
        if data['active'] == toggleValue:
            return result
        data['active'] = toggleValue
        result['changed'] = True
        if toggleValue:
            result['message'] = "均衡饮食已开启。目标：{}".format(config.settingTargetText)
        else:
            result['message'] = "均衡饮食已关闭。目标：{}".format(config.settingTargetText)
        return result
    for groupId in config.groupOrder:
        if settingKey != config.settingGroupKeys[groupId]:
            continue
        toggleValue = parseSettingToggle(value)
        if data['tracking'][groupId] == toggleValue:
            return result
        data['tracking'][groupId] = toggleValue
        result['changed'] = True
        if toggleValue:
            result['message'] = "{}饮食追踪已开启。目标：{}".format(config.groups[groupId]['name'], config.settingTargetText)
        else:
            result['message'] = "{}饮食追踪已关闭。目标：{}".format(config.groups[groupId]['name'], config.settingTargetText)
        return result
    if settingKey == config.settingTargetValueKey:
        amount = parseSettingSliderPercent(value)
        if amount < 0.0:
            result['color'] = '§c'
            result['message'] = "目标营养值必须是 0-100 的数字"
            return result
        if amount <= 0.0:
            amount = 0.01
        if data['targetDietValue'] == amount:
            return result
        data['targetDietValue'] = amount
        result['changed'] = True
        result['message'] = "目标营养值已设置为 {}%。".format(formatDietPercent(data['targetDietValue']))
        return result
    for effectId in config.effectOrder:
        if settingKey != config.dietEffects[effectId]['settingKey']:
            continue
        toggleValue = parseSettingToggle(value)
        if data['effectSettings'][effectId] == toggleValue:
            return result
        data['effectSettings'][effectId] = toggleValue
        result['changed'] = True
        if toggleValue:
            result['message'] = "{}已启用。".format(config.dietEffects[effectId]['name'])
        else:
            result['message'] = "{}已关闭。".format(config.dietEffects[effectId]['name'])
        return result
    if settingKey == config.settingLowPenaltyEnabledKey:
        toggleValue = parseSettingToggle(value)
        if data['lowPenaltyEnabled'] == toggleValue:
            return result
        data['lowPenaltyEnabled'] = toggleValue
        result['changed'] = True
        if toggleValue:
            result['message'] = "低值惩罚已启用。"
        else:
            result['message'] = "低值惩罚已关闭。"
        return result
    if settingKey == config.settingNutritionPenaltyValueKey:
        amount = parseSettingSliderPercent(value)
        if amount < 0.0:
            result['color'] = '§c'
            result['message'] = "低值惩罚阈值必须是 0-100 的数字"
            return result
        if data['nutritionPenaltyValue'] == amount:
            return result
        data['nutritionPenaltyValue'] = amount
        result['changed'] = True
        result['message'] = "低值惩罚阈值已设置为 {}%。".format(formatDietPercent(data['nutritionPenaltyValue']))
        return result
    if settingKey == config.settingNutritionPenaltyWarningOffsetKey:
        amount = parseSettingSliderPercent(value)
        if amount < 0.0:
            result['color'] = '§c'
            result['message'] = "低值提醒提前量必须是 0-100 的数字"
            return result
        if data['nutritionPenaltyWarningOffset'] == amount:
            return result
        data['nutritionPenaltyWarningOffset'] = amount
        result['changed'] = True
        result['message'] = "低值提醒提前量已设置为 {}%。".format(formatDietPercent(data['nutritionPenaltyWarningOffset']))
        return result
    for penaltyId in config.penaltyOrder:
        if settingKey != config.dietPenalties[penaltyId]['settingKey']:
            continue
        toggleValue = parseSettingToggle(value)
        if data['penaltySettings'][penaltyId] == toggleValue:
            return result
        data['penaltySettings'][penaltyId] = toggleValue
        result['changed'] = True
        if toggleValue:
            result['message'] = "{}已启用。".format(config.dietPenalties[penaltyId]['name'])
        else:
            result['message'] = "{}已关闭。".format(config.dietPenalties[penaltyId]['name'])
        return result
    if settingKey == config.settingDeathPenaltyMethodKey:
        deathPenaltyMethod = parseDeathPenaltyMethodSetting(value)
        if not deathPenaltyMethod:
            result['color'] = '§c'
            result['message'] = "未知死亡惩罚方式: {}".format(value)
            return result
        if data['deathPenaltyMethod'] == deathPenaltyMethod:
            return result
        data['deathPenaltyMethod'] = deathPenaltyMethod
        result['changed'] = True
        result['message'] = "死亡惩罚方式已设置为{}。".format(config.deathPenaltyMethodNames[deathPenaltyMethod])
        return result
    if settingKey == config.settingDeathPenaltyLossKey:
        amount = parseSettingSliderPercent(value)
        if amount < 0.0:
            result['color'] = '§c'
            result['message'] = "死亡扣除比例必须是 0-100 的数字"
            return result
        if data['deathPenaltyLoss'] == amount:
            return result
        data['deathPenaltyLoss'] = amount
        result['changed'] = True
        result['message'] = "死亡扣除比例已设置为 {}%。".format(formatDietPercent(data['deathPenaltyLoss']))
        return result
    if settingKey == config.settingDeathPenaltyMinKey:
        amount = parseSettingSliderPercent(value)
        if amount < 0.0:
            result['color'] = '§c'
            result['message'] = "死亡最低保留必须是 0-100 的数字"
            return result
        if data['deathPenaltyMin'] == amount:
            return result
        data['deathPenaltyMin'] = amount
        result['changed'] = True
        result['message'] = "死亡最低保留已设置为 {}%。".format(formatDietPercent(data['deathPenaltyMin']))
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
        if amount != amount or amount == float("inf") or amount == -float("inf"):
            result['color'] = '§c'
            result['message'] = "数值必须是有限数字"
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
