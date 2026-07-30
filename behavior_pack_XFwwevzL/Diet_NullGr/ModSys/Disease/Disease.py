# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.Disease.config as config


# 创建完整疾病状态，新增疾病字段时只需同步配置和此处即可覆盖新玩家默认数据。
def createDefaultData():
    progress = {}
    activeSeconds = {}
    protectionSeconds = {}
    recoveryProgress = {}
    for diseaseId in config.diseaseOrder:
        progress[diseaseId] = 0.0
        activeSeconds[diseaseId] = 0
        protectionSeconds[diseaseId] = 0
        recoveryProgress[diseaseId] = 0.0
    return {
        'enabled': config.defaultEnabled,
        'validEatCount': 0,
        'progress': progress,
        'active': [],
        'activeSeconds': activeSeconds,
        'protectionSeconds': protectionSeconds,
        'recoveryProgress': recoveryProgress,
        'constipationSquatCount': 0
    }


# 总开关关闭时清空所有疾病、候选与保护状态；有效进食计数保留，重新开启后无需重复度过新手保护。
def clearAllDiseaseState(data):
    active = list(data['active'])
    data['active'] = []
    for diseaseId in config.diseaseOrder:
        data['progress'][diseaseId] = 0.0
        data['activeSeconds'][diseaseId] = 0
        data['protectionSeconds'][diseaseId] = 0
        data['recoveryProgress'][diseaseId] = 0.0
    data['constipationSquatCount'] = 0
    return active


