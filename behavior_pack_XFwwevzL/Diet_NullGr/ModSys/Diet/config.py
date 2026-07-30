# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.Disease.config as diseaseConfig
import Diet_NullGr.ModSys.Thirst.config as thirstConfig

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
buttonLayoutVersionKey = "layout_version"
buttonLayoutVersion = 2
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
effectRefreshTick = 1200
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
# 糖分不是必需营养，普通低值提醒与惩罚只检查四类基础营养；糖分异常由疾病系统单独反馈。
essentialGroupOrder = ["fruits", "grains", "proteins", "vegetables"]

percentColorHealthy = (0.96, 0.96, 0.96)
percentColorCaution = (1.0, 0.92, 0.18)
percentColorWarning = (1.0, 0.55, 0.08)
percentColorDanger = (1.0, 0.16, 0.12)
diseaseHighOutlineColor = (1.0, 0.2509803921568627, 0.1019607843137255)
diseaseLowOutlineColor = (0.3058823529411765, 0.9098039215686274, 1.0)

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
        "settingDescription": "开启后四项非糖营养达标会获得生命提升、力量与抗性；关闭后不触发",
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
        "settingDescription": "开启后糖分达标会获得速度和饥饿效果；关闭后不触发",
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
                "groups": essentialGroupOrder,
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
                "groups": essentialGroupOrder,
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
        "name": "启用均衡饮食（开启后进食与饥饿变化会改变营养值并触发饮食效果；关闭后暂停这些功能）",
        "control": controlToggle,
        "default": True,
        "priority": 10,
        "groupId": ""
    },
    thirstConfig.settingDef,
    thirstConfig.styleSettingDef,
    diseaseConfig.settingDef
]
settingPriority = 20
for groupId in groupOrder:
    settingDefs.append({
        "key": settingGroupKeys[groupId],
        "name": "追踪{}（开启后该类食物会改变此营养值并参与效果判断；关闭后数值不再变化且不参与效果）".format(groups[groupId]["name"]),
        "control": controlToggle,
        "default": True,
        "priority": settingPriority,
        "groupId": groupId
    })
    settingPriority += 10

settingDefs.append({
    "key": settingTargetValueKey,
    "name": "目标营养值（奖励效果的达标线；数值越高越难触发奖励）",
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
        "name": "启用{}（{}）".format(dietEffects[effectId]["name"], dietEffects[effectId]["settingDescription"]),
        "control": controlToggle,
        "default": dietEffects[effectId]["defaultEnabled"],
        "priority": settingPriority,
        "groupId": ""
    })
    settingPriority += 10

settingDefs.append({
    "key": settingLowPenaltyEnabledKey,
    "name": "启用低值惩罚（开启后会提醒低营养并施加已启用的惩罚；关闭后不再提醒或施加低值惩罚）",
    "control": controlToggle,
    "default": lowPenaltyEnabled,
    "priority": settingPriority,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingNutritionPenaltyValueKey,
    "name": "低值惩罚阈值（营养值达到或低于此百分比时触发已启用的惩罚；数值越高越容易触发）",
    "control": controlSlider,
    "default": int(nutritionPenaltyValue * 100.0),
    "priority": settingPriority,
    "step": 100,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingNutritionPenaltyWarningOffsetKey,
    "name": "低值提醒提前量（在惩罚阈值基础上提前多少个百分点提醒；数值越高提醒越早）",
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
        "name": "启用{}（开启后{}关闭后不再施加该效果）".format(dietPenalties[penaltyId]["name"], dietPenalties[penaltyId]["description"]),
        "control": controlToggle,
        "default": dietPenalties[penaltyId]["enabled"],
        "priority": settingPriority,
        "groupId": ""
    })
    settingPriority += 10

