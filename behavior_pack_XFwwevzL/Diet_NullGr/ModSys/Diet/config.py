# -*- coding: utf-8 -*-

ssname = "Diet_Core_ServerSys"
csname = "Diet_Core_ClientSys"
ssPath = "Diet_NullGr.ModSys.Diet.Diet_ss.ServerSys"
csPath = "Diet_NullGr.ModSys.Diet.Diet_cs.ClientSys"
uiKey = "diet_screen"
uiName = "diet_screen.main"
uiPath = "Diet_NullGr.ModSys.Diet.DietUI.DietUI"
buttonUiKey = "diet_button"
buttonUiName = "diet_button.main"
buttonUiPath = "Diet_NullGr.ModSys.Diet.DietButtonUI.DietButtonUI"
buttonConfigKey = "Diet_NullGr_ButtonPos"
buttonPosKey = "button_pos"
buttonLongPressSeconds = 1.0
buttonClickMoveLimit = 8.0
settingItemId = "diet_nullgr"
settingName = "均衡饮食"
settingIconPath = "textures/ui/diet_nullgr/button"
settingEventUpdate = "DietSettingUpdate"
settingEventSync = "DietSettingSync"
lowNutritionAlertEvent = "DietLowNutritionAlert"
settingActiveKey = "diet_active"
settingGroupPrefix = "diet_track_"
settingEffectPrefix = "diet_effect_"
settingPenaltyPrefix = "diet_penalty_"
settingTargetValueKey = "diet_target_value"
settingLowPenaltyEnabledKey = "diet_low_penalty_enabled"
settingNutritionPenaltyValueKey = "diet_nutrition_penalty_value"
settingNutritionPenaltyWarningOffsetKey = "diet_nutrition_penalty_warning_offset"
settingDeathPenaltyMethodKey = "diet_death_penalty_method"
settingDeathPenaltyLossKey = "diet_death_penalty_loss"
settingDeathPenaltyMinKey = "diet_death_penalty_min"
settingTargetText = "自己"
controlToggle = "toggle"
controlSlider = "slider"
controlDropDown = "dropdown"

serverSysKey = {
}

clientSysKey = {
}

attrPrefix = "diet_nullgr_"
effectRefreshTick = 12
gainPenaltyPerGroup = 15.0
decayPenaltyPerGroup = 15.0
targetDietValue = 0.8
lowPenaltyEnabled = True
nutritionPenaltyValue = 0.15
nutritionPenaltyWarningOffset = 0.05
lowNutritionAlertSound = "random.toast"
lowNutritionAlertVolume = 1.0
lowNutritionAlertPitch = 1.0
deathPenaltyMin = 0.0
deathPenaltyLoss = 1.0
deathPenaltyMethodAmount = "AMOUNT"
deathPenaltyMethodPercent = "PERCENT"
deathPenaltyMethodReset = "RESET"
deathPenaltyMethodDefault = deathPenaltyMethodAmount
deathPenaltyMethodOrder = [deathPenaltyMethodAmount, deathPenaltyMethodPercent, deathPenaltyMethodReset]
deathPenaltyMethodNames = {
    deathPenaltyMethodAmount: "固定扣除",
    deathPenaltyMethodPercent: "按比例扣除",
    deathPenaltyMethodReset: "死亡重置"
}
deathPenaltyMethodOptions = []
for deathPenaltyMethod in deathPenaltyMethodOrder:
    deathPenaltyMethodOptions.append(deathPenaltyMethodNames[deathPenaltyMethod])
expBase = 2.718281828

groupOrder = ["fruits", "grains", "proteins", "vegetables", "sugars"]

percentColorHealthy = (0.96, 0.96, 0.96)
percentColorCaution = (1.0, 0.92, 0.18)
percentColorWarning = (1.0, 0.55, 0.08)
percentColorDanger = (1.0, 0.16, 0.12)

