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


class DietNullGrAPI(object):
    Diet = DietProxy()


Diet = DietNullGrAPI.Diet

