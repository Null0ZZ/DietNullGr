# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.ModSys.Diet.Diet as DietCore

compFactory = serverApi.GetEngineCompFactory()


class Diet(object):
    # 给外部模组注册单个物品的饮食分类，食物组使用 fruits/grains/proteins/vegetables/sugars。
    @staticmethod
    def registerFood(itemName, foodGroupIds):
        return DietCore.registerFoodGroups(itemName, foodGroupIds)

    # 移除运行时注册的物品分类，内置食物表和 JSON tag 仍然照常生效。
    @staticmethod
    def removeFood(itemName):
        return DietCore.removeRegisteredFood(itemName)

    # 给外部模组扩展 tag 到饮食分类的映射，适合一个 tag 批量覆盖一组自定义食物。
    @staticmethod
    def registerTag(tagName, foodGroupIds):
        return DietCore.registerDietTag(tagName, foodGroupIds)

    # 查询某个物品当前会命中的饮食分类，便于外部模组或测试脚本确认联动结果。
    @staticmethod
    def getFoodGroups(itemName, itemAuxValue=0):
        compItem = compFactory.CreateItem(serverApi.GetLevelId())
        return DietCore.getFoodGroupIds(itemName, itemAuxValue, compItem)

