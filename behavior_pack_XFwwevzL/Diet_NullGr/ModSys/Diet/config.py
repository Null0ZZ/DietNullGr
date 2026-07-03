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
settingActiveKey = "diet_active"
settingGroupPrefix = "diet_track_"
settingTargetText = "自己"
controlToggle = "toggle"

serverSysKey = {
}

clientSysKey = {
}

attrPrefix = "diet_nullgr_"
effectRefreshTick = 120
gainPenaltyPerGroup = 15.0
decayPenaltyPerGroup = 15.0
deathPenaltyMin = 0.0
deathPenaltyLoss = 1.0
expBase = 2.718281828

groupOrder = ["fruits", "grains", "proteins", "vegetables", "sugars"]

groups = {
    "fruits": {
        "name": "水果",
        "tooltip": "你摄入的水果、浆果与甜瓜类食物。",
        "icon": "minecraft:apple",
        "color": [212, 28, 83],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "grains": {
        "name": "谷物",
        "tooltip": "你摄入的面包、小麦、蛋糕等谷物来源。",
        "icon": "minecraft:bread",
        "color": [212, 163, 28],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "proteins": {
        "name": "蛋白质",
        "tooltip": "你摄入的肉类、鱼、蛋和奶类来源。",
        "icon": "minecraft:cooked_beef",
        "color": [212, 120, 28],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "vegetables": {
        "name": "蔬菜",
        "tooltip": "你摄入的根茎、蘑菇、海带和蔬菜汤。",
        "icon": "minecraft:carrot",
        "color": [49, 212, 28],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    },
    "sugars": {
        "name": "糖分",
        "tooltip": "你摄入的糖、蜂蜜、甜点与高糖食物。",
        "icon": "minecraft:honey_bottle",
        "color": [255, 143, 233],
        "defaultValue": 0.0,
        "gainMultiplier": 1.0,
        "decayMultiplier": 1.0
    }
}

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

effectDescriptions = {
    "balanced": "主食、水果、蔬菜、蛋白质均超过80%：获得生命提升、力量、抗性。",
    "sugarRush": "糖分超过80%：获得速度，但同时获得饥饿。"
}