# 从分字段 ModAttr 恢复疾病状态，并清理无效或重复的确诊标识。
def loadPlayerData(playerId, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    data = createDefaultData()
    data['enabled'] = bool(compModAttr.GetAttr(config.attrEnabled, config.defaultEnabled))
    data['validEatCount'] = int(compModAttr.GetAttr(config.attrValidEatCount, 0))
    if data['validEatCount'] < 0:
        data['validEatCount'] = 0
    activeText = compModAttr.GetAttr(config.attrActive, '')
    if activeText:
        for diseaseId in activeText.split(';'):
            if diseaseId not in config.diseases or diseaseId in data['active']:
                continue
            if diseaseId in config.bloodSugarConflict and config.bloodSugarConflict[diseaseId] in data['active']:
                continue
            data['active'].append(diseaseId)
            if len(data['active']) >= config.maxActiveCount:
                break
    for diseaseId in config.diseaseOrder:
        diseaseConfig = config.diseases[diseaseId]
        progress = float(compModAttr.GetAttr(config.attrProgressPrefix + diseaseId, 0.0))
        if progress < 0.0:
            progress = 0.0
        if progress > diseaseConfig['triggerPoints']:
            progress = diseaseConfig['triggerPoints']
        data['progress'][diseaseId] = progress
        data['activeSeconds'][diseaseId] = max(0, int(compModAttr.GetAttr(config.attrActiveSecondsPrefix + diseaseId, 0)))
        data['protectionSeconds'][diseaseId] = max(0, int(compModAttr.GetAttr(config.attrProtectionSecondsPrefix + diseaseId, 0)))
        data['recoveryProgress'][diseaseId] = max(0.0, float(compModAttr.GetAttr(config.attrRecoveryProgressPrefix + diseaseId, 0.0)))
        if diseaseId in data['active']:
            data['progress'][diseaseId] = 0.0
            data['protectionSeconds'][diseaseId] = 0
        else:
            data['activeSeconds'][diseaseId] = 0
            data['recoveryProgress'][diseaseId] = 0.0
            if data['protectionSeconds'][diseaseId] > 0:
                data['progress'][diseaseId] = 0.0
            elif len(data['active']) >= config.maxActiveCount:
                halfProgress = diseaseConfig['triggerPoints'] * config.fullSlotProgressRatio
                if data['progress'][diseaseId] > halfProgress:
                    data['progress'][diseaseId] = halfProgress
    squatCount = int(compModAttr.GetAttr(config.attrConstipationSquatCount, 0))
    data['constipationSquatCount'] = min(config.constipationSquatRequired, max(0, squatCount))
    if 'constipation' not in data['active']:
        data['constipationSquatCount'] = 0
    if not data['enabled']:
        clearAllDiseaseState(data)
    return data


# 疾病状态分字段写入 ModAttr，避免单个复合对象在版本迁移时难以兼容。
def savePlayerData(playerId, data, compFactory):
    compModAttr = compFactory.CreateModAttr(playerId)
    compModAttr.SetAttr(config.attrEnabled, data['enabled'], needRestore=True)
    compModAttr.SetAttr(config.attrValidEatCount, data['validEatCount'], needRestore=True)
    compModAttr.SetAttr(config.attrActive, ';'.join(data['active']), needRestore=True)
    compModAttr.SetAttr(config.attrConstipationSquatCount, data['constipationSquatCount'], needRestore=True)
    for diseaseId in config.diseaseOrder:
        compModAttr.SetAttr(config.attrProgressPrefix + diseaseId, data['progress'][diseaseId], needRestore=True)
        compModAttr.SetAttr(config.attrActiveSecondsPrefix + diseaseId, data['activeSeconds'][diseaseId], needRestore=True)
        compModAttr.SetAttr(config.attrProtectionSecondsPrefix + diseaseId, data['protectionSeconds'][diseaseId], needRestore=True)
        compModAttr.SetAttr(config.attrRecoveryProgressPrefix + diseaseId, data['recoveryProgress'][diseaseId], needRestore=True)


# 将现有 Diet 与 Thirst 真值转换成疾病条件使用的统一快照，所有阈值继续保持 0.0-1.0。
def buildNutritionSnapshot(dietData, thirstData):
    return {
        'values': {
            'fruits': dietData['values']['fruits'],
            'grains': dietData['values']['grains'],
            'proteins': dietData['values']['proteins'],
            'vegetables': dietData['values']['vegetables'],
            'sugars': dietData['values']['sugars'],
            'thirst': thirstData['value'] / config.thirstMaxValue
        },
        'tracking': {
            'fruits': dietData['active'] and dietData['tracking']['fruits'],
            'grains': dietData['active'] and dietData['tracking']['grains'],
            'proteins': dietData['active'] and dietData['tracking']['proteins'],
            'vegetables': dietData['active'] and dietData['tracking']['vegetables'],
            'sugars': dietData['active'] and dietData['tracking']['sugars']
        },
        'thirstEnabled': thirstData['enabled']
    }


# 只有疾病涉及的全部必需营养组仍在追踪时才允许判定，含口渴条件的疾病还要求口渴系统开启。
def isDiseaseAvailable(diseaseId, snapshot):
    diseaseConfig = config.diseases[diseaseId]
    for groupId in diseaseConfig['requiredGroups']:
        if not snapshot['tracking'][groupId]:
            return False
    if diseaseConfig['requiresThirst'] and not snapshot['thirstEnabled']:
        return False
    return True


# 计算疾病本次代谢应增加的进度倍率，零表示当前条件不成立。
def getTriggerMultiplier(diseaseId, snapshot):
    if not isDiseaseAvailable(diseaseId, snapshot):
        return 0.0
    values = snapshot['values']
    fruits = values['fruits']
    grains = values['grains']
    proteins = values['proteins']
    vegetables = values['vegetables']
    sugars = values['sugars']
    thirst = values['thirst']
    if diseaseId == 'hypoglycemia':
        return 1.0 if grains <= 0.15 and fruits <= 0.20 and sugars <= 0.20 else 0.0
    if diseaseId == 'hyperglycemia':
        nonSugarAverage = (fruits + grains + proteins + vegetables) / 4.0
        return 1.0 if sugars >= 0.80 and sugars - nonSugarAverage >= 0.35 else 0.0
    if diseaseId == 'constipation':
        lowFiberCount = 0
        for value in (fruits, grains, vegetables):
            if value <= 0.25:
                lowFiberCount += 1
        if thirst <= 0.35 and lowFiberCount >= 2:
            return 1.0
        if fruits <= 0.15 and grains <= 0.15 and vegetables <= 0.15:
            return 0.5
        return 0.0
    if diseaseId == 'rickets':
        normalCount = 0
        for value in (fruits, grains, vegetables):
            if value >= 0.35:
                normalCount += 1
        return 1.0 if proteins <= 0.15 and normalCount >= 2 else 0.0
    if diseaseId == 'fever':
        criticalCount = 0
        for value in (fruits, grains, proteins, vegetables):
            if value <= 0.15:
                criticalCount += 1
        return 1.0 if thirst <= 0.25 and criticalCount >= 3 else 0.0
    if diseaseId == 'mouth_ulcer':
        if grains > 0.20 or proteins > 0.20:
            return 0.0
        if snapshot['tracking']['sugars'] and sugars >= 0.60:
            return 2.0
        return 1.0
    if diseaseId == 'scurvy':
        return 1.0 if fruits <= 0.10 and vegetables <= 0.15 and (grains >= 0.35 or proteins >= 0.35) else 0.0
    return 0.0


# 饮食恢复条件与触发表共用同一份可见营养快照，追踪关闭时直接视为该疾病可安全清除。
def isRecoveryConditionMet(diseaseId, snapshot):
    if not isDiseaseAvailable(diseaseId, snapshot):
        return True
    values = snapshot['values']
    fruits = values['fruits']
    grains = values['grains']
    proteins = values['proteins']
    vegetables = values['vegetables']
    sugars = values['sugars']
    thirst = values['thirst']
    if diseaseId == 'hypoglycemia':
        return grains >= 0.35 or fruits >= 0.35 or sugars >= 0.35
    if diseaseId == 'hyperglycemia':
        normalCount = 0
        for value in (fruits, grains, proteins, vegetables):
            if value >= 0.35:
                normalCount += 1
        return sugars <= 0.55 and normalCount >= 2
    if diseaseId == 'constipation':
        recoveredCount = 0
        for value in (fruits, grains, vegetables):
            if value >= 0.35:
                recoveredCount += 1
        return thirst >= 0.50 and recoveredCount >= 2
    if diseaseId == 'rickets':
        return proteins >= 0.45
    if diseaseId == 'fever':
        normalCount = 0
        for value in (fruits, grains, proteins, vegetables):
            if value >= 0.30:
                normalCount += 1
        return thirst >= 0.50 and normalCount >= 3
    if diseaseId == 'mouth_ulcer':
        return (grains >= 0.40 and proteins >= 0.30) or (proteins >= 0.40 and grains >= 0.30)
    if diseaseId == 'scurvy':
        return fruits >= 0.40 or vegetables >= 0.45
    return False


# 确诊只占用空闲槽位；低血糖与高血糖不能并存，并在确诊时清掉对方候选进度。
def diagnoseDisease(data, diseaseId):
    if not data['enabled']:
        return False
    if diseaseId not in config.diseases or diseaseId in data['active']:
        return False
    if len(data['active']) >= config.maxActiveCount or data['protectionSeconds'][diseaseId] > 0:
        return False
    if diseaseId in config.bloodSugarConflict:
        conflictId = config.bloodSugarConflict[diseaseId]
        data['progress'][conflictId] = 0.0
        if conflictId in data['active']:
            return False
    data['active'].append(diseaseId)
    data['progress'][diseaseId] = 0.0
    data['activeSeconds'][diseaseId] = 0
    data['recoveryProgress'][diseaseId] = 0.0
    if diseaseId == 'constipation':
        data['constipationSquatCount'] = 0
    return True


# 痊愈会清理本轮状态并开启该疾病自己的保护期，不影响另一个疾病槽位。
def cureDisease(data, diseaseId, useProtection=True):
    if diseaseId not in data['active']:
        return False
    data['active'].remove(diseaseId)
    data['progress'][diseaseId] = 0.0
    data['activeSeconds'][diseaseId] = 0
    data['recoveryProgress'][diseaseId] = 0.0
    if useProtection:
        data['protectionSeconds'][diseaseId] = config.diseases[diseaseId]['protectionSeconds']
        if diseaseId in config.bloodSugarConflict:
            conflictId = config.bloodSugarConflict[diseaseId]
            data['protectionSeconds'][conflictId] = max(
                data['protectionSeconds'][conflictId],
                config.bloodSugarConversionProtectionSeconds
            )
    if diseaseId == 'constipation':
        data['constipationSquatCount'] = 0
    return True


# 对所有已患疾病结算饮食恢复；佝偻病必须连续保持三个代谢点，其余疾病达标即清除。
def applyNutritionRecovery(data, metabolicPoints, snapshot):
    cured = []
    for diseaseId in list(data['active']):
        if not isRecoveryConditionMet(diseaseId, snapshot):
            data['recoveryProgress'][diseaseId] = 0.0
            continue
        requiredPoints = config.diseases[diseaseId]['recoveryMetabolicPoints']
        if requiredPoints > 0.0:
            data['recoveryProgress'][diseaseId] += metabolicPoints
            if data['recoveryProgress'][diseaseId] < requiredPoints:
                continue
        if cureDisease(data, diseaseId):
            cured.append(diseaseId)
    return cured


# 只有真正提供了饮食分类收益的进食才调用此函数，并立即检查可由进食缓解的疾病。
def recordValidEat(data, snapshot):
    data['validEatCount'] += 1
    return applyNutritionRecovery(data, 0.0, snapshot)


# 每个有效代谢点同时推进触发、恢复与快速回退，双槽占满时候选进度最多保留一半。
def advanceMetabolism(data, metabolicPoints, snapshot):
    result = {
        'diagnosed': [],
        'cured': []
    }
    if metabolicPoints <= 0.0:
        return result
    result['cured'] = applyNutritionRecovery(data, metabolicPoints, snapshot)
    if data['validEatCount'] < config.minimumValidEatCount:
        for diseaseId in config.diseaseOrder:
            data['progress'][diseaseId] = 0.0
        return result
    for diseaseId in config.diseaseOrder:
        if diseaseId in data['active']:
            data['progress'][diseaseId] = 0.0
            continue
        if diseaseId in config.bloodSugarConflict and config.bloodSugarConflict[diseaseId] in data['active']:
            data['progress'][diseaseId] = 0.0
            continue
        if data['protectionSeconds'][diseaseId] > 0 or not isDiseaseAvailable(diseaseId, snapshot):
            data['progress'][diseaseId] = 0.0
            continue
        multiplier = getTriggerMultiplier(diseaseId, snapshot)
        if multiplier > 0.0:
            data['progress'][diseaseId] += metabolicPoints * multiplier
        else:
            data['progress'][diseaseId] -= metabolicPoints * config.progressFallbackMultiplier
            if data['progress'][diseaseId] < 0.0:
                data['progress'][diseaseId] = 0.0
        if len(data['active']) >= config.maxActiveCount:
            halfProgress = config.diseases[diseaseId]['triggerPoints'] * config.fullSlotProgressRatio
            if data['progress'][diseaseId] > halfProgress:
                data['progress'][diseaseId] = halfProgress
    for diseaseId in config.diagnosisOrder:
        if len(data['active']) >= config.maxActiveCount:
            break
        if data['progress'][diseaseId] < config.diseases[diseaseId]['triggerPoints']:
            continue
        if diagnoseDisease(data, diseaseId):
            result['diagnosed'].append(diseaseId)
    if len(data['active']) >= config.maxActiveCount:
        for diseaseId in config.diseaseOrder:
            if diseaseId in data['active']:
                continue
            halfProgress = config.diseases[diseaseId]['triggerPoints'] * config.fullSlotProgressRatio
            if data['progress'][diseaseId] > halfProgress:
                data['progress'][diseaseId] = halfProgress
    return result


# 逐秒推进保护与患病时长，超过最长持续时间时自动痊愈，防止疾病演变为慢性负担。
def advanceSeconds(data, seconds):
    cured = []
    if seconds <= 0:
        return cured
    for diseaseId in config.diseaseOrder:
        remaining = data['protectionSeconds'][diseaseId] - seconds
        data['protectionSeconds'][diseaseId] = max(0, remaining)
    for diseaseId in list(data['active']):
        data['activeSeconds'][diseaseId] += seconds
        if data['activeSeconds'][diseaseId] < config.diseases[diseaseId]['maxActiveSeconds']:
            continue
        if cureDisease(data, diseaseId):
            cured.append(diseaseId)
    return cured


# 有效下蹲由服务端事件层完成地面、时长和姿态校验，数据层只累计便秘缓解次数。
def recordConstipationSquat(data):
    if 'constipation' not in data['active']:
        return False
    data['constipationSquatCount'] += 1
    if data['constipationSquatCount'] < config.constipationSquatRequired:
        return False
    return cureDisease(data, 'constipation')


# 死亡会清除当前疾病和全部候选进度，并保留已患疾病的保护期避免重生后立即复发。
def resetAfterDeath(data):
    active = list(data['active'])
    for diseaseId in active:
        cureDisease(data, diseaseId)
    for diseaseId in config.diseaseOrder:
        data['progress'][diseaseId] = 0.0
        data['recoveryProgress'][diseaseId] = 0.0
    data['constipationSquatCount'] = 0
    return active


# 秒数格式统一为分:秒，疾病界面无需自行处理补零与最长时长。
def formatDuration(seconds):
    minutes = int(seconds) // 60
    remainingSeconds = int(seconds) % 60
    return "{}:{:02d}".format(minutes, remainingSeconds)


# 将服务端疾病状态压成客户端列表，每行字段固定，避免 UI 读取存档结构。
def buildClientData(data):
    activeRows = []
    for diseaseId in data['active']:
        diseaseConfig = config.diseases[diseaseId]
        if diseaseId == 'constipation':
            progressText = "下蹲缓解：{}/{}".format(data['constipationSquatCount'], config.constipationSquatRequired)
        elif diseaseId == 'rickets':
            progressText = "恢复保持：{}/{} 代谢点".format(
                int(data['recoveryProgress'][diseaseId]),
                int(diseaseConfig['recoveryMetabolicPoints'])
            )
        else:
            progressText = "恢复进度：等待饮食达标"
        activeRows.append({
            'id': diseaseId,
            'name': diseaseConfig['name'],
            'icon': diseaseConfig['icon'],
            'tips': diseaseConfig['tips'],
            'durationText': "已持续 {} / 最长 {}".format(
                formatDuration(data['activeSeconds'][diseaseId]),
                formatDuration(diseaseConfig['maxActiveSeconds'])
            ),
            'activeSeconds': data['activeSeconds'][diseaseId],
            'progressText': progressText,
            'symptom': diseaseConfig['symptom'],
            'cause': diseaseConfig['cause'],
            'relief': diseaseConfig['relief'],
            'lowGroups': diseaseConfig['lowGroups'],
            'highGroups': diseaseConfig['highGroups']
        })
    return {
        'active': activeRows,
        'activeCount': len(activeRows),
        'maxActiveCount': config.maxActiveCount,
        'validEatCount': data['validEatCount']
    }


# 疾病模块只同步自己的总开关，通用设置客户端负责把分批数据合并到同一页面。
def syncSettingToClient(serverSys, playerId, data):
    serverSys.NotifyToClient(playerId, config.settingEventSync, {
        'values': {
            config.settingEnabledKey: data['enabled']
        }
    })
