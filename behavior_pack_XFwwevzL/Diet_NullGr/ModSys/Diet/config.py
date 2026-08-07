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
settingResetOpenButtonPositionKey = "diet_reset_open_button_position"
settingResetOpenButtonPositionName = "重置饮食打开按钮位置"
settingResetOpenButtonPositionText = "重置"
settingResetOpenButtonPositionPriority = 18
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
# 首次营养起点与死亡重置必须分离，避免死亡把低营养玩家恢复到新玩家的 50%。
deathResetValue = 0.0
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
        "suggestion": "苹果、浆果或西瓜片",
        "icon": "minecraft:apple",
        "color": [238, 102, 119],
        "initialValue": 0.5,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "grains": {
        "name": "谷物",
        "suggestion": "面包、小麦或蛋糕",
        "icon": "minecraft:bread",
        "color": [204, 187, 68],
        "initialValue": 0.5,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "proteins": {
        "name": "蛋白质",
        "suggestion": "肉类、鱼、蛋或牛奶",
        "icon": "minecraft:cooked_beef",
        "color": [250, 141, 84],
        "initialValue": 0.5,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "vegetables": {
        "name": "蔬菜",
        "suggestion": "胡萝卜、马铃薯、蘑菇汤或海带",
        "icon": "minecraft:carrot",
        "color": [34, 136, 51],
        "initialValue": 0.5,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "sugars": {
        "name": "糖分",
        "suggestion": "蜂蜜、糖或甜点",
        "icon": "minecraft:honey_bottle",
        "color": [170, 51, 119],
        "initialValue": 0.5,
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
    "name": "死亡惩罚方式（选择死亡时按固定值扣除、按当前值比例扣除或重置为 {}%）".format(int(deathResetValue * 100.0)),
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

# FruitFarmerDelight 逐项按工作台、烹饪锅、榨汁机、切片和酿造来源审查；名称不替代实际配方。
# 数据来源：FruitFarmerDelight 仓库 9939171ed62199c106eb1d0aba248e72d44b0fff。
fruitFarmerDelightFoodGroups = {
    "fruitfarmersdelight_nullgr:a_mangosteen": ["fruits"],
    "fruitfarmersdelight_nullgr:a_segment_of_orange": ["fruits"],
    "fruitfarmersdelight_nullgr:baked_pear": ["fruits"],
    "fruitfarmersdelight_nullgr:banana": ["fruits"],
    "fruitfarmersdelight_nullgr:banana_beef": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:banana_egg_roll": ["fruits", "grains", "proteins"],
    "fruitfarmersdelight_nullgr:blueberry": ["fruits"],
    "fruitfarmersdelight_nullgr:blueberry_yam": ["fruits", "proteins", "vegetables", "sugars"],
    "fruitfarmersdelight_nullgr:braised_pineapple_meat": ["fruits", "proteins", "vegetables", "sugars"],
    "fruitfarmersdelight_nullgr:cake_passion_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cherry": ["fruits"],
    "fruitfarmersdelight_nullgr:cherry_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:dried_persimmon": ["fruits"],
    "fruitfarmersdelight_nullgr:durian_meat": ["fruits"],
    "fruitfarmersdelight_nullgr:durian_pizza_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_pean": ["fruits"],
    "fruitfarmersdelight_nullgr:grape": ["fruits"],
    "fruitfarmersdelight_nullgr:grape_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:grape_tiramisu": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:half_a_kiwi": ["fruits"],
    "fruitfarmersdelight_nullgr:half_a_mango": ["fruits"],
    "fruitfarmersdelight_nullgr:half_a_papaya": ["fruits"],
    "fruitfarmersdelight_nullgr:half_a_passion_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:half_a_pitaya": ["fruits"],
    "fruitfarmersdelight_nullgr:hami_melon_fire_sb_bowl": ["fruits", "grains", "vegetables"],
    "fruitfarmersdelight_nullgr:hami_melon_piece": ["fruits"],
    "fruitfarmersdelight_nullgr:haw_sheets": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:hawaiian_pizza_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:hawthorn": ["fruits"],
    "fruitfarmersdelight_nullgr:hawthorn_skewers": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:honey_peach": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_blueberry": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_grape": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_mulberry": ["fruits"],
    "fruitfarmersdelight_nullgr:jellydrops_blueberry": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_grape": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:kiwi_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:lemon_chicken_chop": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:lemon_slice": ["fruits"],
    "fruitfarmersdelight_nullgr:litchi_chicken": ["fruits", "proteins", "vegetables", "sugars"],
    "fruitfarmersdelight_nullgr:liulian_stewed_chicken": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:longan": ["fruits"],
    "fruitfarmersdelight_nullgr:loquat": ["fruits"],
    "fruitfarmersdelight_nullgr:luxurious_fruit_salad": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:lychee": ["fruits"],
    "fruitfarmersdelight_nullgr:mango": ["fruits"],
    "fruitfarmersdelight_nullgr:mango_cake": ["fruits", "grains", "sugars"],
    "fruitfarmersdelight_nullgr:mango_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mango_milk": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mangosteen": ["fruits"],
    "fruitfarmersdelight_nullgr:matcha_strawberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_grape": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_kiwifruit": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_passion_fruit": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mulberry": ["fruits"],
    "fruitfarmersdelight_nullgr:papaya_milk": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:passion_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:passion_fruit_chicken": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:passion_fruit_pasta": ["fruits", "grains", "sugars"],
    "fruitfarmersdelight_nullgr:passion_fruit_trout": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:pawpaw": ["fruits"],
    "fruitfarmersdelight_nullgr:pear": ["fruits"],
    "fruitfarmersdelight_nullgr:persimmon": ["fruits"],
    "fruitfarmersdelight_nullgr:pineapple_drumstick_fort": ["fruits", "grains", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:pineapple_rice": ["fruits", "grains", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:pineapple_slice": ["fruits"],
    "fruitfarmersdelight_nullgr:pineapple_strand": ["fruits"],
    "fruitfarmersdelight_nullgr:pitaya_dragon_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:roasted_durian": ["fruits"],
    "fruitfarmersdelight_nullgr:shaddock_slice": ["fruits"],
    "fruitfarmersdelight_nullgr:steamed_eggs_with_oranges": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:stewed_beef_with_hawthorn": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:stewed_beef_with_red_wine": ["fruits", "grains", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:stewed_pear_with_apple": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:stewed_pear_with_loquat": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:strawberry_boo": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:strawberry_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:strawberry_egg_tart": ["fruits", "grains", "proteins"],
    "fruitfarmersdelight_nullgr:tangerine": ["fruits"],
    "fruitfarmersdelight_nullgr:tangerine_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:three_colour_custard": ["fruits", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:biscuit_banana": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_blueberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_cherry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_durian": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_grape": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_hami_melon": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_hawthorn": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_kiwifruit": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_lemon": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_longan": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_loquat": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_lychee": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_mango": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_mangosteen": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_mulberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_papaya": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_passion_fruit": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_peach": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_pear": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_persimmon": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_pineapple": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_pitaya_dragon_fruit": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_raspberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_shaddock": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:biscuit_tangerine": ["fruits", "grains", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:cake_banana_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_cherry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_hami_melon_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_kiwifruit_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_lemon_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_longan_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_loquat_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_lychee_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_mangosteen_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_mulberry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_papaya_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_peach_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_pear_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_persimmon_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_pineapple_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_shaddock_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_strawberry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cake_tangerine_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cheesecake_hawthorn_slice": ["fruits", "grains", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:forzen_sucker_banana": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_blueberry": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_cherry": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_durian": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_grape": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_hami_melon": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_hawthorn": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_kiwifruit": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_longan": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_loquat": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_lychee": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_mango": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_mangosteen": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_mulberry": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_papaya": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_passion_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_peach": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_pear": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_persimmon": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_pineapple": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_pitaya_dragon_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_shaddock": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_tangerine": ["fruits"],

    "fruitfarmersdelight_nullgr:fruit_juice_banana": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_blueberry": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_cherry": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_grape": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_hami_melon": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_hawthorn": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_kiwifruit": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_longan": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_loquat": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_lychee": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_mango": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_mangosteen": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_mulberry": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_papaya": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_passion_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_peach": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_persimmon": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_pineapple": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_pitaya_dragon_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_shaddock": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_tangerine": ["fruits"],

    "fruitfarmersdelight_nullgr:icecream_banana": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_cherry": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_durian": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_hami_melon": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_hawthorn": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_kiwifruit": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_longan": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_loquat": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_lychee": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_mango": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_mangosteen": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_papaya": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_passion_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_peach": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_pear": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_persimmon": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_pineapple": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_pitaya_dragonfruit": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_shaddock": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_tangerine": ["fruits"],

    "fruitfarmersdelight_nullgr:jam_banana": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_blueberry": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_cherry": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_durian": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_grape": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_hami_melon": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_hawthorn": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_kiwifruit": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_longan": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_loquat": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_lychee": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_mango": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_mangosteen": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_mulberry": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_papaya": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_passion_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_peach": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_pear": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_persimmon": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_pineapple": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_pitaya_dragon_fruit": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_shaddock": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_tangerine": ["fruits"],

    "fruitfarmersdelight_nullgr:jellydrops_cherry": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_durian": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_hami_melon": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_hawthorn": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_kiwifruit": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_lemon": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_longan": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_loquat": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_lychee": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_mango": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_mangosteen": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_mulberry": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_papaya": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_peach": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_pear": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_persimmon": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_pineapple": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_pitaya_dragonfruit": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_raspberry": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_shaddock": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_tangerine": ["fruits", "proteins"],

    "fruitfarmersdelight_nullgr:milkshake_avocado": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_banana": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_blueberry": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_cherry": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_durian": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_hami_melon": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_hawthorn": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_lemon": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_longan": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_loquat": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_lychee": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_mango": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_mangosteen": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_mulberry": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_papaya": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_peach": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_pear": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_persimmon": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_pineapple": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_pitaya_dragonfruit": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_raspberry": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_shaddock": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_strawberry": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_tangerine": ["fruits", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:mousse_blueberry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mousse_mango_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mousse_pitaya_dragon_fruit_slice": ["fruits", "grains", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:muffin_banana": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_blueberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_cherry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_durian": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_grape": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_lemon": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_longan": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_lychee": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_mango": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_mulberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_papaya": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_passionfruit": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_peach": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_persimmon": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_pineapple": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_pitaya_dragon_fruit": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_raspberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_shaddock": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_strawberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:muffin_tangerine": ["fruits", "grains", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:send_banana_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_blueberry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_cherry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_durian_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_grape_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_hami_melon_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_hawthorn_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_kiwifruit_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_lemon_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_longan_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_loquat_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_lychee_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_mango_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_mangosteen_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_mulberry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_papaya_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_passion_fruit_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_peach_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_persimmon_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_pineapple_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_pitaya_dragon_fruit_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_raspberry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_shaddock_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_strawberry_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:send_tangerine_slice": ["fruits", "grains", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:thousand_layer_cake_durian_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:thousand_layer_cake_raspberry_slice": ["fruits", "grains", "proteins", "sugars"],

    "fruitfarmersdelight_nullgr:wine_banana": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_blueberry": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_cherry": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_grape": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_hami_melon": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_hawthorn": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_kiwifruit": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_lemon": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_longan": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_loquat": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_mango": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_mangosteen_litchi": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_mulberry": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_papaya": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_passion_fruit": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_peach": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_pear": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_persimmon": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_pineapple": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_pitaya_dragon_fruit": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_raspberry": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_shaddock": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_strawberry": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_tangerine": ["fruits", "grains"],
    "fruitfarmersdelight_nullgr:wine_watermelon": ["fruits", "grains"]
}
foodGroups.update(fruitFarmerDelightFoodGroups)

effectDescriptions = {}
for effectId in effectOrder:
    effectDescriptions[effectId] = dietEffects[effectId]["description"]
for penaltyId in penaltyOrder:
    effectDescriptions[penaltyId] = dietPenalties[penaltyId]["description"]
