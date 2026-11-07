# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Diet.Diet as Diet
import Diet_NullGr.ModSys.Thirst.config as thirstConfig


# 网络和存档共用半百分点整数格式，拒绝布尔值和小数，避免隐式舍入。
def validFoodUnits(values):
    return (isinstance(values, list) and len(values) == len(config.groupOrder) and
            all(type(value) is int and 0 <= value <= config.foodNutritionMaxUnits for value in values))


class FoodNutritionRules(object):
    def __init__(self, extraDataComp, itemComp):
        self.extraDataComp = extraDataComp
        self.itemComp = itemComp
        self.foodIds = None
        self.observedInputs = {}
        self.snapshot = {'version': 1, 'revision': 0, 'rules': {}}
        self.writeEnabled = True
        rawData = extraDataComp.GetExtraData(config.foodNutritionWorldKey)
        if rawData is None:
            return
        if (isinstance(rawData, dict) and rawData.get('version') == 1 and
                type(rawData.get('revision')) is int and rawData['revision'] >= 0 and
                isinstance(rawData.get('rules'), dict) and
                all(validFoodUnits(units) for units in rawData['rules'].values())):
            self.snapshot = rawData
        else:
            self.writeEnabled = False
            print("[DietNullGr] 食物营养存档格式无效，已关闭规则写入")

    # 仅首次浏览目录时扫描注册表，每批让出一帧，全部收集后再发布可写的食物集合。
    def scanFoods(self):
        foodIds = set()
        for index, itemName in enumerate(self.itemComp.GetLoadItems(True)):
            if index and index % config.foodCatalogBatchSize == 0:
                yield
            if ':' not in itemName or itemName in thirstConfig.hydrationOnlyItemNames:
                continue
            if itemName == 'minecraft:milk_bucket':
                foodIds.add(itemName)
                continue
            itemInfo = self.itemComp.GetItemBasicInfo(itemName, 0)
            if itemInfo and (itemInfo['itemType'] == 'food' or itemInfo.get('foodNutrition', 0) > 0):
                foodIds.add(itemName)
        self.foodIds = foodIds

    # 判断清单状态时重新读取自动分类，兼容其他模组在目录建立后注册食物规则。
    def buildCatalog(self):
        entries = []
        for itemName in sorted(self.foodIds):
            if itemName in self.snapshot['rules']:
                status = 'manual'
            else:
                status = 'auto' if Diet.getFoodGroupIds(itemName, 0, self.itemComp) else 'pending'
            entries.append([itemName, status])
        return entries

    # 详情与保存回执使用同一个快照，参考值只来自默认变体的真实进食采样。
    def buildDetail(self, itemName):
        sources = []
        autoGroups = Diet.getFoodGroupIds(itemName, 0, self.itemComp, sources)
        manualUnits = self.snapshot['rules'].get(itemName)
        referenceUnits = None
        if autoGroups and itemName in self.observedInputs:
            hunger, nutrition = self.observedInputs[itemName]
            gains = Diet.calculateGain(hunger, nutrition, autoGroups)
            referenceUnits = [int(round(gains.get(groupId, 0) * 200)) for groupId in config.groupOrder]
        return {
            'itemName': itemName,
            'revision': self.snapshot['revision'],
            'status': 'manual' if manualUnits is not None else ('auto' if autoGroups else 'pending'),
            'manualUnits': manualUnits,
            'autoGroups': autoGroups,
            'autoSources': sources,
            'referenceUnits': referenceUnits
        }

    # 先比对同一物品的旧规则，再保存完整快照；只有落盘成功后进食和目录才看见新规则。
    def writeRule(self, itemName, previousUnits, desiredUnits):
        if not self.writeEnabled:
            return 'storage'
        if ((desiredUnits is not None and not validFoodUnits(desiredUnits)) or
                (previousUnits is not None and not validFoodUnits(previousUnits))):
            return 'invalid'
        rules = self.snapshot['rules']
        currentUnits = rules.get(itemName)
        if currentUnits == desiredUnits:
            return 'same'
        if currentUnits != previousUnits:
            return 'conflict'
        nextRules = rules.copy()
        if desiredUnits is None:
            del nextRules[itemName]
        else:
            nextRules[itemName] = list(desiredUnits)
        nextSnapshot = {'version': 1, 'revision': self.snapshot['revision'] + 1, 'rules': nextRules}
        if not self.extraDataComp.SetExtraData(config.foodNutritionWorldKey, nextSnapshot, False):
            return 'storage'
        if not self.extraDataComp.SaveExtraData():
            # 保存失败后恢复组件缓存，避免下一次世界保存误写入已拒绝的规则。
            if not self.extraDataComp.SetExtraData(config.foodNutritionWorldKey, self.snapshot, False):
                self.writeEnabled = False
                print("[DietNullGr] 食物营养存档回滚失败，已关闭本次会话写入")
            return 'storage'
        self.snapshot = nextSnapshot
        return 'saved'


# 引擎文本可能是 UTF-8 字节串；以 Unicode 字符匹配，跳字时不会拆开汉字。
def foodSearchText(text):
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    return u''.join(text.lower().split())


# 输入与步进按钮共用单位换算；原样保留无效草稿，直到玩家修正。
def parseFoodUnits(text):
    parts = text.strip().split('.', 1)
    whole = parts[0]
    if not whole or len(whole) > 3 or any(character not in '0123456789' for character in whole):
        return None
    fraction = parts[1].rstrip('0') if len(parts) == 2 else ''
    if fraction not in ('', '5'):
        return None
    units = int(whole) * 2 + (1 if fraction else 0)
    return units if units <= config.foodNutritionMaxUnits else None


# 按半百分点整数显示，避免出现浮点误差尾数。
def formatFoodUnits(units):
    return '{}{}'.format(units // 2, '.5' if units % 2 else '')


# 搜索先分档，再维持目录原顺序；分类数量统计全局命中，方便切换命名空间。
def filterFoodCatalog(itemNames, entries, showConfigured, namespace, text):
    keyword = foodSearchText(text)
    counts = {'': 0}
    ranked = [[], [], []]
    for itemName in itemNames:
        entry = entries[itemName]
        if (entry['status'] != 'pending') != showConfigured:
            continue
        itemNamespace = entry['namespace']
        if itemNamespace not in counts:
            counts[itemNamespace] = 0
        name = entry['searchName']
        if not keyword or name == keyword:
            rank = 0
        elif keyword in name:
            rank = 1
        else:
            rank = 2
            offset = 0
            for character in keyword:
                position = name.find(character, offset)
                if position == -1:
                    rank = None
                    break
                offset = position + 1
            if rank is None:
                continue
        counts[itemNamespace] += 1
        counts[''] += 1
        if not namespace or itemNamespace == namespace:
            ranked[rank].append(itemName)
    return ranked[0] + ranked[1] + ranked[2], counts
