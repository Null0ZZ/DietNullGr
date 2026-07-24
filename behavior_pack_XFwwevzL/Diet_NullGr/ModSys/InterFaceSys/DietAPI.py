# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

interFaceModule = [None]


# 外部模组可能先于 Diet 主系统导入 API，延迟加载真实接口可以避开初始化顺序问题。
def loadInterFaceModule():
    if interFaceModule[0] is None:
        interFaceModule[0] = serverApi.ImportModule("Diet_NullGr.ModSys.InterFaceSys.Intract_InterFace")
    return interFaceModule[0]


class DietProxy(object):
    # 给外部模组注册单个物品的饮食分类，食物组使用 fruits/grains/proteins/vegetables/sugars。
    def registerFood(self, itemName, foodGroupIds):
        return loadInterFaceModule().Diet.registerFood(itemName, foodGroupIds)

    # 移除运行时注册的物品分类，内置食物表和 JSON tag 仍然照常生效。
    def removeFood(self, itemName):
        return loadInterFaceModule().Diet.removeFood(itemName)

    # 给外部模组扩展 tag 到饮食分类的映射，适合一个 tag 批量覆盖一组自定义食物。
    def registerTag(self, tagName, foodGroupIds):
        return loadInterFaceModule().Diet.registerTag(tagName, foodGroupIds)

    # 查询某个物品当前会命中的饮食分类，便于外部模组或测试脚本确认联动结果。
    def getFoodGroups(self, itemName, itemAuxValue=0):
        return loadInterFaceModule().Diet.getFoodGroups(itemName, itemAuxValue)


class ThirstProxy(object):
    # 查询服务端口渴真值。
    def getValue(self, playerId):
        return loadInterFaceModule().Thirst.getValue(playerId)

    # 直接设置口渴真值；系统关闭时返回未修改的原值。
    def setValue(self, playerId, value):
        return loadInterFaceModule().Thirst.setValue(playerId, value)

    # 增加口渴值并返回最新真值。
    def addValue(self, playerId, amount):
        return loadInterFaceModule().Thirst.addValue(playerId, amount)

    # 扣除口渴值并返回最新真值。
    def consumeValue(self, playerId, amount):
        return loadInterFaceModule().Thirst.consumeValue(playerId, amount)

    # 查询通用设置中的口渴系统开关。
    def isEnabled(self, playerId):
        return loadInterFaceModule().Thirst.isEnabled(playerId)


class DietNullGrAPI(object):
    Diet = DietProxy()
    Thirst = ThirstProxy()


Diet = DietNullGrAPI.Diet
Thirst = DietNullGrAPI.Thirst

