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
openDietScreenKeyName = "打开均衡饮食"
openDietScreenKeyCategory = "均衡饮食"
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
# 默认只有生存和冒险模式参与饮食系统；开启后创造模式也参与，旁观模式始终冻结。
creativeModeAffected = False
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
deathPenaltyLoss = 0.5
# 首次营养起点与死亡重置必须分离，避免死亡把低营养玩家恢复到新玩家的 50%。
deathResetValue = 0.0
deathPenaltyMethodAmount = "AMOUNT"
deathPenaltyMethodPercent = "PERCENT"
deathPenaltyMethodReset = "RESET"
deathPenaltyMethodDefault = deathPenaltyMethodPercent
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
    "minecraft:apple": ["fruits", "sugars"],
    "minecraft:chorus_fruit": ["fruits"],
    "minecraft:enchanted_golden_apple": ["fruits", "sugars"],
    "minecraft:glow_berries": ["fruits"],
    "minecraft:golden_apple": ["fruits", "sugars"],
    "minecraft:melon": ["fruits"],
    "minecraft:melon_slice": ["fruits", "sugars"],
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
    "farmer_delight_nullgr:grilled_salmon": ["fruits", "proteins", "vegetables", "sugars"],
    "farmer_delight_nullgr:ham": ["proteins"],
    "farmer_delight_nullgr:hamburger": ["grains", "proteins", "vegetables"],
    "farmer_delight_nullgr:honey_cookie": ["grains", "sugars"],
    "farmer_delight_nullgr:honey_glazed_ham": ["fruits", "grains", "proteins", "vegetables", "sugars"],
    "farmer_delight_nullgr:hot_cocoa": ["proteins", "sugars"],
    "farmer_delight_nullgr:kelp_roll": ["grains", "vegetables"],
    "farmer_delight_nullgr:kelp_roll_slice": ["grains", "vegetables"],
    "farmer_delight_nullgr:melon_juice": ["fruits", "sugars"],
    "farmer_delight_nullgr:melon_popsicle": ["fruits", "sugars"],
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
    "fruitfarmersdelight_nullgr:a_mangosteen": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:a_segment_of_orange": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:baked_pear": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:banana": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:banana_beef": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:banana_egg_roll": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:blueberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:blueberry_yam": ["fruits", "proteins", "vegetables", "sugars"],
    "fruitfarmersdelight_nullgr:braised_pineapple_meat": ["fruits", "proteins", "vegetables", "sugars"],
    "fruitfarmersdelight_nullgr:cake_passion_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:cherry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:cherry_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:dried_persimmon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:durian_meat": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:durian_pizza_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_pean": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:grape": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:grape_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:grape_tiramisu": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:half_a_kiwi": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:half_a_mango": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:half_a_papaya": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:half_a_passion_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:half_a_pitaya": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:hami_melon_fire_sb_bowl": ["fruits", "grains", "vegetables"],
    "fruitfarmersdelight_nullgr:hami_melon_piece": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:haw_sheets": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:hawaiian_pizza_slice": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:hawthorn": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:hawthorn_skewers": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:honey_peach": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_blueberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_grape": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_mulberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jellydrops_blueberry": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:jellydrops_grape": ["fruits", "proteins"],
    "fruitfarmersdelight_nullgr:kiwi_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:lemon_chicken_chop": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:lemon_slice": ["fruits"],
    "fruitfarmersdelight_nullgr:litchi_chicken": ["fruits", "proteins", "vegetables", "sugars"],
    "fruitfarmersdelight_nullgr:liulian_stewed_chicken": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:longan": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:loquat": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:luxurious_fruit_salad": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:lychee": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:mango": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:mango_cake": ["fruits", "grains", "sugars"],
    "fruitfarmersdelight_nullgr:mango_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mango_milk": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mangosteen": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:matcha_strawberry": ["fruits", "grains", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_grape": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_kiwifruit": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:milkshake_passion_fruit": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:mulberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:papaya_milk": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:passion_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:passion_fruit_chicken": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:passion_fruit_pasta": ["fruits", "grains", "sugars"],
    "fruitfarmersdelight_nullgr:passion_fruit_trout": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:pawpaw": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:pear": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:persimmon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:pineapple_drumstick_fort": ["fruits", "grains", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:pineapple_rice": ["fruits", "grains", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:pineapple_slice": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:pineapple_strand": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:pitaya_dragon_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:roasted_durian": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:shaddock_slice": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:steamed_eggs_with_oranges": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:stewed_beef_with_hawthorn": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:stewed_beef_with_red_wine": ["fruits", "grains", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:stewed_pear_with_apple": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:stewed_pear_with_loquat": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:strawberry_boo": ["fruits", "proteins", "vegetables"],
    "fruitfarmersdelight_nullgr:strawberry_custard": ["fruits", "proteins", "sugars"],
    "fruitfarmersdelight_nullgr:strawberry_egg_tart": ["fruits", "grains", "proteins"],
    "fruitfarmersdelight_nullgr:tangerine": ["fruits", "sugars"],
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

    "fruitfarmersdelight_nullgr:forzen_sucker_banana": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_blueberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_cherry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_durian": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_grape": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_hami_melon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_hawthorn": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_kiwifruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_longan": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_loquat": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_lychee": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_mango": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_mangosteen": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_mulberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_papaya": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_passion_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_peach": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_pear": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_persimmon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_pineapple": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_pitaya_dragon_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_shaddock": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:forzen_sucker_strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:forzen_sucker_tangerine": ["fruits", "sugars"],

    "fruitfarmersdelight_nullgr:fruit_juice_banana": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_blueberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_cherry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_grape": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_hami_melon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_hawthorn": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_kiwifruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:fruit_juice_longan": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_loquat": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_lychee": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_mango": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_mangosteen": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_mulberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_papaya": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_passion_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_peach": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_persimmon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_pineapple": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_pitaya_dragon_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_raspberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_shaddock": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_strawberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:fruit_juice_tangerine": ["fruits", "sugars"],

    "fruitfarmersdelight_nullgr:icecream_banana": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_cherry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_durian": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_hami_melon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_hawthorn": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_kiwifruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_longan": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_loquat": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_lychee": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_mango": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_mangosteen": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_papaya": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_passion_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_peach": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_pear": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_persimmon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_pineapple": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_pitaya_dragonfruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_raspberry": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_shaddock": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:icecream_strawberry": ["fruits"],
    "fruitfarmersdelight_nullgr:icecream_tangerine": ["fruits", "sugars"],

    "fruitfarmersdelight_nullgr:jam_banana": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_blueberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_cherry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_durian": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_grape": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_hami_melon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_hawthorn": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_kiwifruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_lemon": ["fruits"],
    "fruitfarmersdelight_nullgr:jam_longan": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_loquat": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_lychee": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_mango": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_mangosteen": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_mulberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_papaya": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_passion_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_peach": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_pear": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_persimmon": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_pineapple": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_pitaya_dragon_fruit": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_raspberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_shaddock": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_strawberry": ["fruits", "sugars"],
    "fruitfarmersdelight_nullgr:jam_tangerine": ["fruits", "sugars"],

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

# FarmerDelightDlc_All 的 85 个行为包已逐项审查；功能性物品、纯调料与重复定义不写入运行配置。
# 数据来源：FarmerDelightDlc_All 仓库 3f1ab82efa9f0cf93a78abeed9339790fb6bb74e，共 2205 个全局唯一条目。
# 按命名空间和营养组压缩书写，加载时还原为与现有配置一致的 itemId -> list 映射。
farmerDelightDlcFoodGroups = {}
for namespacePrefix, groupIds, itemNames in (
    ("argentina_delight_nullgr:", ["fruits", "vegetables"], (
        "mate_glow_berry_item", "mate_lime_item",
    )),
    ("argentina_delight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "mate_apple_item", "mate_berry_item", "mate_melon_item",
    )),
    ("argentina_delight_nullgr:", ["grains"], (
        "tostada",
    )),
    ("argentina_delight_nullgr:", ["grains", "proteins"], (
        "choripan", "hamburguesa", "mandibulabloque_cat", "megadibu_item", "milanesa", "sanguchemila",
    )),
    ("argentina_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "pancondulcedeleche",
    )),
    ("argentina_delight_nullgr:", ["proteins"], (
        "alitasdepollo", "brochetascrudas_cooked_item", "brochetascrudas_cooked_item_1",
        "brochetascrudas_cooked_item_2", "caimanalaparrilla", "carnecordero", "chinchulinesitem", "chorizo",
        "cortemardelplata", "costeleta", "costillar", "costillasdechancho", "hamburguesasola", "muslos", "nalgavaca",
        "panceta", "patadepollo", "patamuslo", "pescadocortado", "vacioitem",
    )),
    ("argentina_delight_nullgr:", ["proteins", "vegetables"], (
        "calabazitarellena", "mate_milk_item",
    )),
    ("argentina_delight_nullgr:", ["proteins", "sugars"], (
        "dulcedeleche",
    )),
    ("argentina_delight_nullgr:", ["vegetables"], (
        "mate_0_item", "mate_item", "paparustica", "rodajasdecalabazasitem",
    )),
    ("argentina_delight_nullgr:", ["vegetables", "sugars"], (
        "mate_sugar_item",
    )),
    ("bakingdelight_nullgr:", ["fruits", "sugars"], (
        "apple_petal", "cherry", "cherry_ice_lolly",
    )),
    ("bakingdelight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "cherry_cake", "cherry_mousse", "golden_apple_mousse",
    )),
    ("bakingdelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "apple_cream", "cherry_cream", "cherry_egg", "steamed_cherry_egg",
    )),
    ("bakingdelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "apple_pudding", "cherry_pudding", "golden_apple_cream",
    )),
    ("bakingdelight_nullgr:", ["grains", "proteins"], (
        "empty_cake",
    )),
    ("bakingdelight_nullgr:", ["grains", "proteins", "vegetables"], (
        "braised_shrimp_ball", "cheese_rice_ball", "crystal_dumpling", "french_onion_soup",
        "seaweed_fried_shrimp_cake",
    )),
    ("bakingdelight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "blue_orchid_flower_cake", "egg_tart", "lilac_cake", "matcha_mousse", "orange_tulip_cake",
        "oxeye_daisy_cake", "pink_tulip_cake", "pumpkin_mousse", "rose_cake", "sunflower_cake", "truffle_egg_tart",
        "white_tulip_cake", "wither_rose_cake",
    )),
    ("bakingdelight_nullgr:", ["grains", "proteins", "sugars"], (
        "chocolate_mousse", "cream_mousse", "mousse_wip",
    )),
    ("bakingdelight_nullgr:", ["proteins"], (
        "cheese_ball", "chicken_fillet", "cream", "cream_bucket", "egg_bowl", "fish_egg", "prawn", "shrimp_paste",
        "steamed_egg", "steamed_fish_egg",
    )),
    ("bakingdelight_nullgr:", ["proteins", "vegetables"], (
        "beef_tomato_cup", "cheese_baked_potato", "cream_of_mushroom_soup", "grilled_sausage",
        "grilled_starch_sausage", "matcha_cream", "onion_ring", "pumpkin_cream", "raw_onion_ring", "sausage",
        "sectioned_sausage", "starch_sausage",
    )),
    ("bakingdelight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "matcha_pudding",
    )),
    ("bakingdelight_nullgr:", ["proteins", "sugars"], (
        "caramel_pudding", "chocolate_cream", "pudding_wip_1", "pudding_wip_2",
    )),
    ("bakingdelight_nullgr:", ["vegetables"], (
        "black_pepper_corn", "black_pepper_dust", "black_truffle", "fried_brown_mushroom", "fried_red_mushroom",
        "mashed_potato", "roasted_sunflower_seed", "sunflower_seed", "sunflower_seed_pulp", "white_truffle",
    )),
    ("bakingdelight_nullgr:", ["vegetables", "sugars"], (
        "chocolate_donut", "donut", "raw_donut", "sauce_mashed_potato",
    )),
    ("bakingdelight_nullgr:", ["sugars"], (
        "caramel", "chocolate_sauce",
    )),
    ("barbecue_delight_nullgr:", ["grains"], (
        "bread_slice_skewer", "toast_skewer",
    )),
    ("barbecue_delight_nullgr:", ["proteins"], (
        "beef_skewer", "chicken_skewer", "cod_skewer", "cooked_beef_skewer", "cooked_chicken_skewer",
        "cooked_cod_skewer", "cooked_mutton_skewer", "cooked_pork_skewer", "cooked_rabbit_skewer",
        "cooked_salmon_skewer", "mutton_skewer", "pork_skewer", "rabbit_skewer", "salmon_skewer",
    )),
    ("barbecue_delight_nullgr:", ["vegetables"], (
        "baked_potato_skewer", "mushroom_skewer", "potato_skewer", "roasted_mushroom_skewer",
    )),
    ("bountiful_harvest:", ["fruits", "grains", "proteins", "vegetables"], (
        "roast_turkey",
    )),
    ("bountiful_harvest:", ["grains"], (
        "corn", "corn_kernel", "grilled_corn", "popcorn",
    )),
    ("bountiful_harvest:", ["grains", "proteins", "sugars"], (
        "cornbread", "cornbread_dough", "pecan_pie_slice",
    )),
    ("bountiful_harvest:", ["grains", "vegetables"], (
        "stuffing",
    )),
    ("bountiful_harvest:", ["proteins"], (
        "cooked_turkey", "pecan", "raw_turkey",
    )),
    ("bountiful_harvest:", ["proteins", "vegetables"], (
        "mashed_potatoes_and_gravy",
    )),
    ("bountiful_harvest:", ["proteins", "vegetables", "sugars"], (
        "sweet_potato_casserole",
    )),
    ("bountiful_harvest:", ["vegetables"], (
        "baked_sweet_potato", "sweet_potato",
    )),
    ("butcher_delight_nullgr:", ["grains", "proteins"], (
        "sextuple_meat_treat",
    )),
    ("butcher_delight_nullgr:", ["proteins"], (
        "black_bunny_ears", "black_bunny_tail", "blood_bucket", "brown_bunny_ears", "brown_bunny_tail",
        "chicken_breast", "chicken_foot", "chicken_leg", "chicken_scraps", "chicken_thigh", "chicken_wattle",
        "cooked_bat_meat", "cooked_chicken_breast", "cooked_chicken_leg", "cooked_chicken_scraps",
        "cooked_chicken_thigh", "cooked_chicken_wing", "cooked_cubed_chicken", "cooked_cubed_goat",
        "cooked_cubed_horse", "cooked_cubed_rabbit", "cooked_frog_hand", "cooked_frog_leg", "cooked_frog_meat",
        "cooked_frog_tough", "cooked_goat_ribs", "cooked_goat_roast", "cooked_goat_scraps", "cooked_goat_steak",
        "cooked_ground_chicken", "cooked_ground_goat", "cooked_ground_horse", "cooked_ground_rabbit",
        "cooked_ground_spider", "cooked_horse_rib", "cooked_horse_ribs", "cooked_horse_roast", "cooked_horse_scraps",
        "cooked_rabbit_front_leg", "cooked_rabbit_saddle", "cooked_rabbit_scraps", "cooked_rabbit_thigh",
        "cooked_silverfish_meat", "cooked_spider_eggs", "cooked_spider_sack", "cooked_spider_scraps",
        "cooked_spider_sinew", "cooked_stew_chicken", "cooked_stew_goat", "cooked_stew_horse", "cooked_stew_rabbit",
        "cooked_villager", "cooked_wattle", "cubed_chicken", "cubed_goat", "cubed_horse", "cubed_rabbit",
        "dried_blood", "eyeball", "frog_hand", "frog_leg", "frog_meat", "frog_tough", "goat_ribs", "goat_roast",
        "goat_scraps", "goat_steak", "gold_bunny_ears", "gold_bunny_tail", "ground_chicken", "ground_goat",
        "ground_horse", "ground_rabbit", "ground_spider", "horse_rib", "horse_ribs", "horse_roast", "horse_scraps",
        "rabbit_front_leg", "rabbit_saddle", "rabbit_scraps", "rabbit_thigh", "raw_bat_meat", "raw_chicken_wing",
        "raw_silverfish_meat", "raw_villager", "raw_witche_leg_slice", "raw_witche_meat_slice", "salt_bunny_ears",
        "salt_bunny_tail", "slime_brain", "slime_meat", "spider_caviar", "spider_eggs", "spider_sack",
        "spider_scraps", "spider_sinew", "splotched_bunny_ears", "splotched_bunny_tail", "stew_chicken", "stew_goat",
        "stew_horse", "stew_rabbit", "villager_jerky", "villager_nose", "white_bunny_ears", "white_bunny_tail",
        "witche_leg_slice", "witche_meat_slice", "zombie_brain", "zombie_hide", "zombie_meat",
    )),
    ("butcher_delight_nullgr:", ["proteins", "vegetables"], (
        "cooked_head_bowl",
    )),
    ("butchercraft_nullgr:", ["fruits", "proteins", "sugars"], (
        "berry_fish_scale",
    )),
    ("butchercraft_nullgr:", ["fruits", "proteins", "vegetables"], (
        "perch_berry_bacca_onion",
    )),
    ("butchercraft_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "baked_bass_with_sauce", "roee_salad",
    )),
    ("butchercraft_nullgr:", ["grains", "proteins"], (
        "cod_liver_mousse", "cod_liver_sushi", "fish_zita",
    )),
    ("butchercraft_nullgr:", ["grains", "proteins", "vegetables"], (
        "cod_feast", "fish_kelp_porridge", "fish_pizza", "fish_roe_vegetable_sushi", "pan_fried_perch",
        "roe_vegetable_sushi", "salmon_feast", "stuff_bread_fish_bone", "tuna_pasta",
    )),
    ("butchercraft_nullgr:", ["grains", "proteins", "sugars"], (
        "rice_with_perch_in_honey_sauce",
    )),
    ("butchercraft_nullgr:", ["proteins"], (
        "air_bladder", "butter", "cod_liver", "cod_sausage", "cooked_cod_sausage", "cooked_perch_intestine",
        "cooked_salmon_sausage", "cooked_shark_fin", "cooked_tuna_sausage", "fish_bone_marrow", "fish_bone_stock",
        "fish_eye", "fish_gall_bladder", "fish_gills", "fish_intestines", "perch_intestine", "roe", "roe_egg",
        "salmon_sausage", "shark_fin", "tuna_sausage",
    )),
    ("butchercraft_nullgr:", ["proteins", "vegetables"], (
        "carrot_fish_soup", "ffish_with_potato_pancakes", "fish_cai_barbecue", "fish_eye_soup",
        "fish_maw_five_son_soup", "fish_zhu", "fishbone_seaweed_soup", "prok_with_bladder", "sour_soup_bass",
        "spicy_perch", "stuff_fish_tomato", "stuff_tofu_mushroom", "stuffed_bass", "tartar_sauce",
        "tofu_with_fish_head", "tomato_onion_fish_slice", "vegetable_fish",
    )),
    ("butchercraft_nullgr:", ["proteins", "sugars"], (
        "sugar_egg",
    )),
    ("cake_delight_nulgr:", ["grains", "proteins", "sugars"], (
        "muffins_item", "oreo_item",
    )),
    ("cake_delight_nulgr:", ["grains", "sugars"], (
        "sandy_biscuit",
    )),
    ("casualness_delight_nullgr:", ["grains"], (
        "roast_gluten",
    )),
    ("casualness_delight_nullgr:", ["grains", "proteins"], (
        "quiche_lorraine_slice", "stargazy_pie_slice",
    )),
    ("casualness_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "beef_noodles", "bowl_of_fried_dumpling", "donkey_burger", "fish_and_chips", "fried_dumpling",
        "raw_fried_dumpling", "raw_spring_roll", "spicy_strips", "spring_roll", "yorkshire_pudding",
    )),
    ("casualness_delight_nullgr:", ["grains", "vegetables", "sugars"], (
        "bowl_of_sweet_rice",
    )),
    ("casualness_delight_nullgr:", ["proteins"], (
        "chicken_bobo_chicken", "cooked_donkey_meat", "fried_chicken_chip", "fried_fish", "phantom_puff",
        "raw_chicken_bobo_chicken", "raw_donkey_meat", "tonkatsu",
    )),
    ("casualness_delight_nullgr:", ["proteins", "vegetables"], (
        "bowl_of_paper_wrapped_fish", "cheese_wheel_slice", "phantom_dumplings",
    )),
    ("casualness_delight_nullgr:", ["vegetables"], (
        "cabbage_bobo_chicken", "potato_bobo_chicken", "potato_chip", "potato_slice", "raw_cabbage_bobo_chicken",
        "raw_potato_bobo_chicken",
    )),
    ("casualness_delight_nullgr:", ["sugars"], (
        "green_tongue",
    )),
    ("coconut_delight_nullgr:", ["fruits"], (
        "bowl_coconut_fishing", "coconut", "coconut_ice_cream", "coconut_meat", "coconut_water", "shredded_coconut",
    )),
    ("coconut_delight_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "salty_stir_fry",
    )),
    ("coconut_delight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "coconut_bread", "coconut_muffins",
    )),
    ("coconut_delight_nullgr:", ["fruits", "grains", "vegetables"], (
        "coconut_rice",
    )),
    ("coconut_delight_nullgr:", ["fruits", "proteins"], (
        "coconut_chicken",
    )),
    ("coconut_delight_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "cocnut_milkfish", "coconut_chicken_bowl", "coconut_milk",
    )),
    ("coconut_delight_nullgr:", ["fruits", "proteins", "sugars"], (
        "coconut_bowl", "coconut_cake_slice", "coconut_crisp", "coconut_egg", "coconut_sugar",
    )),
    ("coconut_delight_nullgr:", ["fruits", "sugars"], (
        "coconut_grains", "coconut_milk_sauce",
    )),
    ("coconut_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "bread_dipped_crab_paste",
    )),
    ("coconut_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "crab_sticks",
    )),
    ("coconut_delight_nullgr:", ["proteins"], (
        "coconut_crab", "coconut_crab_claws", "coconut_crab_claws_cooked", "coconut_crab_leg",
        "coconut_crab_leg_cooked", "coconut_crab_meat", "coconut_crab_meat_cooked",
    )),
    ("coconut_delight_nullgr:", ["proteins", "vegetables"], (
        "charcoal_grilled_crab_claws", "charcoal_grilled_crab_legs", "crab_meat_casserole",
    )),
    ("collectors_delight_nullgr:", ["fruits"], (
        "lime", "lime_ice_cream", "lime_popsicle", "lime_slice", "pomegranate_bean_salad",
    )),
    ("collectors_delight_nullgr:", ["fruits", "grains"], (
        "lime_cookie",
    )),
    ("collectors_delight_nullgr:", ["fruits", "grains", "proteins", "vegetables"], (
        "carbonara_pasta", "platinum_bass_stew", "platinum_bass_stew_cup", "stuffed_pasta_shells",
    )),
    ("collectors_delight_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "coffee_cannoli", "honey_lime_chicken",
    )),
    ("collectors_delight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "cannoli", "lime_cake_slice", "lime_pie_slice", "lucuma_cake_slice", "lucuma_cannoli", "panettone_slice",
        "pink_dragon_fruit_cake_slice", "pomegranate_cake_slice",
    )),
    ("collectors_delight_nullgr:", ["fruits", "grains", "vegetables"], (
        "pink_noodles", "potato_fritters",
    )),
    ("collectors_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "lucuma_bread",
    )),
    ("collectors_delight_nullgr:", ["fruits", "proteins"], (
        "apple_gummy", "banana_gummy", "lime_gummy", "lucuma_gummy", "melon_gummy", "passionfruit_gummy",
        "pink_dragon_fruit_gummy", "pomegranate_gummy", "salmon_tartare", "strawberry_gummy",
    )),
    ("collectors_delight_nullgr:", ["fruits", "proteins", "vegetables"], (
        "bullet_pepper_popper", "cod_ceviche", "dragon_stew", "dragon_stew_cup", "glazed_strider",
        "mediterranean_salmon", "pomegranate_chicken", "pomegranate_mutton", "prawn_spread", "spicy_grenadine_jelly",
    )),
    ("collectors_delight_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "pomegranate_pork",
    )),
    ("collectors_delight_nullgr:", ["fruits", "proteins", "sugars"], (
        "dragons_passion", "lime_milkshake", "lucuma_ice_cream", "lucuma_milkshake", "lucuma_pudding",
        "pink_dragon_fruit_milkshake", "pomegranate_custard", "pomegranate_milkshake", "salmon_wrapped_prawn",
    )),
    ("collectors_delight_nullgr:", ["fruits", "vegetables"], (
        "crimson_carrot_roast", "lime_green_tea", "lucuma_gazpacho", "lucuma_gazpacho_cup",
    )),
    ("collectors_delight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "chocolate_arils", "deluxe_salad", "mint_limeade", "pomegranate_black_tea",
    )),
    ("collectors_delight_nullgr:", ["fruits", "sugars"], (
        "berry_limeade", "candied_lime", "dried_pink_dragon_fruit", "gilded_lucuma", "limeade", "lucuma",
        "pink_dragon_fruit", "pink_dragon_fruit_ice_cream", "pink_limeade", "pomegranate", "pomegranate_ice_cream",
        "pomegranate_slice", "pomegranate_smoothie", "shimmering_apple", "strong_limeade", "stygian_pomegranate",
    )),
    ("collectors_delight_nullgr:", ["grains", "proteins"], (
        "clam_roll", "prawn_roll",
    )),
    ("collectors_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "big_rice_ball", "clam_pasta", "crab_lasagna", "crab_noodles", "portobello_pasta", "portobello_quiche_slice",
        "portobello_risotto", "prawn_noodles", "prawn_po_boy", "uni_roll",
    )),
    ("collectors_delight_nullgr:", ["grains", "vegetables"], (
        "portobello_burger", "portobello_rice_soup", "portobello_rice_soup_cup", "portobello_wrap",
        "stuffed_portobello_cap",
    )),
    ("collectors_delight_nullgr:", ["proteins"], (
        "buttered_legs", "chieftain_claw", "chieftain_crab_meat", "chieftain_leg", "clam_meat",
        "cooked_platinum_bass", "cooked_platinum_bass_head", "cooked_platinum_bass_slice", "cooked_tiger_prawn",
        "crab_miso", "platinum_bass", "platinum_bass_head", "platinum_bass_slice", "tiger_prawn", "uni",
    )),
    ("collectors_delight_nullgr:", ["proteins", "vegetables"], (
        "adzuki_gummy", "aloe_gummy", "black_tea_gummy", "chocolate_gummy", "clam_chowder", "clam_meatball_stew",
        "clam_meatball_stew_cup", "coffee_gummy", "fish_mix", "green_tea_gummy", "hemp_gummy", "mint_gummy",
        "prawn_ceviche", "prawn_stew", "prawn_stew_cup", "pumpkin_gummy", "yellow_tea_gummy", "yucca_gummy",
    )),
    ("collectors_delight_nullgr:", ["vegetables"], (
        "baked_portobello_cap",
    )),
    ("corn_delight:", ["fruits", "grains", "proteins"], (
        "classic_corn_dog",
    )),
    ("corn_delight:", ["fruits", "grains", "proteins", "vegetables"], (
        "cornbread_stuffing",
    )),
    ("corn_delight:", ["grains"], (
        "boiled_corn", "corn_kernel", "grilled_corn", "maize", "popcorn", "raw_tortilla", "tortilla",
        "tortilla_chip",
    )),
    ("corn_delight:", ["grains", "proteins"], (
        "corn_dog", "cornbread", "cornbread_batter", "creamed_corn", "nachos",
    )),
    ("corn_delight:", ["grains", "proteins", "vegetables"], (
        "corn_soup", "taco",
    )),
    ("corn_delight:", ["grains", "proteins", "sugars"], (
        "creamy_corn_drink",
    )),
    ("corn_delight:", ["grains", "sugars"], (
        "caramel_popcorn",
    )),
    ("crabber_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "bisque", "crab_cakes", "seafood_gumbo", "shrimp_fried_rice", "stuffed_nautilus_shell",
    )),
    ("crabber_delight_nullgr:", ["proteins"], (
        "arid_flesh", "clawster", "cooked_clam_meat", "cooked_clawster", "cooked_crab", "cooked_frog_leg",
        "cooked_glow_squid_tentacles", "cooked_pufferfish_slice", "cooked_shrimp", "cooked_squid_tentacles",
        "cooked_tropical_fish", "cooked_tropical_fish_slice", "coral_crunch", "crab", "crab_claw", "crab_legs",
        "fish_stick", "pufferfish_slice", "raw_clam_meat", "raw_frog_leg", "raw_glow_squid_tentacles",
        "raw_squid_tentacles", "shrimp", "soggy_flesh", "tropical_fish_slice",
    )),
    ("crabber_delight_nullgr:", ["proteins", "vegetables"], (
        "clam_bake", "clam_chowder", "frog_leg_kebob", "shrimp_skewer", "squid_kebob", "surf_and_turf",
    )),
    ("crabber_delight_nullgr:", ["vegetables"], (
        "jar_of_pickles",
    )),
    ("crabber_delight_nullgr:", ["vegetables", "sugars"], (
        "kelp_shake", "sea_pickle_juice",
    )),
    ("cultural_delight_nullgr:", ["fruits"], (
        "avocado", "cut_avocado",
    )),
    ("cultural_delight_nullgr:", ["fruits", "grains"], (
        "avocado_toast",
    )),
    ("cultural_delight_nullgr:", ["fruits", "grains", "proteins", "vegetables"], (
        "beef_burrito", "rice_ball",
    )),
    ("cultural_delight_nullgr:", ["fruits", "grains", "vegetables"], (
        "hearty_salad", "midori_roll", "midori_roll_slice",
    )),
    ("cultural_delight_nullgr:", ["grains"], (
        "corn_cob", "corn_dough", "popcorn", "smoked_corn", "tortilla", "tortilla_chips",
    )),
    ("cultural_delight_nullgr:", ["grains", "proteins"], (
        "creamed_corn", "elote",
    )),
    ("cultural_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "chicken_roll", "chicken_roll_slice", "chicken_taco", "egg_roll", "empanada", "fish_taco", "mutton_sandwich",
        "pork_wrap", "pufferfish_roll", "spicy_curry", "tropical_roll",
    )),
    ("cultural_delight_nullgr:", ["grains", "vegetables"], (
        "eggplant_burger", "fried_eggplant_pasta",
    )),
    ("cultural_delight_nullgr:", ["vegetables"], (
        "cucumber", "cut_cucumber", "cut_eggplant", "eggplant", "smoked_cut_eggplant", "smoked_eggplant",
        "smoked_tomato", "smoked_white_eggplant", "white_eggplant",
    )),
    ("cultural_delight_nullgr:", ["vegetables", "sugars"], (
        "cut_pickle", "pickle",
    )),
    ("delightful_nullgr:", ["fruits"], (
        "salmonberries",
    )),
    ("delightful_nullgr:", ["fruits", "sugars"], (
        "cantaloupe_popsicle", "cantaloupe_slice",
    )),
    ("delightful_nullgr:", ["fruits", "grains"], (
        "cantaloupe_bread",
    )),
    ("delightful_nullgr:", ["fruits", "grains", "proteins"], (
        "chorus_muffin",
    )),
    ("delightful_nullgr:", ["fruits", "grains", "proteins", "vegetables"], (
        "sinigang", "stuffed_cantaloupe",
    )),
    ("delightful_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "deluxe_cheeseburger",
    )),
    ("delightful_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "chorus_pie_slice", "nut_butter_and_jelly_sandwich", "salmonberry_pie_slice",
    )),
    ("delightful_nullgr:", ["fruits", "proteins"], (
        "cantaloupe_gummy", "salmonberry_gummy",
    )),
    ("delightful_nullgr:", ["fruits", "proteins", "vegetables"], (
        "coconut_curry", "field_salad",
    )),
    ("delightful_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "berry_matcha_latte",
    )),
    ("delightful_nullgr:", ["fruits", "proteins", "sugars"], (
        "rock_candy", "salmonberry_ice_cream", "salmonberry_milkshake", "wrapped_cantaloupe",
    )),
    ("delightful_nullgr:", ["grains", "proteins", "vegetables"], (
        "cheeseburger",
    )),
    ("delightful_nullgr:", ["grains", "proteins", "sugars"], (
        "chunkwich",
    )),
    ("delightful_nullgr:", ["grains", "sugars"], (
        "smore",
    )),
    ("delightful_nullgr:", ["proteins"], (
        "acorn", "cooked_goat", "raw_goat", "roasted_acorn",
    )),
    ("delightful_nullgr:", ["proteins", "vegetables"], (
        "crab_rangoon", "matcha_gummy",
    )),
    ("delightful_nullgr:", ["proteins", "vegetables", "sugars"], (
        "matcha_ice_cream", "matcha_latte", "matcha_milkshake", "pumpkin_pie_slice",
    )),
    ("delightful_nullgr:", ["proteins", "sugars"], (
        "nut_butter_bottle",
    )),
    ("delightful_nullgr:", ["vegetables"], (
        "azalea_tea", "cactus_chili", "cactus_flesh", "cactus_soup", "cactus_soup_cup", "cactus_steak",
        "chopped_clover",
    )),
    ("delightful_nullgr:", ["sugars"], (
        "cooked_marshmallow_stick", "marshmallow_stick",
    )),
    ("dragon_boat_festival_nullgr:", ["fruits", "sugars"], (
        "jujube",
    )),
    ("dragon_boat_festival_nullgr:", ["fruits", "grains", "sugars"], (
        "raw_zongzi_jujube", "zongzi_jujube",
    )),
    ("dragon_boat_festival_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "jujube_porridge",
    )),
    ("dragon_boat_festival_nullgr:", ["grains", "proteins"], (
        "itemraw_zongzi_black_bean", "raw_zongzi_egg", "raw_zongzi_green_bean", "raw_zongzi_meat",
        "zongzi_black_bean", "zongzi_egg", "zongzi_green_bean", "zongzi_meat",
    )),
    ("dragon_boat_festival_nullgr:", ["grains", "proteins", "vegetables"], (
        "green_society",
    )),
    ("dragon_boat_festival_nullgr:", ["proteins"], (
        "black_bean", "green_bean", "salted_egg", "salty_yolk",
    )),
    ("dragon_boat_festival_nullgr:", ["proteins", "sugars"], (
        "green_bean_paste", "green_juice", "soy_milk",
    )),
    ("dumpling_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "beef_tomato_boiled_dumpling", "calamari_boiled_dumpling", "chicken_mush_boiled_dumpling",
        "cod_boiled_dumpling", "dandelion_leaf_boiled_dumpling", "eggplant_egg_boiled_dumpling",
        "garlic_chive_egg_dumpling", "lamb_boiled_dumpling", "pork_cabbage_boiled_dumpling", "pork_cabbage_wonton",
        "pork_carrot_wonton", "pork_celery_boiled_dumpling", "pork_fennel_boiled_dumpling",
        "pork_kelp_boiled_dumpling", "pork_mushroom_wonton", "pork_potato_boiled_dumpling",
        "pufferfish_boiled_dumpling", "rabbit_meat_boiled_dumpling", "salmon_boiled_dumpling",
        "tomato_egg_boiled_dumpling",
    )),
    ("dumpling_delight_nullgr:", ["grains", "vegetables"], (
        "fungus_boiled_dumpling", "garlic_bread", "garlic_rice_with_cauliflower", "mushroom_boiled_dumpling",
    )),
    ("dumpling_delight_nullgr:", ["proteins", "vegetables"], (
        "garlic_baked_cod", "garlic_chicken_stew",
    )),
    ("dumpling_delight_nullgr:", ["vegetables"], (
        "fennel", "fennel_cutting", "garlic", "garlic_chive", "garlic_chive_cutting", "garlic_chop", "garlic_clove",
        "garlic_stuffed_mushrooms", "greenonion", "greenonion_cutting",
    )),
    ("ender_delight_nullgr:", ["fruits"], (
        "chorus_fruit_grain", "chorus_fruit_popsicle",
    )),
    ("ender_delight_nullgr:", ["fruits", "grains"], (
        "chorus_cookie",
    )),
    ("ender_delight_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "chorus_fruit_pie_slice",
    )),
    ("ender_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "stuffed_rice_cake",
    )),
    ("ender_delight_nullgr:", ["fruits", "proteins"], (
        "bubble_tea", "chorus_fruit_milk_tea",
    )),
    ("ender_delight_nullgr:", ["fruits", "proteins", "vegetables"], (
        "dragon_leg_with_sauce", "dragon_meat_stew", "ender_noodle", "ender_sausage", "grilled_shulker",
        "raw_ender_sausage", "roasted_dragon_steak", "steamed_dragon_egg",
    )),
    ("ender_delight_nullgr:", ["fruits", "vegetables"], (
        "assorted_salad", "dragon_breath_and_chorus_soup", "end_mixed_salad",
    )),
    ("ender_delight_nullgr:", ["fruits", "sugars"], (
        "chorus_fruit_wine",
    )),
    ("ender_delight_nullgr:", ["grains", "proteins"], (
        "ender_congee",
    )),
    ("ender_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "ender_bamboo_rice",
    )),
    ("ender_delight_nullgr:", ["grains", "vegetables", "sugars"], (
        "chorus_flower_pie",
    )),
    ("ender_delight_nullgr:", ["proteins"], (
        "dragon_leg", "dried_endermite_meat", "enderman_gristle", "fried_dragon_egg", "liquid_dragon_egg",
        "raw_dragon_meat", "raw_dragon_meat_cuts", "raw_ender_mite_meat", "roasted_dragon_meat",
        "roasted_dragon_meat_cuts", "roasted_shulker_meat", "roasted_shulker_meat_slice", "shulker_meat",
        "shulker_meat_slice", "shulker_omelette", "smoked_dragon_leg",
    )),
    ("ender_delight_nullgr:", ["proteins", "vegetables"], (
        "end_barbecue_stick", "enderman_gristle_stew", "shulker_omelette_mixture", "shulker_soup",
        "stir_fried_shulker_meat",
    )),
    ("ender_delight_nullgr:", ["vegetables"], (
        "chorus_flower_tea",
    )),
    ("ender_delight_nullgr:", ["sugars"], (
        "itemdragon_breath_soda",
    )),
    ("endersdelight:", ["fruits", "grains"], (
        "pearl_pasta_wood",
    )),
    ("endersdelight:", ["fruits", "grains", "proteins"], (
        "crawling_sandwich", "twisted_cereal", "twisted_cereal_wood",
    )),
    ("endersdelight:", ["fruits", "grains", "proteins", "sugars"], (
        "uncanny_cookies",
    )),
    ("endersdelight:", ["fruits", "proteins", "vegetables"], (
        "chorus_stew", "crispy_skewer",
    )),
    ("endersdelight:", ["fruits", "proteins", "sugars"], (
        "chorus_pie_slice", "chorus_stew_wood",
    )),
    ("endersdelight:", ["fruits", "sugars"], (
        "chorus_juice",
    )),
    ("endersdelight:", ["grains"], (
        "strange_eclair",
    )),
    ("endersdelight:", ["grains", "proteins"], (
        "ender_paella",
    )),
    ("endersdelight:", ["grains", "proteins", "vegetables"], (
        "chicken_curry", "stuffed_shulker_bowl",
    )),
    ("endersdelight:", ["grains", "proteins", "sugars"], (
        "ender_paella_wood",
    )),
    ("endersdelight:", ["grains", "vegetables"], (
        "pearl_pasta",
    )),
    ("endersdelight:", ["proteins"], (
        "enderman_sight", "endermite_stew", "mite_crust", "shulker_filet", "shulker_mollusk", "sight_fragment",
    )),
    ("endersdelight:", ["proteins", "vegetables"], (
        "steak_fries",
    )),
    ("endersdelight:", ["proteins", "vegetables", "sugars"], (
        "endermite_stew_wood",
    )),
    ("endersdelight:", ["vegetables"], (
        "amberveil_stew", "amberveiled_curry", "amberveils", "chorusflame", "ethereal_saffron",
        "veil_of_flames_risotto", "voidpepper",
    )),
    ("expanded_delight_nullgr:", ["fruits"], (
        "cranberries",
    )),
    ("expanded_delight_nullgr:", ["fruits", "grains", "proteins"], (
        "cranberry_goat_cheese_toast",
    )),
    ("expanded_delight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "berry_sweet_roll", "cranberry_cobbler_slice", "glow_berry_jelly_sandwich", "glow_berry_sweet_roll",
        "sugar_cookie", "sweet_berry_jelly_sandwich",
    )),
    ("expanded_delight_nullgr:", ["fruits", "proteins"], (
        "glow_berry_jelly",
    )),
    ("expanded_delight_nullgr:", ["fruits", "proteins", "sugars"], (
        "sweet_berry_jelly",
    )),
    ("expanded_delight_nullgr:", ["fruits", "proteins", "vegetables"], (
        "cranberry_chicken", "peanut_salad",
    )),
    ("expanded_delight_nullgr:", ["fruits", "vegetables"], (
        "sweet_potato_salad",
    )),
    ("expanded_delight_nullgr:", ["fruits", "sugars"], (
        "cinnamon_apples", "cranberry_jelly", "cranberry_juice", "glow_berry_juice", "sweet_berry_juice",
    )),
    ("expanded_delight_nullgr:", ["grains"], (
        "cinnamon_rice",
    )),
    ("expanded_delight_nullgr:", ["grains", "proteins"], (
        "cheese_sandwich", "grilled_cheese", "mac_and_cheese",
    )),
    ("expanded_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "chocolate_cookie", "honeyed_goat_cheese_tart_slice", "peanut_butter_honey_sandwich",
        "peanut_butter_sandwich", "snickerdoodle", "sweet_roll",
    )),
    ("expanded_delight_nullgr:", ["grains", "vegetables"], (
        "asparagus_mushroom_pasta", "peperonata",
    )),
    ("expanded_delight_nullgr:", ["proteins"], (
        "cheese_slice",
    )),
    ("expanded_delight_nullgr:", ["proteins", "vegetables"], (
        "asparagus_and_bacon_cheesy", "asparagus_soup_creamy",
    )),
    ("expanded_delight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "sweet_potato_casserole",
    )),
    ("expanded_delight_nullgr:", ["proteins", "sugars"], (
        "peanut_butter", "peanut_honey_soup",
    )),
    ("expanded_delight_nullgr:", ["vegetables"], (
        "asparagus", "baked_sweet_potato", "chili_pepper", "sweet_potato",
    )),
    ("expanded_delight_nullgr:", ["vegetables", "sugars"], (
        "asparagus_soup",
    )),
    ("extravagantdelight_nullgr:", ["fruits"], (
        "boiled_quince", "boiled_quince_pulp", "green_mango", "green_mango_slice", "quince", "sloe_berries",
        "starfruit", "starfruit_slice",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "grains", "proteins"], (
        "mango_chicken_sandwich",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "sloe_treacle_tart_slice", "starfruit_cheesecake_slice", "sweet_berry_yogurt", "sweet_quince_tart_slice",
        "tropical_pizza_slice",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "grains", "vegetables"], (
        "mango_liquor", "sloe_vodka", "starfruit_paloma",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "grains", "vegetables", "sugars"], (
        "sloe_gin",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "grains", "sugars"], (
        "quince_cookie", "sloe_berry_cupcake", "starfruit_muffin",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "proteins"], (
        "green_mango_frappe",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "proteins", "vegetables"], (
        "battered_fish_n_chips", "mango_gazpacho", "starfruit_salmon",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "apple_yogurt", "blueberry_yogurt", "glow_berry_gummy", "glow_berry_yogurt", "mango_cake_slice",
        "mango_glazed_pork", "mango_gummy", "mango_ice_cream", "mango_milkshake", "mango_yogurt", "quince_ice_cream",
        "quince_milkshake", "raspberry_yogurt", "sloe_berry_ice_cream", "sloe_berry_milkshake", "sloe_berry_yogurt",
        "starfruit_gummy", "starfruit_ice_cream", "starfruit_milkshake", "starfruit_yogurt", "strawberry_yogurt",
        "sweet_berry_gummy",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "vegetables"], (
        "mango_salad", "starfruit_salad",
    )),
    ("extravagantdelight_nullgr:", ["fruits", "sugars"], (
        "apple_candy", "glow_berry_lollipop", "mango_candy", "mango_jam", "mango_juice", "mango_lollipop",
        "lush_mango", "lush_mango_slice", "mango_popsicle", "mango_wine", "melon_candy", "quince_candy", "quince_jelly",
        "quince_juice", "quince_lollipop",
        "quince_wine", "sloe_berry_jelly", "sloe_berry_juice", "sloe_berry_lollipop", "sloe_berry_wine",
        "starfruit_candy", "starfruit_jam", "starfruit_juice", "starfruit_lollipop", "starfruit_popsicle", "starfruit_wine",
        "strawberry_lollipop", "sweet_berry_lollipop",
    )),
    ("extravagantdelight_nullgr:", ["grains"], (
        "black_beer", "malt_bread", "malt_cookie",
    )),
    ("extravagantdelight_nullgr:", ["grains", "proteins"], (
        "beer_steak",
    )),
    ("extravagantdelight_nullgr:", ["grains", "proteins", "vegetables"], (
        "beer_beef_stew",
    )),
    ("extravagantdelight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "rhubarb_tart_slice",
    )),
    ("extravagantdelight_nullgr:", ["grains", "proteins", "sugars"], (
        "malt_cake_slice",
    )),
    ("extravagantdelight_nullgr:", ["grains", "vegetables"], (
        "india_pale_ale", "malt_stew", "pale_ale", "rhubarb_liquor",
    )),
    ("extravagantdelight_nullgr:", ["grains", "vegetables", "sugars"], (
        "hop_bread", "pink_gin", "porter_beer", "porter_brownie", "rhubarb_gin",
    )),
    ("extravagantdelight_nullgr:", ["grains", "sugars"], (
        "malt_muffin", "sloe_berry_cookie",
    )),
    ("extravagantdelight_nullgr:", ["proteins"], (
        "marinated_lamb_chops",
    )),
    ("extravagantdelight_nullgr:", ["proteins", "vegetables"], (
        "rhubarb_pork_loin",
    )),
    ("extravagantdelight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "hereford_hop_cheese_wedge", "rhubarb_gummy", "rhubarb_ice_cream", "rhubarb_milkshake",
    )),
    ("extravagantdelight_nullgr:", ["proteins", "sugars"], (
        "honey_gummy",
    )),
    ("extravagantdelight_nullgr:", ["vegetables"], (
        "rhubarb",
    )),
    ("extravagantdelight_nullgr:", ["vegetables", "sugars"], (
        "mint_lollipop", "rhubarb_candy", "rhubarb_jam", "rhubarb_wine",
    )),
    ("extravagantdelight_nullgr:", ["sugars"], (
        "honey_candy",
    )),
    ("farmer_respite_nullgr:", ["fruits"], (
        "rose_hip_tea",
    )),
    ("farmer_respite_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "rose_hip_pie_slice",
    )),
    ("farmer_respite_nullgr:", ["fruits", "sugars"], (
        "rose_hip_tea_honey",
    )),
    ("farmer_respite_nullgr:", ["grains", "proteins", "vegetables"], (
        "black_cod", "tea_curry",
    )),
    ("farmer_respite_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "coffee_cake_slice",
    )),
    ("farmer_respite_nullgr:", ["grains", "vegetables"], (
        "green_tea_cookie",
    )),
    ("farmer_respite_nullgr:", ["proteins", "vegetables"], (
        "black_tea_milk", "blazing_chili", "coffee_milk", "dandelion_tea_milk", "green_tea_milk", "purulent_tea",
        "yellow_tea_milk",
    )),
    ("farmer_respite_nullgr:", ["proteins", "vegetables", "sugars"], (
        "purulent_tea_honey",
    )),
    ("farmer_respite_nullgr:", ["vegetables"], (
        "black_tea", "coffee", "dandelion_tea", "green_tea", "nether_wart_sourdough", "yellow_tea",
    )),
    ("farmer_respite_nullgr:", ["vegetables", "sugars"], (
        "black_tea_honey", "coffe_honey", "green_tea_honey", "yellow_tea_honey",
    )),
    ("fastfood_delight_nullgr:", ["fruits", "proteins", "sugars"], (
        "apple_sauce",
    )),
    ("fastfood_delight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "fruit_ice_cream",
    )),
    ("fastfood_delight_nullgr:", ["fruits", "sugars"], (
        "lemon_soda", "sweet_berry_ice_cream",
    )),
    ("fastfood_delight_nullgr:", ["grains", "proteins"], (
        "cod_sandwich", "croque_monsieur", "salmon_sandwich",
    )),
    ("fastfood_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "cheese_wrap", "cheeseburger", "chicken_cheese_sandwich", "chicken_wrap", "pork_sandwich", "rabbit_sandwich",
    )),
    ("fastfood_delight_nullgr:", ["proteins"], (
        "cheese", "chicken_nuggets",
    )),
    ("fastfood_delight_nullgr:", ["vegetables"], (
        "beet_fries", "carrot_fries", "french_fries", "fried_onions",
    )),
    ("fastfood_delight_nullgr:", ["vegetables", "sugars"], (
        "creaming_soda", "iced_tea", "orange_soda",
    )),
    ("fastfood_delight_nullgr:", ["sugars"], (
        "chocolate_ice_cream", "cola_soda", "ice_cream",
    )),
    ("festive_delight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "festive_chicken",
    )),
    ("festive_delight_nullgr:", ["fruits", "sugars"], (
        "christmas_tea",
    )),
    ("festive_delight_nullgr:", ["sugars"], (
        "sugar_cane",
    )),
    ("festive_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "longevity_noodle", "spring_rolls",
    )),
    ("festive_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "dought_gingerbread_cookie_block", "gingerbread", "gingerbread_cookie_block", "gingerbread_cookie_creeper",
        "gingerbread_cookie_creeper_sugar", "gingerbread_cookie_star", "gingerbread_man", "icing_snow_cookie",
        "icing_sword_cookie", "snow_cookie", "sword_cookie",
    )),
    ("festive_delight_nullgr:", ["proteins"], (
        "salmon_verrines",
    )),
    ("foragersinsight_nullgr:", ["fruits"], (
        "rose_hip",
    )),
    ("foragersinsight_nullgr:", ["fruits", "grains"], (
        "rose_cookie",
    )),
    ("foragersinsight_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "jammy_breakfast_sandwich",
    )),
    ("foragersinsight_nullgr:", ["fruits", "grains", "vegetables"], (
        "rose_roasted_roots",
    )),
    ("foragersinsight_nullgr:", ["fruits", "grains", "vegetables", "sugars"], (
        "seed_butter_jamwich",
    )),
    ("foragersinsight_nullgr:", ["fruits", "proteins", "sugars"], (
        "foragers_granola",
    )),
    ("foragersinsight_nullgr:", ["fruits", "vegetables"], (
        "glowing_carrot_juice", "meadow_medley", "rose_cordial",
    )),
    ("foragersinsight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "rose_granita",
    )),
    ("foragersinsight_nullgr:", ["fruits", "sugars"], (
        "apple_slice", "caramel_apple_slice",
    )),
    ("foragersinsight_nullgr:", ["grains", "proteins"], (
        "acorn_cookie", "acorn_dough", "acorn_noodles",
    )),
    ("foragersinsight_nullgr:", ["grains", "proteins", "vegetables"], (
        "creamy_salmon_bagel", "seaside_sizzler",
    )),
    ("foragersinsight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "slice_of_acorn_carrot_cake",
    )),
    ("foragersinsight_nullgr:", ["grains", "vegetables"], (
        "poppy_seed_bagel", "poppy_seed_jam_cookie", "steamy_kelp_rice",
    )),
    ("foragersinsight_nullgr:", ["grains", "vegetables", "sugars"], (
        "red_velvet_cupcake",
    )),
    ("foragersinsight_nullgr:", ["grains", "sugars"], (
        "black_forest_muffin",
    )),
    ("foragersinsight_nullgr:", ["proteins"], (
        "acorn_meal", "black_acorn", "cooked_rabbit_leg", "raw_rabbit_leg",
    )),
    ("foragersinsight_nullgr:", ["proteins", "vegetables"], (
        "cod_and_pumpkin_stew", "dandelion_root_tea", "kelp_and_beet_salad", "kelp_wrap",
    )),
    ("foragersinsight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "sweet_roasted_rabbit_leg",
    )),
    ("foragersinsight_nullgr:", ["vegetables"], (
        "carrot_poppy_chowder", "dandelion_fries", "dandelion_root", "dandelion_saute", "green_sauce", "rose_petals",
        "seed_milk_bottle", "seed_milk_bucket", "sunflower_butter", "sunflower_kernels",
    )),
    ("frightsdelight_nullgr:", ["fruits"], (
        "soul_berry", "wither_berry",
    )),
    ("frightsdelight_nullgr:", ["fruits", "grains"], (
        "cookie_soul_berry",
    )),
    ("frightsdelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "apple_slime",
    )),
    ("frightsdelight_nullgr:", ["fruits", "proteins", "vegetables"], (
        "soup_rotten_flesh", "soup_slime",
    )),
    ("frightsdelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "punch_slimeapple",
    )),
    ("frightsdelight_nullgr:", ["fruits", "sugars"], (
        "apple_candy", "punch_soul_berry", "punch_wither_berry",
    )),
    ("frightsdelight_nullgr:", ["grains", "proteins"], (
        "cookie_flesh", "cookie_spidereye", "pasta_with_slimeballs",
    )),
    ("frightsdelight_nullgr:", ["proteins"], (
        "monster_mash", "undead_kebab", "web_on_stick",
    )),
    ("frightsdelight_nullgr:", ["proteins", "vegetables"], (
        "soup_spider_eye",
    )),
    ("frightsdelight_nullgr:", ["proteins", "sugars"], (
        "punch_ghasttear", "punch_spidereye",
    )),
    ("frycooking_delight_nullgr:", ["grains"], (
        "plain_donut",
    )),
    ("frycooking_delight_nullgr:", ["proteins"], (
        "fried_chicken_leg", "fried_fish_slice",
    )),
    ("frycooking_delight_nullgr:", ["vegetables"], (
        "canola", "fried_onion_ring", "fried_potato",
    )),
    ("green_delight_nullgr:", ["fruits"], (
        "cactus_fruit_item",
    )),
    ("green_delight_nullgr:", ["grains", "proteins"], (
        "creeper_cookie",
    )),
    ("green_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "bamboo_pasta",
    )),
    ("green_delight_nullgr:", ["grains", "vegetables"], (
        "bamboo_rice", "cactus_sandwich",
    )),
    ("green_delight_nullgr:", ["proteins"], (
        "slime_bread", "slime_popsicle",
    )),
    ("green_delight_nullgr:", ["proteins", "vegetables"], (
        "bamboo_beef",
    )),
    ("green_delight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "slime_jelly",
    )),
    ("green_delight_nullgr:", ["proteins", "sugars"], (
        "slime_mousse",
    )),
    ("green_delight_nullgr:", ["vegetables"], (
        "cactus_dried", "cactus_peeled", "sea_salad",
    )),
    ("green_delight_nullgr:", ["vegetables", "sugars"], (
        "cactus_cola", "cactus_juice", "cactus_stick",
    )),
    ("hearthandharvest_nullgr:", ["fruits"], (
        "raspberry",
    )),
    ("hearthandharvest_nullgr:", ["fruits", "grains", "sugars"], (
        "blueberry_muffin", "blueberry_pie_slice", "grape_pie_slice", "raspberry_pie_slice",
    )),
    ("hearthandharvest_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "trail_mix",
    )),
    ("hearthandharvest_nullgr:", ["fruits", "sugars"], (
        "apple_jam", "baked_apple", "blueberries", "blueberry_jam", "blueberry_juice", "blueberry_wine", "caramel_apple",
        "cherry", "cherry_juice", "cherry_wine", "glow_berry_jam", "grape_jam", "green_grape_juice", "green_grape_wine",
        "green_grapes", "melon_jam", "raisins", "raspberry_jam", "raspberry_juice", "raspberry_wine", "red_grape_juice",
        "red_grape_wine", "red_grapes", "sweet_berry_jam",
    )),
    ("hearthandharvest_nullgr:", ["grains", "proteins"], (
        "batter", "macaroni_and_cheese",
    )),
    ("hearthandharvest_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "carrot_cake_slice",
    )),
    ("hearthandharvest_nullgr:", ["grains", "proteins", "sugars"], (
        "chicken_pot_pie_slice", "waffle",
    )),
    ("hearthandharvest_nullgr:", ["grains", "sugars"], (
        "cheese_slice",
    )),
    ("hearthandharvest_nullgr:", ["proteins"], (
        "cheddar_cheese_slice", "cooked_sausage", "goat_cheese_slice", "goat_milk_bottle", "jerky", "raw_sausage",
        "skewered_sausage",
    )),
    ("hearthandharvest_nullgr:", ["proteins", "vegetables"], (
        "mashed_potatoes", "onion_soup",
    )),
    ("hearthandharvest_nullgr:", ["proteins", "sugars"], (
        "chocolate_bar",
    )),
    ("hearthandharvest_nullgr:", ["vegetables"], (
        "pickled_beetroots", "pickled_cabbage", "pickled_carrots", "pickled_onions", "pickled_potatoes",
        "sunflower_seeds",
    )),
    ("hearthandharvest_nullgr:", ["sugars"], (
        "caramel", "charred_marshmallow_stick", "cotton_candy", "marshmallow_stick", "mead",
        "roasted_marshmallow_stick", "sap_bucket", "syrup_bottle",
    )),
    ("immersive_cooking:", ["proteins"], (
        "clean_spider_shank", "cooked_spider_cutlet", "raw_spider_cutlet", "raw_spider_shank", "smoked_spider_shank",
    )),
    ("immersive_cooking:", ["vegetables"], (
        "bamboo_slice", "curry_base", "diced_onion", "fried_potato_cubes", "fried_potato_slice", "potato_cubes",
        "potato_slice",
    )),
    ("immersive_cooking:", ["vegetables", "sugars"], (
        "pyttipanna",
    )),
    ("large_meals_nullgr:", ["fruits", "proteins", "sugars"], (
        "sweet_berry_custard",
    )),
    ("large_meals_nullgr:", ["grains", "proteins", "vegetables"], (
        "cod_deluxe", "hearty_lunch", "mushroom_pot_pie", "omurice", "pasta_with_mushroom_sauce",
        "roasted_mutton_rack",
    )),
    ("large_meals_nullgr:", ["grains", "proteins", "sugars"], (
        "rice_pudding",
    )),
    ("large_meals_nullgr:", ["proteins"], (
        "cooked_mutton_rack", "raw_mutton_rack",
    )),
    ("large_meals_nullgr:", ["proteins", "vegetables"], (
        "chicken_curry", "potato_soup", "pufferfish_broth", "tomato_egg_soup",
    )),
    ("large_meals_nullgr:", ["vegetables"], (
        "red_soup",
    )),
    ("lavsdelight_nullgr:", ["fruits"], (
        "lemon", "lemon_juice", "lemon_slice",
    )),
    ("lavsdelight_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "lavender_dumpling",
    )),
    ("lavsdelight_nullgr:", ["fruits", "grains", "vegetables", "sugars"], (
        "apple_dumpling",
    )),
    ("lavsdelight_nullgr:", ["fruits", "grains", "sugars"], (
        "blueberry_tart_slice", "peach_tart",
    )),
    ("lavsdelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "cheese_n_berries",
    )),
    ("lavsdelight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "apple_cabbage_stew",
    )),
    ("lavsdelight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "carbonated_water", "melon_tanghulu", "mint_tea",
    )),
    ("lavsdelight_nullgr:", ["fruits", "sugars"], (
        "baked_peach", "blueberries", "cola", "lemon_tea", "lemonade", "peach", "peach_candy", "peach_puree",
        "peach_slice", "peach_syrup", "sweet_berry_juice",
    )),
    ("lavsdelight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "poppy_seed_muffin",
    )),
    ("lavsdelight_nullgr:", ["proteins"], (
        "cheese_wedge", "salted_meat",
    )),
    ("lavsdelight_nullgr:", ["proteins", "sugars"], (
        "milk_chocolate",
    )),
    ("lavsdelight_nullgr:", ["vegetables"], (
        "mint_extract", "mint_leaf", "mint_roots",
    )),
    ("lavsdelight_nullgr:", ["sugars"], (
        "brown_sugar",
    )),
    ("letsdobakey_nullgr:", ["fruits"], (
        "strawberry",
    )),
    ("letsdobakey_nullgr:", ["fruits", "grains"], (
        "sweetberry_cupcake",
    )),
    ("letsdobakey_nullgr:", ["fruits", "grains", "proteins"], (
        "strawberry_cupcake",
    )),
    ("letsdobakey_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "apple_pie_piece", "chocolate_tart_slice", "glowberry_pie_slice", "strawberry_cake_slice",
        "sweetberry_cake_slice",
    )),
    ("letsdobakey_nullgr:", ["fruits", "grains", "sugars"], (
        "apple_cupcake", "strawberry_glazed_cookie", "sweetberry_glazed_cookie",
    )),
    ("letsdobakey_nullgr:", ["fruits", "proteins", "sugars"], (
        "pudding_slice",
    )),
    ("letsdobakey_nullgr:", ["fruits", "sugars"], (
        "apple_jam", "glowberry_jam", "strawberry_jam", "sweetberry_jam",
    )),
    ("letsdobakey_nullgr:", ["grains"], (
        "baguette", "bread_bakey", "croissant", "linzer_tart_slice", "waffle",
    )),
    ("letsdobakey_nullgr:", ["grains", "proteins"], (
        "braided_bread", "bun", "toast_bakey",
    )),
    ("letsdobakey_nullgr:", ["grains", "proteins", "sugars"], (
        "chocolate_cake_slice", "crusty_bread",
    )),
    ("letsdobakey_nullgr:", ["grains", "vegetables"], (
        "vegetable_sandwich",
    )),
    ("letsdobakey_nullgr:", ["grains", "sugars"], (
        "chocolate_glazed_cookie",
    )),
    ("letsdobakey_nullgr:", ["proteins", "sugars"], (
        "bundt_cake_slice", "chocolate",
    )),
    ("letsdobakey_nullgr:", ["vegetables", "sugars"], (
        "yeast",
    )),
    ("letsdobakey_nullgr:", ["sugars"], (
        "chocolate_jam",
    )),
    ("midautumndelight_nullgr:", ["fruits", "grains", "sugars"], (
        "mooncake_jujube",
    )),
    ("midautumndelight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "mooncake_nut",
    )),
    ("midautumndelight_nullgr:", ["grains", "proteins", "sugars"], (
        "mooncake_bean_paste", "mooncake_lotus", "mooncake_meat", "mooncake_yolk",
    )),
    ("midautumndelight_nullgr:", ["grains", "vegetables", "sugars"], (
        "mooncake_taro", "osmanthus_flowers_cake",
    )),
    ("midautumndelight_nullgr:", ["grains", "sugars"], (
        "mooncake_piece",
    )),
    ("midautumndelight_nullgr:", ["vegetables", "sugars"], (
        "osmanthus_flowers_sugar", "osmanthus_flowers_wine",
    )),
    ("milet_delight_nullgr:", ["fruits"], (
        "glow_berry_wine",
    )),
    ("milet_delight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "sweet_berry_biscuit",
    )),
    ("milet_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "chorus_millet_pastry", "glow_berry_millet_pastry",
    )),
    ("milet_delight_nullgr:", ["grains"], (
        "millet_gruel", "millet_rice", "millet_wine", "wheat_wine",
    )),
    ("milet_delight_nullgr:", ["grains", "proteins"], (
        "bone_millet_noodles", "millet_beef", "millet_chicken", "millet_noodles", "millet_porkchop",
    )),
    ("milet_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "fried_millet_rice",
    )),
    ("milet_delight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "chocolate_biscuit",
    )),
    ("milet_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "honey_biscuit", "milk_biscuit", "milk_millet_pastry", "millet_biscuit", "sculk_biscuit",
    )),
    ("milet_delight_nullgr:", ["grains", "vegetables"], (
        "millet_pumpkin_soup", "millet_vegetable_soup", "potato_millet_noodles", "potato_rolls",
        "tomato_millet_noodles",
    )),
    ("milet_delight_nullgr:", ["grains", "vegetables", "sugars"], (
        "chocolate_millet_pastry",
    )),
    ("milet_delight_nullgr:", ["grains", "sugars"], (
        "millet_ball", "millet_pastry", "sculk_millet_pastry",
    )),
    ("milet_delight_nullgr:", ["vegetables"], (
        "potato_sauce",
    )),
    ("milet_delight_nullgr:", ["sugars"], (
        "cooked_spun_sugar", "spun_sugar",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "grains", "proteins"], (
        "ice_cream_cone_glowing_berries", "ice_cream_cone_lemon", "ice_cream_cone_purple_fruit",
        "ice_cream_cone_raspberry", "ice_cream_cone_raspberry2", "ice_cream_cone_strawberry",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "ice_cream_cone_banana", "ice_cream_cone_berry_bacca", "ice_cream_cone_blueberry", "ice_cream_cone_cherry",
        "ice_cream_cone_durian", "ice_cream_cone_grape", "ice_cream_cone_hami_melon", "ice_cream_cone_hawthorn",
        "ice_cream_cone_kiwifruit", "ice_cream_cone_longan", "ice_cream_cone_loquat", "ice_cream_cone_lychee",
        "ice_cream_cone_mango", "ice_cream_cone_mangosteen", "ice_cream_cone_mulberry", "ice_cream_cone_papaya",
        "ice_cream_cone_passion_fruit", "ice_cream_cone_peach", "ice_cream_cone_pear", "ice_cream_cone_persimmon",
        "ice_cream_cone_pineapple", "ice_cream_cone_pitaya_dragon_fruit", "ice_cream_cone_shaddock",
        "ice_cream_cone_tangerine",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "proteins"], (
        "coconut_milk_jelly",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "proteins", "vegetables"], (
        "coconut_jelly_coconut_green", "moonlight_own_goal", "raw_coconut_latte",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "cheese_strawberry", "matcha_mango_milk", "purple_grape_cheese",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "proteins", "sugars"], (
        "domineering_cheese_strawberry", "peach_jelly", "raw_coconut_durian",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "bumper_passion_fruit", "cherry_berry", "domineering_cherry", "forest_rose", "lemon_black_tea", "mango_pomelo_sago",
        "orange_american", "peach_own_goal", "taro_grape",
    )),
    ("milk_cream_delight_nullgr:", ["fruits", "sugars"], (
        "cheese_peach", "lemonade",
    )),
    ("milk_cream_delight_nullgr:", ["grains", "proteins"], (
        "ice_cream_cone_red_peas", "waffles",
    )),
    ("milk_cream_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "ice_cream_cone_black_tea", "ice_cream_cone_coffee", "ice_cream_cone_green_tea", "ice_cream_cone_matcha",
        "ice_cream_cone_yellow_tea",
    )),
    ("milk_cream_delight_nullgr:", ["grains", "vegetables"], (
        "oat_coffee",
    )),
    ("milk_cream_delight_nullgr:", ["proteins", "vegetables"], (
        "cloud_matcha", "xueding_coffee",
    )),
    ("milk_cream_delight_nullgr:", ["vegetables"], (
        "cassava", "iced_americano", "sago", "tapioca_flour", "xiancaodong",
    )),
    ("milk_cream_delight_nullgr:", ["vegetables", "sugars"], (
        "bobo", "bubble_tea",
    )),
    ("miners_delight:", ["grains", "proteins"], (
        "insect_wrap",
    )),
    ("miners_delight:", ["grains", "proteins", "vegetables"], (
        "bat_rolls", "bowl_of_stuffed_squid", "glow_ink_pasta", "insect_sandwich", "noodle_soup_cup",
        "pasta_with_veggieballs", "squid_sandwich",
    )),
    ("miners_delight:", ["grains", "vegetables"], (
        "cave_hamburger", "vegan_hamburger", "vegan_patty", "vegan_steak_and_potatoes", "vegan_wrap",
    )),
    ("miners_delight:", ["proteins"], (
        "arthropod", "axolotl", "baked_squid", "baked_tentacles", "bat_wing", "cooked_arthropod", "glow_squid",
        "milk_cup", "silverfish_eggs", "smoked_bat_wing", "squid", "tentacles", "weird_caviar",
    )),
    ("miners_delight:", ["proteins", "vegetables"], (
        "baked_cod_stew_cup", "bat_soup", "bat_soup_cup", "beef_stew_cup", "bone_broth_cup", "cave_soup_cup",
        "chicken_soup_cup", "fish_stew_cup", "improvised_barbecue_stick", "insect_stew", "insect_stew_cup",
        "rabbit_stew_cup", "seasoned_arthropods", "takoyaki",
    )),
    ("miners_delight:", ["vegetables"], (
        "baked_cave_carrot", "cave_carrot", "cave_soup", "moss", "mushroom_stew_cup", "vegetable_soup_cup",
    )),
    ("miners_delight:", ["vegetables", "sugars"], (
        "beetroot_soup_cup", "hot_cocoa_cup", "pumpkin_soup_cup",
    )),
    ("muffins_thaidelight_nullgr:", ["fruits"], (
        "lime", "lime_slice", "raw_papaya", "raw_papaya_slice",
    )),
    ("muffins_thaidelight_nullgr:", ["fruits", "grains", "vegetables", "sugars"], (
        "stir_fried_noodle",
    )),
    ("muffins_thaidelight_nullgr:", ["fruits", "proteins"], (
        "durian_curry",
    )),
    ("muffins_thaidelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "durian_cake_slice", "somtam",
    )),
    ("muffins_thaidelight_nullgr:", ["fruits", "sugars"], (
        "durian_pulp", "fried_durian", "lime_juice", "papaya", "papaya_juice", "papaya_slice",
    )),
    ("muffins_thaidelight_nullgr:", ["grains", "proteins", "vegetables"], (
        "crab_fried_rice",
    )),
    ("muffins_thaidelight_nullgr:", ["proteins"], (
        "bottle_of_blue_dragonfly", "bottle_of_green_dragonfly", "bottle_of_red_dragonfly",
        "bottle_of_yellow_dragonfly", "cooked_dragonfly", "cooked_flower_crab", "dragonfly", "fish_sauce_bottle",
        "flower_crab", "omelette",
    )),
    ("muffins_thaidelight_nullgr:", ["proteins", "vegetables"], (
        "bamboo_shoot_soup", "basil_omelette", "cooked_seafood_crab_meat", "phat_kaphrao", "steamed_bamboo_shoot",
    )),
    ("muffins_thaidelight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "spicy_minced_meat_salad",
    )),
    ("muffins_thaidelight_nullgr:", ["vegetables"], (
        "pesto_sauce", "seafood_bucket",
    )),
    ("muffins_thaidelight_nullgr:", ["vegetables", "sugars"], (
        "butterfly_pea_tea",
    )),
    ("mushroon_delight_nullgr:", ["vegetables"], (
        "acacia_mushroom_item", "acacia_woodear_item", "artistconk_item", "bigmushrooms_item",
        "bouncystool2_blue_item", "bouncystool2_purple_item", "bouncystool2_red_item", "brich_artistconk_item",
        "brich_trunk_mushroom", "chickenofthewoods_item", "fanfern_item", "fountainfungus_item",
        "glowshroomsredone_blue_item", "glowshroomsredone_green_item", "glowshroomsredone_orange_item",
        "glowshroomsredone_pink_item", "glowshroomsredone_purple_item", "glowstools_item", "jellyshroomplant_item",
        "jungle_trunk_mushroom", "korugreen_item", "lanternshroom1_item", "mossymazepolypore_item",
        "oak_stump_mushroom", "puffballsredone_item", "shaggymane_item", "spore_item", "spruce_stump_mushroom",
        "tinymushrooms_item", "toadstool_blue_item", "toadstool_green_item", "toadstool_orange_item",
        "toadstool_purple_item", "toadstool_red_item", "woodear_item",
    )),
    ("natural_delight_nullgr:", ["grains", "proteins"], (
        "grow_acorn_face", "pine_nut_porridge", "sponge_cake",
    )),
    ("natural_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "acorn_cold_noodles",
    )),
    ("natural_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "acorn_bread", "guazi_crisp",
    )),
    ("natural_delight_nullgr:", ["grains", "vegetables"], (
        "rose_cake",
    )),
    ("natural_delight_nullgr:", ["proteins"], (
        "acorn", "acorn_tofu", "pine_nut", "pumpkin_seed", "shell_sunflower_seeds", "sunflower_seeds",
        "watermelon_seed",
    )),
    ("natural_delight_nullgr:", ["proteins", "vegetables"], (
        "acorn_fry_cabbage", "fried_acorn_tofu", "peony_flower_tea", "pine_nut_meatball", "sponge_tree_fry_egg",
        "sunflower_seed_beef",
    )),
    ("natural_delight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "stewed_chicken_with_clove_face",
    )),
    ("natural_delight_nullgr:", ["vegetables"], (
        "acacia_flower", "lilac", "peony", "rose",
    )),
    ("natural_delight_nullgr:", ["vegetables", "sugars"], (
        "acacia_flower_soup", "acacia_scented_tea", "rose_tea", "shiyan_mountain_clove_tea",
    )),
    ("natural_delight_nullgr:", ["sugars"], (
        "birch_juice",
    )),
    ("nether_delight_nullgr:", ["fruits"], (
        "magma_gelatin", "propelpearl",
    )),
    ("nether_delight_nullgr:", ["fruits", "proteins"], (
        "nether_skewer",
    )),
    ("nether_delight_nullgr:", ["grains", "proteins"], (
        "ghast_dough", "hotdog",
    )),
    ("nether_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "chilidog", "crimson_stroganoff", "fried_hoglin_chop", "spicy_curry",
    )),
    ("nether_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "breakfast_sampler",
    )),
    ("nether_delight_nullgr:", ["proteins"], (
        "bleeding_tartar", "boiled_egg", "broken_strider_egg", "burnt_roll", "cold_striderloaf", "ghasta",
        "ghasta_with_cream", "ground_strider", "hoglin_loin", "hoglin_sirloin", "magma_cake_slice",
        "roasted_hoglin_ears", "roasted_sausage", "rock_soup", "sausage", "spicy_cotton", "strider_slice",
        "striderloaf",
    )),
    ("nether_delight_nullgr:", ["proteins", "vegetables"], (
        "blue_tenderloin_steak", "deviled_egg", "ghast_salad", "grilled_strider", "hot_cream", "hot_cream_cone",
        "hot_wings", "hot_wings_bucket", "plate_of_stuffed_hoglin_ham", "plate_of_stuffed_hoglin_roast",
        "plate_of_stuffed_hoglin_snout", "sausage_and_potatoes", "spicy_hoglin_stew", "spicy_noodle_soup",
        "spicy_skewer", "strider_and_grilled_fungus", "strider_moss_stew", "strider_stew", "warped_moldy_meat",
    )),
    ("nether_delight_nullgr:", ["vegetables"], (
        "bullet_pepper",
    )),
    ("newyear_delight_nullgr:", ["fruits", "grains"], (
        "tangyuan_blueberry", "tangyuan_blueberry_spoon", "tangyuan_durian", "tangyuan_durian_spoon",
        "tangyuan_hawthorn", "tangyuan_hawthorn_spoon", "tangyuan_pineapple", "tangyuan_pineapple_spoon",
        "tangyuan_strawberry", "tangyuan_strawberry_spoon",
    )),
    ("newyear_delight_nullgr:", ["grains"], (
        "glutinousrice", "glutinousricedough", "tangyuan", "tangyuan_chocolate", "tangyuan_chocolate_spoon",
        "tangyuan_grow", "tangyuan_spoon",
    )),
    ("newyear_delight_nullgr:", ["grains", "proteins"], (
        "tangyuan_beanpaste", "tangyuan_beanpaste_spoon", "tangyuan_cheese", "tangyuan_cheese_spoon",
        "tangyuan_peanut", "tangyuan_peanut_spoon", "tangyuan_pork", "tangyuan_pork_spoon", "tangyuan_shrimp",
        "tangyuan_shrimp_spoon",
    )),
    ("newyear_delight_nullgr:", ["grains", "vegetables"], (
        "tangyuan_matcha", "tangyuan_matcha_spoon", "tangyuan_taropaste", "tangyuan_taropaste_spoon",
    )),
    ("newyear_delight_nullgr:", ["proteins"], (
        "bean_paste", "red_bean_shrub",
    )),
    ("ocean_delight_nullgr:", ["grains", "proteins"], (
        "elder_guardian_roll", "fugu_rice_cakes", "fugu_roll", "squid_rings",
    )),
    ("ocean_delight_nullgr:", ["proteins"], (
        "baked_tentacle_on_a_stick", "cooked_elder_guardian_slice", "cooked_guardian_tail", "cooked_puffish",
        "cut_tentacles", "elder_guardian_eye", "elder_guardian_slab", "elder_guardian_slice", "fugu_sashimi",
        "fugu_slice", "guardian", "guardian_eye", "guardian_tail", "puffish_nail", "puffish_venom_sac",
        "tentacle_on_a_stick", "tentacles",
    )),
    ("ocean_delight_nullgr:", ["proteins", "vegetables"], (
        "bowl_of_guardian_soup", "cabbage_wrapped_elder_guardian", "cooked_stuffed_cod", "puffish_soup",
        "stuffed_cod",
    )),
    ("ocean_delight_nullgr:", ["vegetables"], (
        "braised_sea_pickle", "seagrass_salad",
    )),
    ("ocean_delight_nullgr:", ["vegetables", "sugars"], (
        "honey_fried_kelp",
    )),
    ("oceanic_delight_nullgr:", ["fruits", "vegetables"], (
        "nautilus_kelp_juice",
    )),
    ("oceanic_delight_nullgr:", ["grains", "proteins"], (
        "caviar_toast", "shrimp_chips",
    )),
    ("oceanic_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "caesar_salad", "egg_roll", "fish_egg_noodle_soup", "fish_egg_roll", "fish_egg_roll_slice",
        "pasta_with_eye_balls", "plate_of_paella", "plate_of_stuffed_pufferfish", "sea_pickle_roll",
        "sea_pickle_roll_slice", "seafood_rice", "shrimp_roll", "takoyaki",
    )),
    ("oceanic_delight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "globular_rice",
    )),
    ("oceanic_delight_nullgr:", ["grains", "sugars"], (
        "sponce_cake_slice",
    )),
    ("oceanic_delight_nullgr:", ["proteins"], (
        "ancient_fish_eggs", "cooked_shrimp", "elder_guardian_eye", "glow_squid_tentacles",
        "grilled_squid_tentacles", "raw_shrimp", "salmon_eggs", "shrimp_slices", "squid_tentacles",
    )),
    ("oceanic_delight_nullgr:", ["proteins", "vegetables"], (
        "fish_skewer", "glows_squid_stew", "shrimp_stew", "squid_and_pickles", "squid_salad", "steamed_beef",
    )),
    ("oceanic_delight_nullgr:", ["vegetables"], (
        "potato_salad", "sea_grape", "sea_salad", "sliced_sea_pickles",
    )),
    ("oceanic_delight_nullgr:", ["vegetables", "sugars"], (
        "sea_grape_juice",
    )),
    ("ramadandelight_nullgr:", ["fruits", "sugars"], (
        "date",
    )),
    ("ramadandelight_nullgr:", ["fruits", "grains", "sugars"], (
        "date_stuffed_cookie",
    )),
    ("ramadandelight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "kunafa",
    )),
    ("ramadandelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "mhalbiya", "sweet_tagine",
    )),
    ("ramadandelight_nullgr:", ["fruits", "sugars"], (
        "date_syrup",
    )),
    ("ramadandelight_nullgr:", ["grains"], (
        "bourek_sheet", "flat_bread",
    )),
    ("ramadandelight_nullgr:", ["grains", "proteins"], (
        "hummus_tahini",
    )),
    ("ramadandelight_nullgr:", ["grains", "proteins", "vegetables"], (
        "bourek", "chickpea_and_rice", "haleem", "makloba", "manakish", "quiche_slice", "raw_bourek", "raw_samosa",
        "samosa", "sayadieh",
    )),
    ("ramadandelight_nullgr:", ["grains", "sugars"], (
        "luqaimat", "zalabiya",
    )),
    ("ramadandelight_nullgr:", ["proteins"], (
        "chickpea", "kebab", "raw_kebab",
    )),
    ("ramadandelight_nullgr:", ["proteins", "vegetables"], (
        "chorba", "harira", "savory_filling", "tagine",
    )),
    ("ramadandelight_nullgr:", ["vegetables"], (
        "parsley", "tabbouleh",
    )),
    ("rusticdelight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "honey_pancake",
    )),
    ("rusticdelight_nullgr:", ["fruits", "grains", "sugars"], (
        "fruit_beignet",
    )),
    ("rusticdelight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "sweet_salad",
    )),
    ("rusticdelight_nullgr:", ["grains"], (
        "fried_dough", "fried_dumplings",
    )),
    ("rusticdelight_nullgr:", ["grains", "proteins"], (
        "batter", "calamari_roll",
    )),
    ("rusticdelight_nullgr:", ["grains", "proteins", "vegetables"], (
        "cherry_blossom_cheesecake_slic", "cherry_blossom_cookie", "cherry_blossom_pancake", "fried_calamari",
        "fried_chicken", "fried_mushrooms", "spring_rolls", "stuffed_bell_pepper_green", "stuffed_bell_pepper_red",
        "stuffed_bell_pepper_yellow", "vegetable_pancake",
    )),
    ("rusticdelight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "pumpkin_pancake",
    )),
    ("rusticdelight_nullgr:", ["grains", "proteins", "sugars"], (
        "chocolate_pancake", "coffee_cookie", "pancake", "syrup_cheesecake_slice", "syrup_cookie",
    )),
    ("rusticdelight_nullgr:", ["grains", "vegetables"], (
        "bell_pepper_pasta", "bell_pepper_roll_green", "bell_pepper_roll_red", "bell_pepper_roll_yellow",
        "cherry_blossom_roll",
    )),
    ("rusticdelight_nullgr:", ["grains", "sugars"], (
        "syrup_sandwich",
    )),
    ("rusticdelight_nullgr:", ["proteins"], (
        "calamari", "calamari_slice", "cooked_calamari", "cooked_calamari_slice", "milk_coffee",
    )),
    ("rusticdelight_nullgr:", ["proteins", "vegetables"], (
        "coffee_braised_beef", "potato_salad",
    )),
    ("rusticdelight_nullgr:", ["proteins", "sugars"], (
        "chocolate_coffee", "syrup_coffee",
    )),
    ("rusticdelight_nullgr:", ["vegetables"], (
        "baked_potato_slices", "bell_pepper_green", "bell_pepper_red", "bell_pepper_slice_green",
        "bell_pepper_slice_red", "bell_pepper_slice_yellow", "bell_pepper_soup", "bell_pepper_yellow",
        "coffee_beans", "cook_bell_pepper_slice_green", "cook_bell_pepper_slice_red",
        "cook_bell_pepper_slice_yellow", "golden_coffee_beans", "potato_slices", "roasted_bell_pepper_green",
        "roasted_bell_pepper_red", "roasted_bell_pepper_yellow", "roasted_coffee_beans",
    )),
    ("rusticdelight_nullgr:", ["sugars"], (
        "syrup",
    )),
    ("silents_delight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "sculk_sensor_sprinkles",
    )),
    ("silents_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "heartburger", "sculk_catalyst_pie_crust", "sculk_catalyst_pie_slice", "warden_ear_fried_rice",
    )),
    ("silents_delight_nullgr:", ["grains", "vegetables"], (
        "sculk_sensor_tendril_roll", "sculk_sensor_tendril_roll_slic",
    )),
    ("silents_delight_nullgr:", ["proteins"], (
        "baked_warden_ear_on_a_stick", "cut_warden_ear", "minced_warden_heart", "warden_ear",
        "warden_ear_on_a_stick", "warden_heart", "warden_heart_patty",
    )),
    ("silents_delight_nullgr:", ["proteins", "vegetables"], (
        "plate_of_warden_heart", "sculk_soup",
    )),
    ("silents_delight_nullgr:", ["vegetables"], (
        "sculk_barbecue_stick", "sculk_sensor_tendril", "sculk_vein_salad",
    )),
    ("silents_delight_nullgr:", ["vegetables", "sugars"], (
        "sculk_shrieker_shake",
    )),
    ("slavic_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "pancakes_with_berries",
    )),
    ("slavic_delight_nullgr:", ["grains"], (
        "kvass_bottle", "pancakes",
    )),
    ("slavic_delight_nullgr:", ["grains", "proteins"], (
        "pelmeni",
    )),
    ("slavic_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "kurnik", "okroshka_kvass", "pirozhok_with_onions",
    )),
    ("slavic_delight_nullgr:", ["grains", "vegetables"], (
        "pirozhok_with_potatoes",
    )),
    ("slavic_delight_nullgr:", ["proteins"], (
        "boiled_egg", "chicken_patty", "crab_sticks", "minced_chicken", "minced_cod", "minced_pork", "pork_patty",
        "sausage",
    )),
    ("slavic_delight_nullgr:", ["proteins", "vegetables"], (
        "borsch", "crab_salad", "kefir_bottle", "mash_and_patty", "okroshka_kefir", "solyanka", "svekolnik",
    )),
    ("slavic_delight_nullgr:", ["vegetables"], (
        "boiled_potatoes", "cucumber", "mashed_potatoes", "pickles", "radish", "sauerkraut_jar",
    )),
    ("spanish_delight_nullgr:", ["grains", "proteins"], (
        "croquettes",
    )),
    ("spanish_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "paella",
    )),
    ("spanish_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "churro",
    )),
    ("spanish_delight_nullgr:", ["grains", "vegetables"], (
        "gazpacho", "pantumaca",
    )),
    ("spanish_delight_nullgr:", ["proteins"], (
        "fried_squid_ring", "green_bean", "squid_ring",
    )),
    ("spanish_delight_nullgr:", ["proteins", "vegetables"], (
        "pil_pil_cod", "spanish_tortilla",
    )),
    ("spanish_delight_nullgr:", ["vegetables"], (
        "brava_potatoes", "green_pepper", "red_pepper", "sliced_onion", "sliced_potato",
    )),
    ("stack_burger_nullgr:", ["fruits", "sugars"], (
        "apple_slices",
    )),
    ("stack_burger_nullgr:", ["fruits", "sugars"], (
        "golden_apple_slices",
    )),
    ("stack_burger_nullgr:", ["grains"], (
        "my_hurger",
    )),
    ("stack_burger_nullgr:", ["grains", "proteins", "sugars"], (
        "bread_slice", "burger_bread_bottom_item", "my_burger_2", "toasted_bread_slice_item",
    )),
    ("stack_burger_nullgr:", ["proteins"], (
        "bacon_strips", "chicken_filet", "cod_filet", "cooked_chicken_filet", "cooked_cod_filet", "cooked_pork_cuts",
        "cooked_salmon_filet", "pork_cuts", "salmon_filet", "spread", "spread_bread_loaf",
    )),
    ("stack_burger_nullgr:", ["vegetables"], (
        "chopped_beetroot", "chopped_carrot", "chopped_onion", "cooked_chopped_beetroot", "cooked_chopped_carrot",
        "cooked_chopped_onion", "cooked_tomato_slice", "cooked_tomato_slice_0", "cooked_tomato_slice_1",
        "cooked_tomato_slice_2", "lettuce_head", "lettuce_leaf", "pickle_chips", "sliced_toasted_crimson_fungus",
        "sliced_toasted_warped_fungus", "toasted_crimson_fungus", "toasted_warped_fungus", "tomato_slice",
        "tomato_slice_0", "tomato_slice_1", "tomato_slice_2",
    )),
    ("stack_burger_nullgr:", ["vegetables", "sugars"], (
        "chopped_golden_carrot",
    )),
    ("sushigocrafting_nullgr:", ["fruits", "grains", "proteins", "vegetables"], (
        "crab_california", "crab_cheese_california", "crab_cucumber_california", "salmon_california",
        "salmon_cheese_california", "salmon_cucumber_california", "tobiko_crab_california",
        "tobiko_crab_cheese_california", "tobiko_crab_cucumber_california", "tobiko_salmon_california",
        "tobiko_salmon_cheese_california", "tobiko_salmon_cucumber_california", "tobiko_tuna_california",
        "tobiko_tuna_cheese_california", "tobiko_tuna_cucumber_california", "tuna_california",
        "tuna_cheese_california", "tuna_cucumber_california",
    )),
    ("sushigocrafting_nullgr:", ["fruits", "grains", "vegetables"], (
        "avocado_maki",
    )),
    ("sushigocrafting_nullgr:", ["grains"], (
        "onigiri",
    )),
    ("sushigocrafting_nullgr:", ["grains", "proteins", "vegetables"], (
        "chicken_temaki", "crab_maki", "salmon_gunkan", "salmon_maki", "salmon_nigiri", "salmon_temaki",
        "shrimp_nigiri", "shrimp_temaki", "tuna_gunkan", "tuna_maki", "tuna_nigiri", "tuna_temaki",
    )),
    ("sushigocrafting_nullgr:", ["grains", "vegetables"], (
        "cucumber_maki", "wakame_gunkan",
    )),
    ("sushigocrafting_nullgr:", ["proteins"], (
        "raw_tuna", "shrimp_bucket", "soy_sauce", "tobiko", "tuna_fillet",
    )),
    ("sushigocrafting_nullgr:", ["vegetables"], (
        "dried_seaweed", "nori_sheets", "seaweed", "sesame_seed", "wasabi_root",
    )),
    ("tea_delight_nullgr:", ["vegetables"], (
        "ceramic_teacup_black_tea", "ceramic_teacup_green_tea", "ceramic_teacup_matcha_tea",
        "ceramic_teacup_oolong_tea", "ceramic_teacup_red_tea", "ceramic_teacup_white_tea",
        "ceramic_teacup_yellow_tea",
    )),
    ("ube_delight_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "halo_halo",
    )),
    ("ube_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "arroz_caldo", "bangsilog", "lumpia",
    )),
    ("ube_delight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "chicken_inasal_rice", "ensaymada_ube", "ensaymada_ube_raw", "polvorone_ube", "tosilog", "ube_cake_slice",
    )),
    ("ube_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "ensaymada", "ensaymada_raw", "polvorone_cc", "polvorone_pinipig",
    )),
    ("ube_delight_nullgr:", ["grains", "vegetables"], (
        "cookie_ginger", "cookie_ube", "sinangag",
    )),
    ("ube_delight_nullgr:", ["grains", "vegetables", "sugars"], (
        "hopia_ube", "hopia_ube_raw", "pandesal_ube", "pandesal_ube_raw",
    )),
    ("ube_delight_nullgr:", ["grains", "sugars"], (
        "hopia_munggo", "hopia_munggo_raw", "pandesal", "pandesal_raw",
    )),
    ("ube_delight_nullgr:", ["proteins"], (
        "fish_sauce_bottle",
    )),
    ("ube_delight_nullgr:", ["proteins", "vegetables"], (
        "bulalo", "kinilaw", "mechado", "sisig",
    )),
    ("ube_delight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "chicken_inasal", "milk_tea_ube", "tocino",
    )),
    ("ube_delight_nullgr:", ["proteins", "sugars"], (
        "condensed_milk_bottle", "leche_flan", "polvorone",
    )),
    ("ube_delight_nullgr:", ["vegetables"], (
        "ginger", "ginger_chop", "lemongrass", "ube",
    )),
    ("valentine_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "apple_cookie", "berry_cookie", "chorus_cookie", "golden_cookie", "medic_cookie", "melon_cookie",
        "omega_cookie", "special_apple_cookie", "special_berry_cookie", "special_chorus_cookie",
        "special_golden_cookie", "special_medic_cookie", "special_melon_cookie", "special_omega_cookie",
    )),
    ("valentine_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "caramel_cookie", "fire_cookie", "glow_cookie", "peculiar_cookie", "special_caramel_cookie",
        "special_fire_cookie", "special_glow_cookie", "special_peculiar_cookie",
    )),
    ("valentine_delight_nullgr:", ["grains", "vegetables", "sugars"], (
        "aristea_cookie", "good_vision_cookie", "nether_wart_cookie", "special_aristea_cookie",
        "special_good_vision_cookie", "special_nether_wart_cookie", "special_spooky_cookie", "spooky_cookie",
    )),
    ("valentine_delight_nullgr:", ["grains", "sugars"], (
        "evil_cookie", "explosive_cookie", "extra_special_chocolate_cookie", "prismatic_cookie", "rocket_cookie",
        "special_chocolate_cookie", "special_evil_cookie", "special_explosive_cookie", "special_prismatic_cookie",
        "special_rocket_cookie",
    )),
    ("valentine_delight_nullgr:", ["sugars"], (
        "colorful_cotton_candy1", "colorful_cotton_candy2", "colorful_cotton_candy3", "cotton_candy",
    )),
    ("vanilladelight_nullgr:", ["fruits", "sugars"], (
        "apple_salad", "apple_slice", "berries_salad", "cooked_apple", "golden_apple_slice",
    )),
    ("vanilladelight_nullgr:", ["fruits", "grains", "sugars"], (
        "chorus_pie_slice", "melon_pie_slice",
    )),
    ("vanilladelight_nullgr:", ["fruits", "proteins"], (
        "glow_tropical_fish_stew",
    )),
    ("vanilladelight_nullgr:", ["fruits", "proteins", "sugars"], (
        "glow_berries_candy", "sweet_berry_custard",
    )),
    ("vanilladelight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "grilled_beetroot",
    )),
    ("vanilladelight_nullgr:", ["fruits", "sugars"], (
        "glow_berries_jam", "golden_apple_cider", "sweet_berries_jam",
    )),
    ("vanilladelight_nullgr:", ["proteins", "vegetables"], (
        "cod_stew",
    )),
    ("vanilladelight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "milky_pumpkin",
    )),
    ("vanilladelight_nullgr:", ["proteins", "sugars"], (
        "caramel_candy", "caramelized_chicken", "honey_candy", "honey_pudding",
    )),
    ("vanilladelight_nullgr:", ["vegetables"], (
        "carrot_salad", "cooked_carrot",
    )),
    ("vanilladelight_nullgr:", ["sugars"], (
        "caramel_bottle",
    )),
    ("vegan_delight_nullgr:", ["fruits", "sugars"], (
        "applesauce",
    )),
    ("vegan_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "pasta_with_tofuballs", "tofish_roll", "tofu_burger", "tofu_sandwich",
    )),
    ("vegan_delight_nullgr:", ["proteins"], (
        "cooked_smoked_tofu", "cooked_smoked_tofu_slices", "cooked_tofu", "cooked_tofu_slices", "minced_tofu",
        "silken_tofu", "smoked_tofu", "smoked_tofu_slices", "soybean", "tofu", "tofu_patty", "tofu_slices",
    )),
    ("vegan_delight_nullgr:", ["proteins", "vegetables"], (
        "cooked_smoked_tofish", "cooked_tofish", "roasted_tofu_chops", "smoked_tofish", "smoked_tofish_roll",
        "tofish",
    )),
    ("veggiesdelight_nullgr:", ["grains", "proteins"], (
        "sweet_potato_cupcake",
    )),
    ("veggiesdelight_nullgr:", ["grains", "proteins", "vegetables"], (
        "cauliflower_burger", "chicken_fajitas_wrap",
    )),
    ("veggiesdelight_nullgr:", ["grains", "proteins", "vegetables", "sugars"], (
        "carrot_cake_slice",
    )),
    ("veggiesdelight_nullgr:", ["grains", "proteins", "sugars"], (
        "sweet_potato_mochi",
    )),
    ("veggiesdelight_nullgr:", ["grains", "vegetables"], (
        "cauliflower_bread", "cesar_salad", "mhadjeb", "sweet_potato_dough", "uncooked_mhadjeb", "vegan_pizza_slice",
    )),
    ("veggiesdelight_nullgr:", ["grains", "vegetables", "sugars"], (
        "sweet_potato_pie_slice",
    )),
    ("veggiesdelight_nullgr:", ["proteins", "vegetables"], (
        "cacciatore", "carrot_juice", "cauliflower_patty", "cauliflower_soup", "cooked_cauliflower_patty",
        "dandelion_and_eggs", "fish_and_chips", "mashed_potatoes", "shakshouka", "steak_fajitas",
        "stuffed_bellpeppers",
    )),
    ("veggiesdelight_nullgr:", ["proteins", "vegetables", "sugars"], (
        "beetroot_brownie", "dandelion_juice",
    )),
    ("veggiesdelight_nullgr:", ["vegetables"], (
        "baked_sweet_potato", "bellpepper", "cauliflower", "cauliflower_floret", "fried_cauliflower_floret",
        "potato_noodle", "potato_noodles", "roasted_garlic_clove", "roasted_vegetables", "smoked_bellpepper",
        "sweet_potato", "whole_roasted_cauliflower",
    )),
    ("veggiesdelight_nullgr:", ["vegetables", "sugars"], (
        "fermented_garlic_honey",
    )),
    ("vietnam_delight_nullgr:", ["fruits"], (
        "bell_fruit", "green_kumquat", "kumquat", "rotten_plum",
    )),
    ("vietnam_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "banana_powder", "fried_banana",
    )),
    ("vietnam_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "plum_bread",
    )),
    ("vietnam_delight_nullgr:", ["fruits", "proteins", "vegetables"], (
        "banana_blossom_sour_soup",
    )),
    ("vietnam_delight_nullgr:", ["fruits", "proteins", "vegetables", "sugars"], (
        "plum_sauce_pork_belly",
    )),
    ("vietnam_delight_nullgr:", ["fruits", "proteins", "sugars"], (
        "plum_jelly",
    )),
    ("vietnam_delight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "plum_tea",
    )),
    ("vietnam_delight_nullgr:", ["fruits", "sugars"], (
        "banana", "banana_cake", "golden_plum", "plum", "plum_jam",
    )),
    ("vietnam_delight_nullgr:", ["grains"], (
        "cooked_sticky_rice", "sticky_rice",
    )),
    ("vietnam_delight_nullgr:", ["grains", "vegetables"], (
        "cooked_pandan_rice",
    )),
    ("vietnam_delight_nullgr:", ["proteins", "vegetables"], (
        "banana_blossom_salad", "lotus_rhizome_pork_soup", "lotus_stem_chicken_pandan_soup", "lotus_stem_salad",
        "stirfried_banana_rhizome",
    )),
    ("vietnam_delight_nullgr:", ["vegetables"], (
        "banana_blossom", "banana_blossom_shredded", "banana_stem", "basil_leaf", "bird_eye_chilis",
        "garlic_chili_sauce", "garlic_chives", "ginger", "lolot_leaf", "lotus_embryo", "lotus_rhizome",
        "lotus_rhizome_slice", "onion", "pandan_leaf", "pickled_mustard_greens", "purple_lotus_flower_tea",
        "scallion", "shallot", "turmeric", "white_lotus_flower_tea", "yellow_lotus_flower_tea", "young_lotus_stem",
    )),
    ("vietnam_delight_nullgr:", ["vegetables", "sugars"], (
        "lotus_embryo_tea", "lotus_rhizome_sweet_soup", "lotus_seed_sweet_soup",
    )),
    ("vietnam_delight_nullgr:", ["sugars"], (
        "molasses",
    )),
    ("vintage_delight_nullgr:", ["fruits"], (
        "gearo_berry",
    )),
    ("vintage_delight_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "pb_j",
    )),
    ("vintage_delight_nullgr:", ["fruits", "grains", "proteins", "vegetables", "sugars"], (
        "deluxe_burger",
    )),
    ("vintage_delight_nullgr:", ["fruits", "grains", "proteins", "sugars"], (
        "deluxe_granola_bar", "peanut_butter_and_jelly_sandwich",
    )),
    ("vintage_delight_nullgr:", ["fruits", "grains", "vegetables", "sugars"], (
        "overnight_oats",
    )),
    ("vintage_delight_nullgr:", ["fruits", "grains", "sugars"], (
        "fruity_granola_bar",
    )),
    ("vintage_delight_nullgr:", ["fruits", "vegetables", "sugars"], (
        "cucumber_salad",
    )),
    ("vintage_delight_nullgr:", ["fruits", "sugars"], (
        "apple_sauce_bottle", "apple_sauce_jar", "gearo_berry_jam_bottle", "gearo_berry_jam_jar", "gearo_raisin",
        "glow_berry_jam_bottle", "glow_berry_jam_jar",
    )),
    ("vintage_delight_nullgr:", ["grains"], (
        "oat_dough",
    )),
    ("vintage_delight_nullgr:", ["grains", "proteins", "vegetables"], (
        "cheese_burger", "cheese_pasta", "pad_thai",
    )),
    ("vintage_delight_nullgr:", ["grains", "proteins", "sugars"], (
        "cheese_pizza_slice", "chocolate_nut_granola_bar", "meat_pizza_slice", "peanut_butter_cookie",
    )),
    ("vintage_delight_nullgr:", ["grains", "vegetables"], (
        "stuffed_burrito",
    )),
    ("vintage_delight_nullgr:", ["grains", "sugars"], (
        "oatmeal", "oatmeal_cookie",
    )),
    ("vintage_delight_nullgr:", ["proteins"], (
        "century_egg", "century_egg2", "cheese_curds", "cheese_slice", "magic_peanut", "peanut", "pickled_egg",
        "roasted_peanut", "salted_cod", "salted_salmon", "surstromming",
    )),
    ("vintage_delight_nullgr:", ["proteins", "vegetables"], (
        "ghostly_chili",
    )),
    ("vintage_delight_nullgr:", ["proteins", "sugars"], (
        "honey_roasted_peanut", "nut_mash_bottle", "nut_mash_jar", "nut_milk_bottle", "peanut_butter",
    )),
    ("vintage_delight_nullgr:", ["vegetables"], (
        "cabbage_kimchi", "cucumber_noodles", "ghost_pepper", "pickle_soup", "pickled_beetroot", "pickled_onion",
        "pickled_pepper",
    )),
    ("vintage_delight_nullgr:", ["vegetables", "sugars"], (
        "pepper_jam_bottle", "pepper_jam_jar", "relish_bottle", "relish_jar", "sweet_berry_jam_bottle",
        "sweet_berry_jam_jar", "vinegar_bottle", "vinegar_jar",
    )),
    ("vintage_delight_nullgr:", ["sugars"], (
        "honey_jar",
    )),
    ("winemaking_delight:", ["fruits"], (
        "glittering_grenadine",
    )),
    ("winemaking_delight:", ["fruits", "grains", "sugars"], (
        "mead", "saccharine_rum",
    )),
    ("winemaking_delight:", ["fruits", "sugars"], (
        "apple_jelly", "glow_berry_marmalade", "sweet_berry_jam",
    )),
    ("winemaking_delight:", ["grains"], (
        "beer", "rice_wine",
    )),
    ("winemaking_delight:", ["grains", "proteins", "vegetables"], (
        "cheesy_pasta", "ham_and_cheese_sandwich", "horror_lasagna", "pizza_slice", "red_rum", "scarlet_pierogies",
    )),
    ("winemaking_delight:", ["grains", "vegetables"], (
        "bloody_mary", "kombucha", "salty_folly", "steel_toe_stout", "strongroot_ale", "vodka", "withering_dross",
    )),
    ("winemaking_delight:", ["grains", "vegetables", "sugars"], (
        "pale_jane",
    )),
    ("winemaking_delight:", ["proteins"], (
        "jerky",
    )),
    ("winemaking_delight:", ["proteins", "vegetables"], (
        "dread_nog", "egg_grog", "fiery_fondue", "kippers", "vegetable_omelet",
    )),
    ("winemaking_delight:", ["proteins", "vegetables", "sugars"], (
        "creamy_onion_soup", "flaxen_cheese_wedge", "scarlet_cheese_wedge",
    )),
    ("winemaking_delight:", ["proteins", "sugars"], (
        "cocoa_fudge",
    )),
    ("winemaking_delight:", ["vegetables"], (
        "kimchi",
    )),
    ("winemaking_delight:", ["vegetables", "sugars"], (
        "pickled_pickles",
    )),
):
    for itemName in itemNames:
        farmerDelightDlcFoodGroups[namespacePrefix + itemName] = list(groupIds)
