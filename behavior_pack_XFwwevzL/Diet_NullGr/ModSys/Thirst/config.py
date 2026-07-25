# -*- coding: utf-8 -*-

ssname = "Thirst_Core_ServerSys"
csname = "Thirst_Core_ClientSys"
ssPath = "Diet_NullGr.ModSys.Thirst.Thirst_ss.ServerSys"
csPath = "Diet_NullGr.ModSys.Thirst.Thirst_cs.ClientSys"

serverSysKey = {
    ssname: ssPath
}

clientSysKey = {
    csname: csPath
}

uiKey = "thirst_hud"
uiName = "thirst_hud.main"
uiPath = "Diet_NullGr.ModSys.Thirst.ThirstHUD.ThirstHUD"

maxValue = 20.0
defaultValue = 20.0
displayMaxValue = 20
criticalValue = 6.0
baseDecayIntervalTick = 20
baseDecayPerSecond = 1.0 / 180.0
hungerDecayFactor = 0.2
dataSaveIntervalTick = 600
respawnValue = 20.0
dehydrationDamageIntervalTick = 80
dehydrationDamage = 1.0
easyDehydrationMinHealth = 10.0
normalDehydrationMinHealth = 1.0

playerEatDrinkEvent = "PlayerEatFoodServerEvent"
actorUseDrinkEvent = "ActorUseItemServerEvent"

drinkItemValues = {
    "minecraft:milk_bucket": {
        "event": playerEatDrinkEvent,
        "defaultValue": 8.0,
        "auxValues": {}
    },
    # 水瓶与可饮用药水共用同一物品 ID；水瓶使用附加值 0，其余药水暂用默认补水量。
    "minecraft:potion": {
        "event": actorUseDrinkEvent,
        "defaultValue": 4.0,
        "auxValues": {
            0: 6.0
        }
    }
}

