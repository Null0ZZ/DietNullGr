# -*- coding: utf-8 -*-

ssname = "Disease_Core_ServerSys"
csname = "Disease_Core_ClientSys"
ssPath = "Diet_NullGr.ModSys.Disease.Disease_ss.ServerSys"
csPath = "Diet_NullGr.ModSys.Disease.Disease_cs.ClientSys"

serverSysKey = {
    ssname: ssPath
}

clientSysKey = {
    csname: csPath
}

syncEvent = "DiseaseSyncData"
visualEvent = "DiseaseVisualSync"
visualReadyEvent = "DiseaseVisualReady"
symptomEvent = "DiseaseSymptom"
clientReadyEvent = "DiseaseClientReady"
jumpEvent = "DiseasePlayerJump"
settingEnabledKey = "disease_enabled"
settingEventUpdate = "DietSettingUpdate"
settingEventSync = "DietSettingSync"
settingKeys = (settingEnabledKey,)
defaultEnabled = True
debugCommandEnabled = False

settingDef = {
    "key": settingEnabledKey,
    "name": "启用疾病系统（开启后长期饮食失衡可能触发疾病；关闭后清除全部疾病状态并停止判定）",
    "control": "toggle",
    "default": defaultEnabled,
    "priority": 17,
    "groupId": ""
}

effectRefreshTick = 100
dataSaveTick = 600
customEffectDurationPadding = 10
statusEffectDuration = 6
nauseaDuration = 4
intermittentNauseaDuration = 10
nauseaSharedCooldownSeconds = 30
hypoglycemiaLateSeconds = 45
hypoglycemiaNauseaIntervalSeconds = 30
hyperglycemiaNauseaIntervalSeconds = 45
feverNauseaIntervalSeconds = 60
hypoglycemiaJumpIntervalTick = 30
ricketsJumpDamageCooldownTick = 100
ricketsJumpDamageChance = 15
ricketsFallDamageMultiplier = 1.5
symptomDamage = 1.0
minimumHealthAfterSymptom = 1.0
constipationSneakHoldTick = 5
constipationMaxVerticalMove = 0.4
constipationReliefSound = "diet_nullgr.constipation_relief"
constipationReliefSoundVolume = 1.0
constipationReliefSoundPitch = 1.0
ricketsFractureSound = "diet_nullgr.rickets_fracture"
ricketsFractureSoundVolume = 1.0
ricketsFractureSoundPitch = 1.0
constipationBodyGrowSeconds = 120.0
feverHeadGrowSeconds = 300.0
constipationMaximumBodyScale = 1.25
feverMaximumHeadScale = 2.5
visualScaleFadeTick = 20
hyperglycemiaThirstMultiplier = 1.25
feverThirstMultiplier = 1.5
hypoglycemiaVisionPostProcess = "dietHypoglycemiaVision"
hypoglycemiaVisionStrengthParameter = "strength"
hypoglycemiaVisionInitialStrength = 0.1
hypoglycemiaVisionMaxStrength = 1.0
hypoglycemiaVisionGrowSeconds = 90.0
hypoglycemiaVisionFadeTick = 20
hypoglycemiaSprintLimitSource = "hypoglycemia"
hypoglycemiaQuickProtectionSeconds = 60
bloodSugarConversionProtectionSeconds = 120
bodyScaleQuery = "query.mod.diet_body_scale"
headScaleQuery = "query.mod.diet_head_scale"
playerScaleAnimationKey = "diet_disease_scale"
playerScaleAnimation = "animation.diet_nullgr.disease_scale"
invalidGroundBlocks = [
    "minecraft:air",
    "minecraft:water",
    "minecraft:flowing_water",
    "minecraft:bubble_column"
]
invalidBodyBlocks = [
    "minecraft:water",
    "minecraft:flowing_water",
    "minecraft:bubble_column"
]

attrPrefix = "diet_nullgr_disease_"
attrEnabled = attrPrefix + "enabled"
attrValidEatCount = attrPrefix + "valid_eat_count"
attrActive = attrPrefix + "active"
attrConstipationSquatCount = attrPrefix + "constipation_squat_count"
attrProgressPrefix = attrPrefix + "progress_"
attrActiveSecondsPrefix = attrPrefix + "active_seconds_"
attrProtectionSecondsPrefix = attrPrefix + "protection_seconds_"
attrRecoveryProgressPrefix = attrPrefix + "recovery_progress_"

minimumValidEatCount = 5
maxActiveCount = 2
fullSlotProgressRatio = 0.5
progressFallbackMultiplier = 2.0
constipationSquatRequired = 12
thirstMaxValue = 20.0