foodGroups.update(farmerDelightDlcFoodGroups)

# 屠宰工艺数据逐项核对物品定义、烹饪锅配方和进食合成链，避免仅按名称推断复合食品原料。
butcherCraftFoodGroups = {}
for groupIds, itemNames in (
    (["fruits", "grains", "proteins", "vegetables"], (
        "rack_lamb",
    )),
    (["fruits", "proteins", "sugars"], (
        "friedfish",
    )),
    (["fruits", "proteins", "vegetables"], (
        "pot_roast",
    )),
    (["grains"], (
        "bread_slice",
    )),
    (["grains", "proteins"], (
        "buttered_toast", "chickenfriedsteak", "friedbrains", "friedchicken", "grilled_cheese",
        "pork_tenderloin", "sausage_roll", "sausageinbun", "sos",
    )),
    (["grains", "proteins", "vegetables"], (
        "beef_wellington", "mashed_potato_gravy", "salisbury_steak",
    )),
    (["grains", "proteins", "vegetables", "sugars"], (
        "pulled_pork_sandwich",
    )),
    (["proteins"], (
        "beef_jerky", "beef_rib", "beef_scraps", "brain", "butter", "cheese", "cooked_beef_rib",
        "cooked_beef_scraps", "cooked_brain", "cooked_cubed_beef", "cooked_cubed_lamb", "cooked_cubed_pork",
        "cooked_ground_beef", "cooked_ground_lamb", "cooked_ground_pork", "cooked_heart", "cooked_kidney",
        "cooked_lamb_rib", "cooked_lamb_ribs", "cooked_lamb_roast", "cooked_lamb_scraps", "cooked_liver",
        "cooked_lung", "cooked_oxtail", "cooked_pork_rib", "cooked_pork_ribs", "cooked_pork_roast",
        "cooked_pork_scraps", "cooked_ribs", "cooked_roast", "cooked_stew_beef", "cooked_stew_lamb",
        "cooked_stew_pork", "cooked_stomach", "cooked_tongue", "cooked_tripe", "cubed_beef", "cubed_lamb",
        "cubed_pork", "ground_beef", "ground_lamb", "ground_pork", "heart", "jelly_black", "jelly_blue",
        "jelly_brown", "jelly_cyan", "jelly_green", "jelly_grey", "jelly_light_blue", "jelly_light_grey",
        "jelly_lime", "jelly_magenta", "jelly_orange", "jelly_pink", "jelly_purple", "jelly_red",
        "jelly_white", "jelly_yellow", "kidney", "lamb_jerky", "lamb_rib", "lamb_ribs", "lamb_roast",
        "lamb_scraps", "liver", "lung", "oxtail", "pork_jerky", "pork_rib", "pork_ribs", "pork_roast",
        "pork_scraps", "ribs", "roast", "sausage", "sausagecooked", "stew_beef", "stew_lamb", "stew_pork",
        "stomach", "tongue", "tripe",
    )),
    (["proteins", "vegetables"], (
        "broth", "haggis", "lamb_stew", "liver_onions", "meat_pie_slice", "oxtail_soup", "pork_stew",
        "stirfry", "stuffedheart",
    )),
    (["proteins", "vegetables", "sugars"], (
        "bbq_ribs", "hash",
    )),
    (["vegetables"], (
        "frenchfries",
    )),
    (["vegetables", "sugars"], (
        "ketchup",
    )),
):
    for itemName in itemNames:
        butcherCraftFoodGroups["butchercraft_nullgr:" + itemName] = list(groupIds)