# 外部模组的饮品和液态餐均在进食完成事件结算，静态表只保存每个物品的差异化恢复值。
# 审查来源：FarmerDelightDlc_All/.口渴值数据，外部模组源码快照 3f1ab82efa9f0cf93a78abeed9339790fb6bb74e。
foodDrinkDefaultValues = {
    # 数据来源：argentina_delight_BP
    "argentina_delight_nullgr:mate_apple_item": 5.0,
    "argentina_delight_nullgr:mate_berry_item": 5.0,
    "argentina_delight_nullgr:mate_glow_berry_item": 5.0,
    "argentina_delight_nullgr:mate_item": 5.0,
    "argentina_delight_nullgr:mate_lime_item": 5.0,
    "argentina_delight_nullgr:mate_melon_item": 5.0,
    "argentina_delight_nullgr:mate_milk_item": 5.0,
    "argentina_delight_nullgr:mate_sugar_item": 5.0,
    # 数据来源：BakingDelight_BP
    "bakingdelight_nullgr:cream_of_mushroom_soup": 3.0,
    "bakingdelight_nullgr:french_onion_soup": 4.0,
    # 数据来源：BamBooTeaDelight_BP
    "tea_delight_nullgr:ceramic_teacup_black_tea": 3.0,
    "tea_delight_nullgr:ceramic_teacup_green_tea": 3.0,
    "tea_delight_nullgr:ceramic_teacup_matcha_tea": 3.0,
    "tea_delight_nullgr:ceramic_teacup_oolong_tea": 3.0,
    "tea_delight_nullgr:ceramic_teacup_red_tea": 3.0,
    "tea_delight_nullgr:ceramic_teacup_white_tea": 3.0,
    "tea_delight_nullgr:ceramic_teacup_yellow_tea": 3.0,
    # 数据来源：behavior_pack_57aCr2yh
    "silents_delight_nullgr:sculk_shrieker_shake": 4.0,
    "silents_delight_nullgr:sculk_soup": 4.0,
    # 数据来源：behavior_pack_A54KFeFE
    "green_delight_nullgr:cactus_cola": 5.0,
    "green_delight_nullgr:cactus_juice": 5.0,
    # 数据来源：behavior_pack_FNLDmFMv
    "frightsdelight_nullgr:punch_ghasttear": 2.0,
    "frightsdelight_nullgr:punch_slimeapple": 3.0,
    "frightsdelight_nullgr:punch_soul_berry": 2.0,
    "frightsdelight_nullgr:punch_spidereye": 2.0,
    "frightsdelight_nullgr:punch_wither_berry": 2.0,
    "frightsdelight_nullgr:soup_rotten_flesh": 4.0,
    "frightsdelight_nullgr:soup_slime": 4.0,
    "frightsdelight_nullgr:soup_spider_eye": 4.0,
    # 数据来源：behavior_pack_G43dZXg2
    "endersdelight:amberveil_stew": 3.0,
    "endersdelight:amberveiled_curry": 3.0,
    "endersdelight:chicken_curry": 3.0,
    "endersdelight:chorus_juice": 5.0,
    "endersdelight:chorus_stew": 3.0,
    "endersdelight:chorus_stew_wood": 3.0,
    "endersdelight:endermite_stew": 3.0,
    "endersdelight:endermite_stew_wood": 3.0,
    # 数据来源：behavior_pack_GBHBBfXS
    "muffins_thaidelight_nullgr:bamboo_shoot_soup": 4.0,
    "muffins_thaidelight_nullgr:butterfly_pea_tea": 5.0,
    "muffins_thaidelight_nullgr:durian_curry": 3.0,
    "muffins_thaidelight_nullgr:lime_juice": 5.0,
    "muffins_thaidelight_nullgr:papaya_juice": 5.0,
    # 数据来源：behavior_pack_H60M18ao
    "newyear_delight_nullgr:tangyuan": 3.0,
    "newyear_delight_nullgr:tangyuan_beanpaste": 3.0,
    "newyear_delight_nullgr:tangyuan_blueberry": 3.0,
    "newyear_delight_nullgr:tangyuan_cheese": 3.0,
    "newyear_delight_nullgr:tangyuan_chocolate": 3.0,
    "newyear_delight_nullgr:tangyuan_durian": 3.0,
    "newyear_delight_nullgr:tangyuan_hawthorn": 3.0,
    "newyear_delight_nullgr:tangyuan_matcha": 3.0,
    "newyear_delight_nullgr:tangyuan_peanut": 3.0,
    "newyear_delight_nullgr:tangyuan_pineapple": 3.0,
    "newyear_delight_nullgr:tangyuan_pork": 3.0,
    "newyear_delight_nullgr:tangyuan_shrimp": 3.0,
    "newyear_delight_nullgr:tangyuan_strawberry": 3.0,
    "newyear_delight_nullgr:tangyuan_taropaste": 3.0,
    # 数据来源：behavior_pack_lp18gR25
    "winemaking_delight:beer": 3.0,
    "winemaking_delight:bloody_mary": 1.0,
    "winemaking_delight:creamy_onion_soup": 3.0,
    "winemaking_delight:dread_nog": 2.0,
    "winemaking_delight:egg_grog": 2.0,
    "winemaking_delight:fiery_fondue": 3.0,
    "winemaking_delight:glittering_grenadine": 2.0,
    "winemaking_delight:kombucha": 3.0,
    "winemaking_delight:mead": 2.0,
    "winemaking_delight:pale_jane": 3.0,
    "winemaking_delight:red_rum": 1.0,
    "winemaking_delight:rice_wine": 2.0,
    "winemaking_delight:saccharine_rum": 1.0,
    "winemaking_delight:salty_folly": 2.0,
    "winemaking_delight:steel_toe_stout": 3.0,
    "winemaking_delight:strongroot_ale": 3.0,
    "winemaking_delight:vodka": 1.0,
    "winemaking_delight:withering_dross": 2.0,
    # 数据来源：behavior_pack_NvOh95Bs
    "coconut_delight_nullgr:bowl_coconut_fishing": 4.0,
    "coconut_delight_nullgr:cocnut_milkfish": 3.0,
    "coconut_delight_nullgr:coconut_chicken": 3.0,
    "coconut_delight_nullgr:coconut_chicken_bowl": 3.0,
    "coconut_delight_nullgr:coconut_milk": 5.0,
    "coconut_delight_nullgr:coconut_water": 6.0,
    "coconut_delight_nullgr:crab_meat_casserole": 3.0,
    # 数据来源：behavior_pack_OqBizuzL
    "expanded_delight_nullgr:asparagus_soup": 3.0,
    "expanded_delight_nullgr:asparagus_soup_creamy": 3.0,
    "expanded_delight_nullgr:cranberry_juice": 5.0,
    "expanded_delight_nullgr:glow_berry_juice": 5.0,
    "expanded_delight_nullgr:peanut_honey_soup": 3.0,
    "expanded_delight_nullgr:sweet_berry_juice": 5.0,
    # 数据来源：behavior_pack_PNyiSH2B
    "nether_delight_nullgr:crimson_stroganoff": 3.0,
    "nether_delight_nullgr:rock_soup": 4.0,
    "nether_delight_nullgr:spicy_curry": 3.0,
    "nether_delight_nullgr:spicy_hoglin_stew": 3.0,
    "nether_delight_nullgr:spicy_noodle_soup": 4.0,
    "nether_delight_nullgr:strider_stew": 3.0,
    # 数据来源：behavior_pack_rSLi2Sva
    "rusticdelight_nullgr:bell_pepper_soup": 4.0,
    "rusticdelight_nullgr:chocolate_coffee": 4.0,
    "rusticdelight_nullgr:coffee": 4.0,
    "rusticdelight_nullgr:coffee_braised_beef": 3.0,
    "rusticdelight_nullgr:dark_coffee": 4.0,
    "rusticdelight_nullgr:honey_coffee": 4.0,
    "rusticdelight_nullgr:milk_coffee": 4.0,
    "rusticdelight_nullgr:syrup_coffee": 4.0,
    # 数据来源：behavior_pack_ZddxNft7
    "delightful_nullgr:azalea_tea": 5.0,
    "delightful_nullgr:berry_matcha_latte": 5.0,
    "delightful_nullgr:cactus_chili": 3.0,
    "delightful_nullgr:cactus_soup": 4.0,
    "delightful_nullgr:cactus_soup_cup": 3.0,
    "delightful_nullgr:coconut_curry": 3.0,
    "delightful_nullgr:ender_nectar": 5.0,
    "delightful_nullgr:lavender_tea": 5.0,
    "delightful_nullgr:matcha_latte": 5.0,
    "delightful_nullgr:matcha_milkshake": 4.0,
    "delightful_nullgr:prickly_pear_juice": 5.0,
    "delightful_nullgr:salmonberry_milkshake": 4.0,
    "delightful_nullgr:sinigang": 4.0,
    # 数据来源：ButcherDelight_DLC_Fish_BP
    "butchercraft_nullgr:carrot_fish_soup": 4.0,
    "butchercraft_nullgr:fish_bone_stock": 4.0,
    "butchercraft_nullgr:fish_eye_soup": 4.0,
    "butchercraft_nullgr:fish_kelp_porridge": 3.0,
    "butchercraft_nullgr:fish_maw_five_son_soup": 4.0,
    "butchercraft_nullgr:fish_zhu": 3.0,
    "butchercraft_nullgr:fishbone_seaweed_soup": 4.0,
    "butchercraft_nullgr:sour_soup_bass": 4.0,
    "butchercraft_nullgr:tofu_with_fish_head": 4.0,
    "butchercraft_nullgr:tomato_onion_fish_slice": 3.0,
    # 数据来源：ButcherDelight_DLC_Up_BP
    "butcher_delight_nullgr:blood_bucket": 8.0,
    # 数据来源：CasualnessDelight_BP
    "casualness_delight_nullgr:beef_noodles": 4.0,
    # 数据来源：CollectorDelight_BP
    "collectors_delight_nullgr:berry_limeade": 5.0,
    "collectors_delight_nullgr:clam_chowder": 3.0,
    "collectors_delight_nullgr:clam_meatball_stew": 3.0,
    "collectors_delight_nullgr:clam_meatball_stew_cup": 3.0,
    "collectors_delight_nullgr:crab_miso": 4.0,
    "collectors_delight_nullgr:crimson_carrot_roast": 3.0,
    "collectors_delight_nullgr:deific_blood": 4.0,
    "collectors_delight_nullgr:dragon_stew": 3.0,
    "collectors_delight_nullgr:dragon_stew_cup": 3.0,
    "collectors_delight_nullgr:dragons_passion": 4.0,
    "collectors_delight_nullgr:heavens_cream": 4.0,
    "collectors_delight_nullgr:hermits_sour": 2.0,
    "collectors_delight_nullgr:limbo_brew": 4.0,
    "collectors_delight_nullgr:lime_green_tea": 5.0,
    "collectors_delight_nullgr:lime_milkshake": 4.0,
    "collectors_delight_nullgr:limeade": 5.0,
    "collectors_delight_nullgr:long_limbo_brew": 4.0,
    "collectors_delight_nullgr:long_sweet_recovery": 4.0,
    "collectors_delight_nullgr:lucuma_gazpacho": 4.0,
    "collectors_delight_nullgr:lucuma_gazpacho_cup": 3.0,
    "collectors_delight_nullgr:lucuma_milkshake": 4.0,
    "collectors_delight_nullgr:mint_limeade": 5.0,
    "collectors_delight_nullgr:pink_dragon_fruit_milkshake": 4.0,
    "collectors_delight_nullgr:pink_limeade": 5.0,
    "collectors_delight_nullgr:platinum_bass_stew": 3.0,
    "collectors_delight_nullgr:platinum_bass_stew_cup": 3.0,
    "collectors_delight_nullgr:pomegranate_black_tea": 5.0,
    "collectors_delight_nullgr:pomegranate_milkshake": 4.0,
    "collectors_delight_nullgr:pomegranate_mutton": 3.0,
    "collectors_delight_nullgr:pomegranate_pork": 3.0,
    "collectors_delight_nullgr:pomegranate_smoothie": 4.0,
    "collectors_delight_nullgr:portobello_rice_soup": 3.0,
    "collectors_delight_nullgr:portobello_rice_soup_cup": 3.0,
    "collectors_delight_nullgr:prawn_stew": 3.0,
    "collectors_delight_nullgr:prawn_stew_cup": 3.0,
    "collectors_delight_nullgr:reanimators_garden": 4.0,
    "collectors_delight_nullgr:rose_moon": 4.0,
    "collectors_delight_nullgr:strong_limbo_brew": 4.0,
    "collectors_delight_nullgr:strong_limeade": 5.0,
    "collectors_delight_nullgr:strong_sweet_recovery": 4.0,
    "collectors_delight_nullgr:strong_vernal_purge": 4.0,
    "collectors_delight_nullgr:sweet_recovery": 4.0,
    "collectors_delight_nullgr:vernal_purge": 4.0,
    # 数据来源：Corn_Delight_BP
    "corn_delight:corn_soup": 3.0,
    "corn_delight:creamy_corn_drink": 5.0,
    # 数据来源：CrabberDelight_BP
    "crabber_delight_nullgr:bisque": 3.0,
    "crabber_delight_nullgr:clam_bake": 3.0,
    "crabber_delight_nullgr:clam_chowder": 3.0,
    "crabber_delight_nullgr:kelp_shake": 4.0,
    "crabber_delight_nullgr:sea_pickle_juice": 5.0,
    "crabber_delight_nullgr:seafood_gumbo": 3.0,
    # 数据来源：CulturalDelight_BP
    "cultural_delight_nullgr:spicy_curry": 3.0,
    # 数据来源：DragonBoatFestival_BP
    "dragon_boat_festival_nullgr:green_bean_paste": 4.0,
    "dragon_boat_festival_nullgr:green_juice": 5.0,
    "dragon_boat_festival_nullgr:jujube_porridge": 3.0,
    "dragon_boat_festival_nullgr:soy_milk": 6.0,
    # 数据来源：DumplingDelight_BP
    "dumpling_delight_nullgr:pork_cabbage_wonton": 4.0,
    "dumpling_delight_nullgr:pork_carrot_wonton": 4.0,
    "dumpling_delight_nullgr:pork_mushroom_wonton": 4.0,
    # 数据来源：EnderDelight_BP
    "ender_delight_nullgr:bubble_tea": 5.0,
    "ender_delight_nullgr:chorus_flower_tea": 5.0,
    "ender_delight_nullgr:chorus_fruit_milk_tea": 5.0,
    "ender_delight_nullgr:chorus_fruit_wine": 2.0,
    "ender_delight_nullgr:dragon_breath_and_chorus_soup": 4.0,
    "ender_delight_nullgr:dragon_meat_stew": 3.0,
    "ender_delight_nullgr:ender_congee": 3.0,
    "ender_delight_nullgr:ender_noodle": 4.0,
    "ender_delight_nullgr:enderman_gristle_stew": 3.0,
    "ender_delight_nullgr:itemdragon_breath_soda": 5.0,
    "ender_delight_nullgr:shulker_soup": 4.0,
    # 数据来源：ExtravagantDelight_BP
    "extravagantdelight_nullgr:apple_yogurt": 4.0,
    "extravagantdelight_nullgr:beer_beef_stew": 3.0,
    "extravagantdelight_nullgr:black_beer": 3.0,
    "extravagantdelight_nullgr:blueberry_yogurt": 4.0,
    "extravagantdelight_nullgr:glow_berry_yogurt": 4.0,
    "extravagantdelight_nullgr:green_mango_frappe": 4.0,
    "extravagantdelight_nullgr:india_pale_ale": 3.0,
    "extravagantdelight_nullgr:malt_stew": 3.0,
    "extravagantdelight_nullgr:mango_gazpacho": 4.0,
    "extravagantdelight_nullgr:mango_juice": 5.0,
    "extravagantdelight_nullgr:mango_liquor": 1.0,
    "extravagantdelight_nullgr:mango_milkshake": 4.0,
    "extravagantdelight_nullgr:mango_wine": 2.0,
    "extravagantdelight_nullgr:mango_yogurt": 4.0,
    "extravagantdelight_nullgr:pale_ale": 3.0,
    "extravagantdelight_nullgr:pink_gin": 1.0,
    "extravagantdelight_nullgr:porter_beer": 3.0,
    "extravagantdelight_nullgr:quince_juice": 5.0,
    "extravagantdelight_nullgr:quince_milkshake": 4.0,
    "extravagantdelight_nullgr:quince_wine": 2.0,
    "extravagantdelight_nullgr:raspberry_yogurt": 4.0,
    "extravagantdelight_nullgr:rhubarb_gin": 1.0,
    "extravagantdelight_nullgr:rhubarb_liquor": 1.0,
    "extravagantdelight_nullgr:rhubarb_milkshake": 4.0,
    "extravagantdelight_nullgr:rhubarb_wine": 2.0,
    "extravagantdelight_nullgr:sloe_berry_juice": 5.0,
    "extravagantdelight_nullgr:sloe_berry_milkshake": 4.0,
    "extravagantdelight_nullgr:sloe_berry_wine": 2.0,
    "extravagantdelight_nullgr:sloe_berry_yogurt": 4.0,
    "extravagantdelight_nullgr:sloe_gin": 1.0,
    "extravagantdelight_nullgr:sloe_vodka": 1.0,
    "extravagantdelight_nullgr:starfruit_juice": 5.0,
    "extravagantdelight_nullgr:starfruit_milkshake": 4.0,
    "extravagantdelight_nullgr:starfruit_paloma": 1.0,
    "extravagantdelight_nullgr:starfruit_wine": 2.0,
    "extravagantdelight_nullgr:starfruit_yogurt": 4.0,
    "extravagantdelight_nullgr:strawberry_yogurt": 4.0,
    "extravagantdelight_nullgr:sweet_berry_yogurt": 4.0,
    # 数据来源：Farmer_Respite_BP
    "farmer_respite_nullgr:black_cod": 3.0,
    "farmer_respite_nullgr:black_tea": 5.0,
    "farmer_respite_nullgr:black_tea_honey": 5.0,
    "farmer_respite_nullgr:black_tea_milk": 5.0,
    "farmer_respite_nullgr:coffe_honey": 4.0,
    "farmer_respite_nullgr:coffee": 4.0,
    "farmer_respite_nullgr:coffee_milk": 4.0,
    "farmer_respite_nullgr:dandelion_tea": 5.0,
    "farmer_respite_nullgr:dandelion_tea_milk": 5.0,
    "farmer_respite_nullgr:green_tea": 5.0,
    "farmer_respite_nullgr:green_tea_honey": 5.0,
    "farmer_respite_nullgr:green_tea_milk": 5.0,
    "farmer_respite_nullgr:purulent_tea": 5.0,
    "farmer_respite_nullgr:purulent_tea_honey": 5.0,
    "farmer_respite_nullgr:rose_hip_tea": 5.0,
    "farmer_respite_nullgr:rose_hip_tea_honey": 5.0,
    "farmer_respite_nullgr:tea_curry": 3.0,
    "farmer_respite_nullgr:yellow_tea": 5.0,
    "farmer_respite_nullgr:yellow_tea_honey": 5.0,
    "farmer_respite_nullgr:yellow_tea_milk": 5.0,
    # 数据来源：Fastfood_Delight_BP
    "fastfood_delight_nullgr:cola_soda": 5.0,
    "fastfood_delight_nullgr:creaming_soda": 5.0,
    "fastfood_delight_nullgr:iced_tea": 5.0,
    "fastfood_delight_nullgr:lemon_soda": 5.0,
    "fastfood_delight_nullgr:orange_soda": 5.0,
    # 数据来源：FestiveDelight_BP
    "festive_delight_nullgr:christmas_tea": 5.0,
    # 数据来源：ForagerSinsight_BP
    "foragersinsight_nullgr:carrot_poppy_chowder": 3.0,
    "foragersinsight_nullgr:cod_and_pumpkin_stew": 3.0,
    "foragersinsight_nullgr:dandelion_root_tea": 5.0,
    "foragersinsight_nullgr:forest_elixir": 4.0,
    "foragersinsight_nullgr:glowing_carrot_juice": 5.0,
    "foragersinsight_nullgr:rose_cordial": 5.0,
    "foragersinsight_nullgr:rose_granita": 4.0,
    "foragersinsight_nullgr:seed_milk_bottle": 6.0,
    "foragersinsight_nullgr:seed_milk_bucket": 8.0,
    # 数据来源：HearthAndHarvest_BP
    "hearthandharvest_nullgr:blueberry_juice": 5.0,
    "hearthandharvest_nullgr:blueberry_wine": 2.0,
    "hearthandharvest_nullgr:cherry_juice": 5.0,
    "hearthandharvest_nullgr:cherry_wine": 2.0,
    "hearthandharvest_nullgr:goat_milk_bottle": 6.0,
    "hearthandharvest_nullgr:green_grape_juice": 5.0,
    "hearthandharvest_nullgr:green_grape_wine": 2.0,
    "hearthandharvest_nullgr:mead": 2.0,
    "hearthandharvest_nullgr:onion_soup": 4.0,
    "hearthandharvest_nullgr:raspberry_juice": 5.0,
    "hearthandharvest_nullgr:raspberry_wine": 2.0,
    "hearthandharvest_nullgr:red_grape_juice": 5.0,
    "hearthandharvest_nullgr:red_grape_wine": 2.0,
    "hearthandharvest_nullgr:wine": 2.0,
    # 数据来源：LargeMeals_BP
    "large_meals_nullgr:chicken_curry": 3.0,
    "large_meals_nullgr:potato_soup": 3.0,
    "large_meals_nullgr:pufferfish_broth": 4.0,
    "large_meals_nullgr:red_soup": 4.0,
    "large_meals_nullgr:rice_pudding": 3.0,
    "large_meals_nullgr:sweet_berry_custard": 3.0,
    "large_meals_nullgr:tomato_egg_soup": 3.0,
    # 数据来源：LavsDelight_BP
    "lavsdelight_nullgr:apple_cabbage_stew": 3.0,
    "lavsdelight_nullgr:carbonated_water": 6.0,
    "lavsdelight_nullgr:cola": 5.0,
    "lavsdelight_nullgr:lemon_juice": 5.0,
    "lavsdelight_nullgr:lemon_tea": 5.0,
    "lavsdelight_nullgr:lemonade": 5.0,
    "lavsdelight_nullgr:mint_tea": 5.0,
    "lavsdelight_nullgr:sweet_berry_juice": 5.0,
    # 数据来源：MidAutumnDelight_BP
    "midautumndelight_nullgr:osmanthus_flowers_wine": 2.0,
    # 数据来源：MilkCreamDelight_BP
    "milk_cream_delight_nullgr:bubble_tea": 5.0,
    "milk_cream_delight_nullgr:bumper_passion_fruit": 5.0,
    "milk_cream_delight_nullgr:cheese_peach": 5.0,
    "milk_cream_delight_nullgr:cheese_strawberry": 5.0,
    "milk_cream_delight_nullgr:cherry_berry": 5.0,
    "milk_cream_delight_nullgr:cloud_matcha": 5.0,
    "milk_cream_delight_nullgr:coconut_jelly_coconut_green": 5.0,
    "milk_cream_delight_nullgr:domineering_cheese_strawberry": 5.0,
    "milk_cream_delight_nullgr:domineering_cherry": 5.0,
    "milk_cream_delight_nullgr:forest_rose": 5.0,
    "milk_cream_delight_nullgr:iced_americano": 4.0,
    "milk_cream_delight_nullgr:lemon_black_tea": 5.0,
    "milk_cream_delight_nullgr:lemonade": 5.0,
    "milk_cream_delight_nullgr:mango_pomelo_sago": 4.0,
    "milk_cream_delight_nullgr:matcha_mango_milk": 4.0,
    "milk_cream_delight_nullgr:moonlight_own_goal": 5.0,
    "milk_cream_delight_nullgr:oat_coffee": 4.0,
    "milk_cream_delight_nullgr:orange_american": 4.0,
    "milk_cream_delight_nullgr:peach_jelly": 5.0,
    "milk_cream_delight_nullgr:peach_own_goal": 5.0,
    "milk_cream_delight_nullgr:purple_grape_cheese": 5.0,
    "milk_cream_delight_nullgr:raw_coconut_durian": 4.0,
    "milk_cream_delight_nullgr:raw_coconut_latte": 4.0,
    "milk_cream_delight_nullgr:taro_grape": 4.0,
    "milk_cream_delight_nullgr:xueding_coffee": 4.0,
    # 数据来源：MilletDelight_BP
    "milet_delight_nullgr:bone_millet_noodles": 4.0,
    "milet_delight_nullgr:glow_berry_wine": 2.0,
    "milet_delight_nullgr:millet_gruel": 3.0,
    "milet_delight_nullgr:millet_pumpkin_soup": 3.0,
    "milet_delight_nullgr:millet_vegetable_soup": 3.0,
    "milet_delight_nullgr:millet_wine": 2.0,
    "milet_delight_nullgr:wheat_wine": 2.0,
    # 数据来源：MinersDelight_BP
    "miners_delight:baked_cod_stew_cup": 3.0,
    "miners_delight:bat_soup": 4.0,
    "miners_delight:bat_soup_cup": 3.0,
    "miners_delight:beef_stew_cup": 3.0,
    "miners_delight:beetroot_soup_cup": 3.0,
    "miners_delight:bone_broth_cup": 3.0,
    "miners_delight:cave_soup": 4.0,
    "miners_delight:cave_soup_cup": 3.0,
    "miners_delight:chicken_soup_cup": 3.0,
    "miners_delight:fish_stew_cup": 3.0,
    "miners_delight:hot_cocoa_cup": 3.0,
    "miners_delight:insect_stew": 3.0,
    "miners_delight:insect_stew_cup": 3.0,
    "miners_delight:milk_cup": 3.0,
    "miners_delight:mushroom_stew_cup": 3.0,
    "miners_delight:noodle_soup_cup": 3.0,
    "miners_delight:pumpkin_soup_cup": 3.0,
    "miners_delight:rabbit_stew_cup": 3.0,
    "miners_delight:vegetable_soup_cup": 3.0,
    # 数据来源：NaturalDelight__BP
    "natural_delight_nullgr:acacia_flower_soup": 4.0,
    "natural_delight_nullgr:acacia_scented_tea": 5.0,
    "natural_delight_nullgr:birch_juice": 5.0,
    "natural_delight_nullgr:peony_flower_tea": 5.0,
    "natural_delight_nullgr:pine_nut_porridge": 3.0,
    "natural_delight_nullgr:rose_tea": 5.0,
    "natural_delight_nullgr:shiyan_mountain_clove_tea": 5.0,
    "natural_delight_nullgr:stewed_chicken_with_clove_face": 3.0,
    # 数据来源：NetherDelight_BP
    "nether_delight_nullgr:strider_moss_stew": 3.0,
    # 数据来源：Ocean_Delight_BP
    "ocean_delight_nullgr:bowl_of_guardian_soup": 4.0,
    "ocean_delight_nullgr:braised_sea_pickle": 3.0,
    "ocean_delight_nullgr:puffish_soup": 4.0,
    # 数据来源：OceanicDelight_BP
    "oceanic_delight_nullgr:fish_egg_noodle_soup": 4.0,
    "oceanic_delight_nullgr:glows_squid_stew": 3.0,
    "oceanic_delight_nullgr:nautilus_kelp_juice": 5.0,
    "oceanic_delight_nullgr:sea_grape_juice": 5.0,
    "oceanic_delight_nullgr:shrimp_stew": 3.0,
    # 数据来源：RamadanDelight_BP
    "ramadandelight_nullgr:chorba": 4.0,
    "ramadandelight_nullgr:haleem": 3.0,
    "ramadandelight_nullgr:harira": 3.0,
    "ramadandelight_nullgr:mhalbiya": 3.0,
    "ramadandelight_nullgr:sweet_tagine": 3.0,
    "ramadandelight_nullgr:tagine": 3.0,
    # 数据来源：SlavicDelightNullGr_BP
    "slavic_delight_nullgr:borsch": 4.0,
    "slavic_delight_nullgr:kefir_bottle": 4.0,
    "slavic_delight_nullgr:kvass_bottle": 3.0,
    "slavic_delight_nullgr:okroshka_kefir": 3.0,
    "slavic_delight_nullgr:okroshka_kvass": 3.0,
    "slavic_delight_nullgr:solyanka": 4.0,
    "slavic_delight_nullgr:svekolnik": 4.0,
    # 数据来源：SpanishDelight_BP
    "spanish_delight_nullgr:gazpacho": 4.0,
    # 数据来源：Ube_Delight_BP
    "ube_delight_nullgr:arroz_caldo": 3.0,
    "ube_delight_nullgr:bulalo": 4.0,
    "ube_delight_nullgr:mechado": 3.0,
    "ube_delight_nullgr:milk_tea_ube": 5.0,
    # 数据来源：VanillaDelight_BP
    "vanilladelight_nullgr:cod_stew": 3.0,
    "vanilladelight_nullgr:glow_tropical_fish_stew": 3.0,
    "vanilladelight_nullgr:golden_apple_cider": 3.0,
    # 数据来源：Veggiesdelight_BP
    "dumpling_delight_nullgr:garlic_chicken_stew": 3.0,
    "veggiesdelight_nullgr:cacciatore": 3.0,
    "veggiesdelight_nullgr:carrot_juice": 5.0,
    "veggiesdelight_nullgr:cauliflower_soup": 3.0,
    "veggiesdelight_nullgr:dandelion_juice": 5.0,
    # 数据来源：VietnamDelightNullGr_BP
    "vietnam_delight_nullgr:banana_blossom_sour_soup": 4.0,
    "vietnam_delight_nullgr:lotus_embryo_tea": 5.0,
    "vietnam_delight_nullgr:lotus_rhizome_pork_soup": 4.0,
    "vietnam_delight_nullgr:lotus_rhizome_sweet_soup": 3.0,
    "vietnam_delight_nullgr:lotus_seed_sweet_soup": 3.0,
    "vietnam_delight_nullgr:lotus_stem_chicken_pandan_soup": 4.0,
    "vietnam_delight_nullgr:plum_tea": 5.0,
    "vietnam_delight_nullgr:purple_lotus_flower_tea": 5.0,
    "vietnam_delight_nullgr:white_lotus_flower_tea": 5.0,
    "vietnam_delight_nullgr:yellow_lotus_flower_tea": 5.0,
    # 数据来源：VintageDelight_BP
    "vintage_delight_nullgr:ghostly_chili": 3.0,
    "vintage_delight_nullgr:nut_milk_bottle": 6.0,
    "vintage_delight_nullgr:oatmeal": 3.0,
    "vintage_delight_nullgr:overnight_oats": 3.0,
    "vintage_delight_nullgr:pickle_soup": 4.0,
}

for itemName, defaultValue in foodDrinkDefaultValues.items():
    drinkItemValues[itemName] = {
        "event": playerEatDrinkEvent,
        "defaultValue": defaultValue,
        "auxValues": {}
    }

attrValue = "diet_nullgr_thirst_value"
attrEnabled = "diet_nullgr_thirst_enabled"
syncEvent = "ThirstSyncData"
clientReadyEvent = "ThirstClientReady"
settingEnabledKey = "thirst_enabled"
settingEventUpdate = "DietSettingUpdate"
settingEventSync = "DietSettingSync"

flashInterval = 0.12
flashToggleCount = 6

settingDef = {
    "key": settingEnabledKey,
    "name": "启用口渴值（开启后口渴会持续消耗，低值限制冲刺，耗尽时受伤；关闭后隐藏口渴条并停止这些影响）",
    "control": "toggle",
    "default": True,
    "priority": 15,
    "groupId": ""
}