settingDefs.append({
    "key": settingDeathPenaltyMethodKey,
    "name": "死亡惩罚方式（选择死亡时按固定值扣除、按当前值比例扣除或重置为初始值）",
    "control": controlDropDown,
    "default": deathPenaltyMethodNames[deathPenaltyMethodDefault],
    "priority": settingPriority,
    "options": deathPenaltyMethodOptions,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingDeathPenaltyLossKey,
    "name": "死亡扣除比例（固定扣除时减营养百分点，按比例扣除时减当前值比例；死亡重置时无效）",
    "control": controlSlider,
    "default": int(deathPenaltyLoss * 100.0),
    "priority": settingPriority,
    "step": 100,
    "groupId": ""
})
settingPriority += 10
settingDefs.append({
    "key": settingDeathPenaltyMinKey,
    "name": "死亡最低保留（固定或按比例扣除后至少保留的营养值；死亡重置时不生效）",
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

# FarmerDelight 逐项按实际配方、可食份量和成品定位审查；药剂不登记为营养食物。
# 数据来源：FarmerDelight 仓库 8337dcdb00e28fbea0fd3f0379faa994a2810372。
farmerDelightFoodGroups = {
    "farmer_delight_nullgr:apple_cider": ["fruits", "sugars"],
    "farmer_delight_nullgr:apple_pie_slice": ["fruits", "grains", "sugars"],
    "farmer_delight_nullgr:bacon": ["proteins"],
    "farmer_delight_nullgr:bacon_and_eggs": ["proteins"],
    "farmer_delight_nullgr:bacon_sandwich": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:baked_cod_stew": ["proteins", "vegetables"],
    "farmer_delight_nullgr:barbecue_stick": ["proteins", "vegetables"],
    "farmer_delight_nullgr:beef_patty": ["proteins"],
    "farmer_delight_nullgr:beef_stew": ["proteins", "vegetables"],
    "farmer_delight_nullgr:bone_broth": ["proteins", "vegetables"],
    "farmer_delight_nullgr:cabbage": ["vegetables"],
    "farmer_delight_nullgr:cabbage_leaf": ["vegetables"],
    "farmer_delight_nullgr:cabbage_rolls": ["proteins", "vegetables"],
    "farmer_delight_nullgr:cake_slice": ["grains", "sugars"],
    "farmer_delight_nullgr:chicken_cuts": ["proteins"],
    "farmer_delight_nullgr:chicken_sandwich": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:chicken_soup": ["proteins", "vegetables"],
    "farmer_delight_nullgr:chocolate_pie_slice": ["grains", "proteins", "sugars"],
    "farmer_delight_nullgr:cod_roll": ["grains", "proteins"],
    "farmer_delight_nullgr:cod_slice": ["proteins"],
    "farmer_delight_nullgr:cooked_bacon": ["proteins"],
    "farmer_delight_nullgr:cooked_chicken_cuts": ["proteins"],
    "farmer_delight_nullgr:cooked_cod_slice": ["proteins"],
    "farmer_delight_nullgr:cooked_mutton_chops": ["proteins"],
    "farmer_delight_nullgr:cooked_rice": ["grains"],
    "farmer_delight_nullgr:cooked_salmon_slice": ["proteins"],
    "farmer_delight_nullgr:dumplings": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:egg_sandwich": ["grains", "proteins"],
    "farmer_delight_nullgr:fish_stew": ["proteins", "vegetables"],
    "farmer_delight_nullgr:fried_egg": ["proteins"],
    "farmer_delight_nullgr:fried_rice": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:fruit_salad": ["fruits", "proteins", "vegetables", "sugars"],
    "farmer_delight_nullgr:gleaming_salad": ["fruits", "vegetables", "sugars"],
    "farmer_delight_nullgr:glow_berry_custard": ["fruits", "proteins", "sugars"],
    "farmer_delight_nullgr:grilled_salmon": ["fruits", "proteins", "vegetables"],
    "farmer_delight_nullgr:ham": ["proteins"],
    "farmer_delight_nullgr:hamburger": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:honey_cookie": ["grains", "sugars"],
    "farmer_delight_nullgr:honey_glazed_ham": ["fruits", "grains", "proteins", "vegetables", "sugars"],
    "farmer_delight_nullgr:hot_cocoa": ["proteins", "sugars"],
    "farmer_delight_nullgr:kelp_roll": ["grains", "vegetables"],
    "farmer_delight_nullgr:kelp_roll_slice": ["grains", "vegetables"],
    "farmer_delight_nullgr:melon_juice": ["fruits", "sugars"],
    "farmer_delight_nullgr:melon_popsicle": ["fruits"],
    "farmer_delight_nullgr:milk_bottle": ["proteins"],
    "farmer_delight_nullgr:minced_beef": ["proteins"],
    "farmer_delight_nullgr:mixed_salad": ["vegetables", "sugars"],
    "farmer_delight_nullgr:mushroom_rice": ["grains", "vegetables"],
    "farmer_delight_nullgr:mutton_chops": ["proteins"],
    "farmer_delight_nullgr:mutton_wrap": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:nether_salad": ["vegetables"],
    "farmer_delight_nullgr:noodle_soup": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:onion": ["vegetables"],
    "farmer_delight_nullgr:onion_soup": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:pasta_with_meatballs": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:pasta_with_mutton_chop": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:pie_crust": ["grains", "proteins"],
    "farmer_delight_nullgr:pumpkin_slice": ["vegetables"],
    "farmer_delight_nullgr:pumpkin_soup": ["proteins", "vegetables"],
    "farmer_delight_nullgr:ratatouille": ["vegetables"],
    "farmer_delight_nullgr:raw_pasta": ["grains"],
    "farmer_delight_nullgr:roast_chicken": ["proteins", "vegetables", "sugars"],
    "farmer_delight_nullgr:roasted_mutton_chops": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:salmon_roll": ["grains", "proteins"],
    "farmer_delight_nullgr:salmon_slice": ["proteins"],
    "farmer_delight_nullgr:shepherds_pie_item": ["proteins", "vegetables"],
    "farmer_delight_nullgr:smoked_ham": ["proteins"],
    "farmer_delight_nullgr:squid_ink_pasta": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:steak_and_potatoes": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:stuffed_potato": ["proteins", "vegetables"],
    "farmer_delight_nullgr:stuffed_pumpkin": ["fruits", "grains", "proteins", "vegetables", "sugars"],
    "farmer_delight_nullgr:sweet_berry_cheesecake_slice": ["fruits", "grains", "proteins", "sugars"],
    "farmer_delight_nullgr:sweet_berry_cookie": ["fruits", "grains", "sugars"],
    "farmer_delight_nullgr:tomato": ["vegetables"],
    "farmer_delight_nullgr:tomato_sauce": ["vegetables", "sugars"],
    "farmer_delight_nullgr:vegetable_noodles": ["grains", "vegetables"],
    "farmer_delight_nullgr:vegetable_soup": ["vegetables"],
    "farmer_delight_nullgr:wheat_dough": ["grains"]
}
foodGroups.update(farmerDelightFoodGroups)

effectDescriptions = {}
for effectId in effectOrder:
    effectDescriptions[effectId] = dietEffects[effectId]["description"]
for penaltyId in penaltyOrder:
    effectDescriptions[penaltyId] = dietPenalties[penaltyId]["description"]