foodGroups.update(butcherCraftFoodGroups)

# 巴西乐事数据逐项核对标准配方和烹饪锅配方；同一成品存在多种配方时采用原料类别并集。
brazilianDelightFoodGroups = {}
for groupIds, itemNames in (
    (["fruits"], (
        "acai_berries", "coconut_drink", "coconut_milk", "coconut_slice", "coffee_berries", "guarana_fruit",
        "guarana_powder", "lemon", "lemon_slice",
    )),
    (["fruits", "grains", "proteins", "sugars"], (
        "plate_of_canjica",
    )),
    (["fruits", "grains", "proteins", "vegetables"], (
        "salpicao",
    )),
    (["fruits", "proteins", "sugars"], (
        "acai_cream", "beijinho", "brigadeiro_ball", "chocolate_love_apple", "coconut_cream",
        "coconut_sweet", "powdered_peanut_candy", "quindim", "sweet_love_apple",
    )),
    (["fruits", "proteins", "vegetables"], (
        "plate_of_fried_fish_with_acai", "plate_of_fish_moqueca",
    )),
    (["fruits", "sugars"], (
        "acai_tea_with_guarana", "caipirinha", "guarana_juice", "guarana_soda", "lemonade",
    )),
    (["fruits", "vegetables", "sugars"], (
        "collard_lemonade",
    )),
    (["grains"], (
        "angu", "brazilian_rice", "cooked_corn", "corn", "corn_flour", "corn_on_a_stick",
        "grilled_corn_on_a_stick", "kernels", "pastel_dough", "white_kernels",
    )),
    (["grains", "proteins"], (
        "brazilian_breakfast", "brazilian_dinner", "bread_with_butter", "buttered_corn", "corn_meal",
        "couscous",
    )),
    (["grains", "proteins", "sugars"], (
        "corn_porridge", "sweet_rice",
    )),
    (["grains", "proteins", "vegetables"], (
        "broa", "cassava_fritters", "coxinha", "raw_cassava_fritters", "raw_coxinha",
    )),
    (["grains", "proteins", "vegetables", "sugars"], (
        "carrot_cake_slice", "carrot_cake_with_chocolate_slice", "chicken_pot_pie_slice",
    )),
    (["grains", "vegetables"], (
        "garlic_bread", "pastel", "raw_pastel",
    )),
    (["proteins"], (
        "bean_pod", "black_beans", "butter", "carioca_beans", "cooked_shrimp",
        "grilled_cheese_on_a_stick", "heavy_cream_bucket", "minas_cheese_on_a_stick", "minas_cheese_slice",
        "shrimp",
    )),
    (["proteins", "sugars"], (
        "brigadeiro_cream", "cajuzinho", "condensed_milk", "milk_caramel", "peanut_brittle",
        "pudding_slice",
    )),
    (["proteins", "vegetables"], (
        "cheese_bread", "cheese_bread_dough", "collard_greens_farofa", "cooked_black_beans",
        "cooked_carioca_beans", "fried_cassava_with_butter", "plate_of_feijoada", "plate_of_green_soup",
        "plate_of_stroganoff", "tropeiro_beans",
    )),
    (["vegetables"], (
        "cassava_flour", "cassava_root", "chimarrao", "coffee_beans", "collard_greens", "collard_greens_salad",
        "dried_yerba_mate", "garlic_bulb", "garlic_clove", "roasted_garlic", "tucupi",
        "yerba_mate_leaves",
    )),
    (["sugars"], (
        "garapa",
    )),
):
    for itemName in itemNames:
        brazilianDelightFoodGroups["brazilian_delight_nullgr:" + itemName] = list(groupIds)
foodGroups.update(brazilianDelightFoodGroups)

effectDescriptions = {}
for effectId in effectOrder:
    effectDescriptions[effectId] = dietEffects[effectId]["description"]
for penaltyId in penaltyOrder:
    effectDescriptions[penaltyId] = dietPenalties[penaltyId]["description"]