# 存档、客户端显示和遍历统一使用固定顺序，避免字典顺序造成状态变化。
diseaseOrder = [
    "hypoglycemia",
    "hyperglycemia",
    "constipation",
    "rickets",
    "fever",
    "mouth_ulcer",
    "scurvy"
]

# 多种疾病同轮达到触发线时按玩法严重度填充空闲槽位，不替换已经确诊的疾病。
diagnosisOrder = [
    "fever",
    "hyperglycemia",
    "hypoglycemia",
    "scurvy",
    "rickets",
    "constipation",
    "mouth_ulcer"
]

bloodSugarConflict = {
    "hypoglycemia": "hyperglycemia",
    "hyperglycemia": "hypoglycemia"
}

# 每种疾病只依赖玩家可见的营养组；recoveryMetabolicPoints 为零表示饮食达标后立即痊愈。
diseases = {
    "hypoglycemia": {
        "name": "低血糖",
        "tips": "能量不足；吃主食、水果或甜食",
        "cause": "谷物、水果和糖分均长期处于低位。",
        "relief": "补充谷物可稳定缓解，水果或甜食可快速缓解。",
        "symptom": "初期疾跑不再加速并限制连续跳跃，持续后会视野模糊重影并间歇反胃。",
        "customEffect": "diet_nullgr:hypoglycemia",
        "icon": "textures/ui/diet_nullgr/disease/hypoglycemia_effect",
        "priority": 3,
        "triggerPoints": 3.0,
        "maxActiveSeconds": 240,
        "protectionSeconds": 180,
        "recoveryMetabolicPoints": 0.0,
        "lowGroups": ["fruits", "grains", "sugars"],
        "highGroups": [],
        "requiredGroups": ["grains", "fruits", "sugars"],
        "requiresThirst": False
    },
    "hyperglycemia": {
        "name": "高血糖",
        "tips": "糖分过量；停甜食并补其他食物",
        "cause": "糖分长期过高，并明显高于其他四类营养。",
        "relief": "暂停甜食，将糖分降到 55% 以下并补充至少两类非糖食物。",
        "symptom": "缓慢、间歇反胃、口渴消耗提高，并暂停糖分冲刺。",
        "customEffect": "diet_nullgr:hyperglycemia",
        "icon": "textures/ui/diet_nullgr/disease/hyperglycemia_effect",
        "priority": 2,
        "triggerPoints": 4.0,
        "maxActiveSeconds": 480,
        "protectionSeconds": 240,
        "recoveryMetabolicPoints": 0.0,
        "lowGroups": [],
        "highGroups": ["sugars"],
        "requiredGroups": ["fruits", "grains", "proteins", "vegetables", "sugars"],
        "requiresThirst": False
    },
    "constipation": {
        "name": "便秘",
        "tips": "缺水少纤维；补水、补两类食物或下蹲",
        "cause": "水分不足，且水果、谷物和蔬菜摄入偏少。",
        "relief": "将口渴值恢复到 50% 以上并补充其中至少两类食物，或完成 12 次有效下蹲。",
        "symptom": "进食后反胃，身体逐渐变大，可通过连续下蹲缓解。",
        "customEffect": "diet_nullgr:constipation",
        "icon": "textures/ui/diet_nullgr/disease/constipation_effect",
        "priority": 6,
        "triggerPoints": 8.0,
        "maxActiveSeconds": 600,
        "protectionSeconds": 180,
        "recoveryMetabolicPoints": 0.0,
        "lowGroups": ["fruits", "grains", "vegetables"],
        "highGroups": [],
        "requiredGroups": ["fruits", "grains", "vegetables"],
        "requiresThirst": True
    },
    "rickets": {
        "name": "佝偻病",
        "tips": "蛋白质不足；补充牛奶、鱼或蛋",
        "cause": "蛋白质长期不足，但其他饮食类别仍较充足。",
        "relief": "将蛋白质恢复到 45% 以上并保持 3 个代谢点，推荐牛奶、鱼或蛋。",
        "symptom": "摔落伤害提高，跳跃时可能受伤并播放骨折音效。",
        "customEffect": "diet_nullgr:rickets",
        "icon": "textures/ui/diet_nullgr/disease/rickets_effect",
        "priority": 5,
        "triggerPoints": 18.0,
        "maxActiveSeconds": 600,
        "protectionSeconds": 300,
        "recoveryMetabolicPoints": 3.0,
        "lowGroups": ["proteins"],
        "highGroups": [],
        "requiredGroups": ["fruits", "grains", "proteins", "vegetables"],
        "requiresThirst": False
    },
    "fever": {
        "name": "发烧",
        "tips": "严重缺水缺营养；补水并均衡进食",
        "cause": "严重缺水，并且多类非糖营养同时处于危急水平。",
        "relief": "将口渴值恢复到 50% 以上，并使至少三类非糖营养达到 30%。",
        "symptom": "虚弱、间歇反胃、口渴消耗提高，头部随持续时间逐渐变大。",
        "customEffect": "diet_nullgr:fever",
        "icon": "textures/ui/diet_nullgr/disease/fever_effect",
        "priority": 1,
        "triggerPoints": 5.0,
        "maxActiveSeconds": 360,
        "protectionSeconds": 240,
        "recoveryMetabolicPoints": 0.0,
        "lowGroups": ["fruits", "grains", "proteins", "vegetables"],
        "highGroups": [],
        "requiredGroups": ["fruits", "grains", "proteins", "vegetables"],
        "requiresThirst": True
    },
    "mouth_ulcer": {
        "name": "口腔溃疡",
        "tips": "谷物蛋白不足；补两类并少吃甜食",
        "cause": "谷物和蛋白质长期不足，高糖饮食会加快发病。",
        "relief": "让谷物和蛋白质一项达到 40%、另一项达到 30%，并减少甜食。",
        "symptom": "进食时播放疼痛提示，并有概率受到不会致死的伤害。",
        "customEffect": "diet_nullgr:mouth_ulcer",
        "icon": "textures/ui/diet_nullgr/disease/mouth_ulcer_effect",
        "priority": 7,
        "triggerPoints": 9.0,
        "maxActiveSeconds": 480,
        "protectionSeconds": 180,
        "recoveryMetabolicPoints": 0.0,
        "lowGroups": ["grains", "proteins"],
        "highGroups": [],
        "requiredGroups": ["grains", "proteins"],
        "requiresThirst": False
    },
    "scurvy": {
        "name": "坏血病",
        "tips": "水果蔬菜不足；补充水果或蔬菜",
        "cause": "水果和蔬菜长期严重不足，但谷物或蛋白质仍较充足。",
        "relief": "将水果恢复到 40% 以上，或将蔬菜恢复到 45% 以上。",
        "symptom": "持续虚弱，受伤后会短暂获得挖掘疲劳。",
        "customEffect": "diet_nullgr:scurvy",
        "icon": "textures/ui/diet_nullgr/disease/scurvy_effect",
        "priority": 4,
        "triggerPoints": 18.0,
        "maxActiveSeconds": 600,
        "protectionSeconds": 300,
        "recoveryMetabolicPoints": 0.0,
        "lowGroups": ["fruits", "vegetables"],
        "highGroups": [],
        "requiredGroups": ["fruits", "grains", "proteins", "vegetables"],
        "requiresThirst": False
    }
}

