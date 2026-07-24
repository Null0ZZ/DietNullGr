# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.Diet as DietCore
import Diet_NullGr.ModSys.Thirst.config as thirstConfig

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


class Thirst(object):
    # 查询服务端口渴真值，外部玩法不需要了解 HUD 的 0 到 20 离散显示格式。
    @staticmethod
    def getValue(playerId):
        serverSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        return serverSys.getThirstValue(playerId)

    # 直接设置口渴真值；系统关闭时接口保持 no-op 并返回原值。
    @staticmethod
    def setValue(playerId, value):
        serverSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        return serverSys.setThirstValue(playerId, value)

    # 增加口渴值并返回裁剪后的真值，适合饮水或恢复类玩法。
    @staticmethod
    def addValue(playerId, amount):
        serverSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        return serverSys.addThirstValue(playerId, amount)

    # 消耗口渴值并返回裁剪后的真值，适合移动、环境或时间衰减玩法。
    @staticmethod
    def consumeValue(playerId, amount):
        serverSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        return serverSys.consumeThirstValue(playerId, amount)

    # 查询通用设置中的口渴系统开关，玩法模块可据此跳过自身衰减计算。
    @staticmethod
    def isEnabled(playerId):
        serverSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        return serverSys.isThirstEnabled(playerId)