groups = {
    "fruits": {
        "name": "水果",
        "tooltip": "你摄入的水果、浆果与甜瓜类食物。",
        "suggestion": "苹果、浆果或西瓜片",
        "icon": "minecraft:apple",
        "color": [212, 28, 83],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "grains": {
        "name": "谷物",
        "tooltip": "你摄入的面包、小麦、蛋糕等谷物来源。",
        "suggestion": "面包、小麦或蛋糕",
        "icon": "minecraft:bread",
        "color": [212, 163, 28],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "proteins": {
        "name": "蛋白质",
        "tooltip": "你摄入的肉类、鱼、蛋和奶类来源。",
        "suggestion": "肉类、鱼、蛋或牛奶",
        "icon": "minecraft:cooked_beef",
        "color": [212, 120, 28],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "vegetables": {
        "name": "蔬菜",
        "tooltip": "你摄入的根茎、蘑菇、海带和蔬菜汤。",
        "suggestion": "胡萝卜、马铃薯、蘑菇汤或海带",
        "icon": "minecraft:carrot",
        "color": [49, 212, 28],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "sugars": {
        "name": "糖分",
        "tooltip": "你摄入的糖、蜂蜜、甜点与高糖食物。",
        "suggestion": "蜂蜜、糖或甜点",
        "icon": "minecraft:honey_bottle",
        "color": [255, 143, 233],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    }
}

effectOrder = ["balanced", "sugarRush"]
penaltyOrder = ["singleLowNutrition", "multipleLowNutrition"]

dietEffects = {
    "balanced": {
        "name": "均衡奖励",
        "settingKey": settingEffectPrefix + "balanced",
        "defaultEnabled": True,
        "description": "主食、水果、蔬菜、蛋白质达到目标值：获得生命提升、力量、抗性。",
        "conditions": [
            {
                "groups": ["proteins", "fruits", "vegetables", "grains"],
                "match": "all",
                "minMatches": 1,
                "useTarget": True,
                "usePenaltyThreshold": False,
                "above": targetDietValue,
                "below": 1.0
            }
        ],
        "statusEffects": [
            {"name": "health_boost", "duration": 6, "amplifier": 0, "increment": 0},
            {"name": "strength", "duration": 6, "amplifier": 0, "increment": 0},
            {"name": "resistance", "duration": 6, "amplifier": 0, "increment": 0}
        ]
    },
    "sugarRush": {
        "name": "糖分冲刺",
        "settingKey": settingEffectPrefix + "sugarRush",
        "defaultEnabled": True,
        "description": "糖分达到目标值：获得速度，但同时获得饥饿。",
        "conditions": [
            {
                "groups": ["sugars"],
                "match": "all",
                "minMatches": 1,
                "useTarget": True,
                "usePenaltyThreshold": False,
                "above": targetDietValue,
                "below": 1.0
            }
        ],
        "statusEffects": [
            {"name": "speed", "duration": 6, "amplifier": 0, "increment": 0},
            {"name": "hunger", "duration": 6, "amplifier": 2, "increment": 0}
        ]
    }
}

dietPenalties = {
    "singleLowNutrition": {
        "name": "营养不足",
        "settingKey": settingPenaltyPrefix + "singleLowNutrition",
        "enabled": True,
        "description": "任意一项营养低于惩罚阈值：获得虚弱。",
        "conditions": [
            {
                "groups": groupOrder,
                "match": "any",
                "minMatches": 1,
                "useTarget": False,
                "usePenaltyThreshold": True,
                "above": 0.0,
                "below": nutritionPenaltyValue
            }
        ],
        "statusEffects": [
            {"name": "weakness", "duration": 6, "amplifier": 0, "increment": 0}
        ]
    },
    "multipleLowNutrition": {
        "name": "严重营养不足",
        "settingKey": settingPenaltyPrefix + "multipleLowNutrition",
        "enabled": True,
        "description": "任意两项营养低于惩罚阈值：额外获得缓慢。",
        "conditions": [
            {
                "groups": groupOrder,
                "match": "every",
                "minMatches": 2,
                "useTarget": False,
                "usePenaltyThreshold": True,
                "above": 0.0,
                "below": nutritionPenaltyValue
            }
        ],
        "statusEffects": [
            {"name": "slowness", "duration": 6, "amplifier": 0, "increment": 0}
        ]
    }
}

effectSettingKeys = {}
for effectId in effectOrder:
    effectSettingKeys[effectId] = dietEffects[effectId]["settingKey"]

settingGroupKeys = {}
for groupId in groupOrder:
    settingGroupKeys[groupId] = settingGroupPrefix + groupId

settingDefs = [
    {
        "key": settingActiveKey,
        "name": "启用均衡饮食",
        "control": controlToggle,
        "default": True,
        "priority": 10,
        "groupId": ""
    }
]
settingPriority = 20
for groupId in groupOrder:
    settingDefs.append({
        "key": settingGroupKeys[groupId],
        "name": "追踪{}".format(groups[groupId]["name"]),
        "control": controlToggle,
        "default": True,
        "priority": settingPriority,
        "groupId": groupId
    })
    settingPriority += 10

settingDefs.append({
    "key": settingTargetValueKey,
    "name": "目标营养值",
    "control": controlSlider,
    "default": int(targetDietValue * 100.0),
    "priority": settingPriority,
    "step": 100,
    "groupId": ""
})
settingPriority += 10
for effectId in effectOrder:
    settingDefs.append({
        "key": dietEffects[effectId]["settingKey"],
        "name": "启用{}".format(dietEffects[effectId]["name"]),
        "control": controlToggle,
        "default": dietEffects[effectId]["defaultEnabled"],
        "priority": settingPriority,
        "groupId": ""
    })
    settingPriority += 10

settingDefs.append({
    "key": settingLowPenaltyEnabledKey,
    "name": "启用低值惩罚",
    "control": controlToggle,
    "default": lowPenaltyEnabled,
    "priority": settingPriority,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingNutritionPenaltyValueKey,
    "name": "低值惩罚阈值",
    "control": controlSlider,
    "default": int(nutritionPenaltyValue * 100.0),
    "priority": settingPriority,
    "step": 100,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingNutritionPenaltyWarningOffsetKey,
    "name": "低值提醒提前量",
    "control": controlSlider,
    "default": int(nutritionPenaltyWarningOffset * 100.0),
    "priority": settingPriority,
    "step": 100,
    "groupId": ""
})
settingPriority += 10
for penaltyId in penaltyOrder:
    settingDefs.append({
        "key": dietPenalties[penaltyId]["settingKey"],
        "name": "启用{}".format(dietPenalties[penaltyId]["name"]),
        "control": controlToggle,
        "default": dietPenalties[penaltyId]["enabled"],
        "priority": settingPriority,
        "groupId": ""
    })
    settingPriority += 10

settingDefs.append({
    "key": settingDeathPenaltyMethodKey,
    "name": "死亡惩罚方式",
    "control": controlDropDown,
    "default": deathPenaltyMethodNames[deathPenaltyMethodDefault],
    "priority": settingPriority,
    "options": deathPenaltyMethodOptions,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingDeathPenaltyLossKey,
    "name": "死亡扣除比例",
    "control": controlSlider,
    "default": int(deathPenaltyLoss * 100.0),
    "priority": settingPriority,
    "step": 100,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingDeathPenaltyMinKey,
    "name": "死亡最低保留",
    "control": controlSlider,
    "default": int(deathPenaltyMin * 100.0),
    "priority": settingPriority,
    "step": 100,
    "groupId": ""
})

settingDefByKey = {}
for settingDef in settingDefs:
    settingDefByKey[settingDef["key"]] = settingDef

dietTagGroups = {
    "diet/fruit": ["fruits"],
    "diet/fruits": ["fruits"],
    "diet/grain": ["grains"],
    "diet/grains": ["grains"],
    "diet/protein": ["proteins"],
    "diet/proteins": ["proteins"],
    "diet/vegetable": ["vegetables"],
    "diet/vegetables": ["vegetables"],
    "diet/sugar": ["sugars"],
    "diet/sugars": ["sugars"]
}

foodGroups = {
    "minecraft:apple": ["fruits"],
    "minecraft:chorus_fruit": ["fruits"],
    "minecraft:enchanted_golden_apple": ["fruits", "sugars"],
    "minecraft:glow_berries": ["fruits"],
    "minecraft:golden_apple": ["fruits", "sugars"],
    "minecraft:melon": ["fruits"],
    "minecraft:melon_slice": ["fruits"],
    "minecraft:sweet_berries": ["fruits", "sugars"],

    "minecraft:bread": ["grains"],
    "minecraft:cake": ["grains", "sugars"],
    "minecraft:cookie": ["grains", "sugars"],
    "minecraft:pumpkin_pie": ["grains", "vegetables", "sugars"],
    "minecraft:wheat": ["grains"],

    "minecraft:beef": ["proteins"],
    "minecraft:bone": ["proteins"],
    "minecraft:chicken": ["proteins"],
    "minecraft:cod": ["proteins"],
    "minecraft:cooked_beef": ["proteins"],
    "minecraft:cooked_chicken": ["proteins"],
    "minecraft:cooked_cod": ["proteins"],
    "minecraft:cooked_mutton": ["proteins"],
    "minecraft:cooked_porkchop": ["proteins"],
    "minecraft:cooked_rabbit": ["proteins"],
    "minecraft:cooked_salmon": ["proteins"],
    "minecraft:egg": ["proteins"],
    "minecraft:fermented_spider_eye": ["proteins", "vegetables"],
    "minecraft:ink_sac": ["proteins"],
    "minecraft:milk_bucket": ["proteins"],
    "minecraft:mutton": ["proteins"],
    "minecraft:porkchop": ["proteins"],
    "minecraft:pufferfish": ["proteins"],
    "minecraft:rabbit": ["proteins"],
    "minecraft:rabbit_stew": ["proteins", "vegetables"],
    "minecraft:rotten_flesh": ["proteins"],
    "minecraft:salmon": ["proteins"],
    "minecraft:spider_eye": ["proteins"],
    "minecraft:suspicious_stew": ["proteins", "vegetables"],
    "minecraft:tropical_fish": ["proteins"],
    "minecraft:turtle_egg": ["proteins"],

    "minecraft:baked_potato": ["vegetables"],
    "minecraft:bamboo": ["vegetables"],
    "minecraft:beetroot": ["vegetables"],
    "minecraft:beetroot_seeds": ["vegetables"],
    "minecraft:beetroot_soup": ["vegetables"],
    "minecraft:birch_leaves": ["vegetables"],
    "minecraft:brown_mushroom": ["vegetables"],
    "minecraft:cactus": ["vegetables"],
    "minecraft:carrot": ["vegetables"],
    "minecraft:crimson_fungus": ["vegetables"],
    "minecraft:crimson_roots": ["vegetables"],
    "minecraft:dried_kelp": ["vegetables"],
    "minecraft:golden_carrot": ["vegetables", "sugars"],
    "minecraft:kelp": ["vegetables"],
    "minecraft:lily_pad": ["vegetables"],
    "minecraft:melon_seeds": ["vegetables"],
    "minecraft:mushroom_stew": ["vegetables"],
    "minecraft:nether_wart": ["vegetables"],
    "minecraft:poisonous_potato": ["vegetables"],
    "minecraft:potato": ["vegetables"],
    "minecraft:pumpkin": ["vegetables"],
    "minecraft:pumpkin_seeds": ["vegetables"],
    "minecraft:red_mushroom": ["vegetables"],
    "minecraft:sea_pickle": ["vegetables"],
    "minecraft:seagrass": ["vegetables"],
    "minecraft:shroomlight": ["vegetables"],
    "minecraft:sunflower": ["vegetables"],
    "minecraft:warped_fungus": ["vegetables"],
    "minecraft:warped_roots": ["vegetables"],
    "minecraft:wheat_seeds": ["vegetables"],

    "minecraft:cocoa_beans": ["sugars"],
    "minecraft:honey_bottle": ["sugars"],
    "minecraft:honeycomb": ["sugars"],
    "minecraft:sugar": ["sugars"]
}

effectDescriptions = {}
for effectId in effectOrder:
    effectDescriptions[effectId] = dietEffects[effectId]["description"]
for penaltyId in penaltyOrder:
    effectDescriptions[penaltyId] = dietPenalties[penaltyId]["description"]