# 疾病测试指令只把营养快照调整到目标触发区间，疾病进度仍由真实饥饿下降自然推进。
# 发烧的条件天然会同时满足其他低营养疾病，最终确诊顺序继续服从正式疾病规则。
debugCommandNutritionProfiles = {
    "hypoglycemia": {
        "fruits": 0.10,
        "grains": 0.10,
        "proteins": 0.50,
        "vegetables": 0.50,
        "sugars": 0.10,
        "thirst": 1.00
    },
    "hyperglycemia": {
        "fruits": 0.50,
        "grains": 0.50,
        "proteins": 0.50,
        "vegetables": 0.50,
        "sugars": 1.00,
        "thirst": 1.00
    },
    "constipation": {
        "fruits": 0.20,
        "grains": 0.50,
        "proteins": 0.50,
        "vegetables": 0.20,
        "sugars": 0.50,
        "thirst": 0.30
    },
    "rickets": {
        "fruits": 0.50,
        "grains": 0.50,
        "proteins": 0.10,
        "vegetables": 0.50,
        "sugars": 0.50,
        "thirst": 1.00
    },
    "fever": {
        "fruits": 0.10,
        "grains": 0.10,
        "proteins": 0.10,
        "vegetables": 0.50,
        "sugars": 0.50,
        "thirst": 0.20
    },
    "mouth_ulcer": {
        "fruits": 0.20,
        "grains": 0.10,
        "proteins": 0.10,
        "vegetables": 0.50,
        "sugars": 0.75,
        "thirst": 1.00
    },
    "scurvy": {
        "fruits": 0.10,
        "grains": 0.50,
        "proteins": 0.50,
        "vegetables": 0.10,
        "sugars": 0.50,
        "thirst": 1.00
    }
}
