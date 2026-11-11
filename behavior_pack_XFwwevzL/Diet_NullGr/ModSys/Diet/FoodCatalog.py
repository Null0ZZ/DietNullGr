# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.ModSys.Diet.FoodNutrition as FoodNutrition
import Diet_NullGr.ModSys.Diet.config as config


class FoodCatalog(object):
    def __init__(self, clientSystem):
        self.clientSystem = clientSystem
        compFactory = clientApi.GetEngineCompFactory()
        levelId = clientApi.GetLevelId()
        self.itemComp = compFactory.CreateItem(levelId)
        self.gameComp = compFactory.CreateGame(levelId)
        self.entries = {}
        self.itemNames = None
        self.representatives = {}
        self.version = None
        self.requestId = None
        self.requestTimer = None
        self.chunks = {}
        self.indexing = None
        self.pendingDetails = []

    # 目录同步与详情编辑各有请求状态，快速开关界面或点进详情都可以继续收包和建索引。
    def Request(self):
        if self.requestId is not None:
            return
        self.clientSystem.foodNutritionRequestId += 1
        self.requestId = self.clientSystem.foodNutritionRequestId
        args = {'requestId': self.requestId}
        if self.version is not None:
            args['catalogVersion'] = self.version
        self.requestTimer = self.gameComp.AddTimer(20.0, self.RequestExpired, self.requestId)
        self.clientSystem.NotifyToServer(config.foodCatalogRequest, args)

    # 一次请求从收分片持续到建索引结束，期间收到的规则回执要合并到完整快照。
    def ReceiveCatalog(self, args):
        if self.requestTimer is None or args['requestId'] != self.requestId:
            return
        canEdit = args['canEdit']
        if args['kind'] == 'catalogCurrent':
            self._finishRequest()
            node = self.clientSystem.foodNutritionNode
            if node is not None:
                node.CatalogUpdated(canEdit, False)
            return
        self.chunks[args['index']] = args['entries']
        if len(self.chunks) != args['total']:
            return
        rows = [row for index in range(args['total']) for row in self.chunks[index]]
        self.chunks.clear()
        self.gameComp.CancelTimer(self.requestTimer)
        self.requestTimer = None
        indexing = clientApi.StartCoroutine(self._indexCatalog(rows, args['catalogVersion'], canEdit))
        if self.requestId is not None:
            self.indexing = indexing

    # 仅对首次出现的物品分帧查询引擎。完整索引合并期间的单项变更后再供新界面复用。
    def _indexCatalog(self, rows, version, canEdit):
        entries = {}
        itemNames = []
        representatives = {}
        lookupCount = 0
        for itemName, status in rows:
            if itemName in self.entries:
                entry = self.entries[itemName].copy()
                namespace = entry['namespace']
            else:
                if lookupCount and lookupCount % config.foodCatalogBatchSize == 0:
                    yield
                lookupCount += 1
                info = self.itemComp.GetItemBasicInfo(itemName, 0)
                label = info['itemName'] if info and info['itemName'] else itemName
                namespace = itemName.split(':', 1)[0]
                entry = {
                    'label': label, 'searchName': FoodNutrition.foodSearchText(label),
                    'namespace': namespace, 'icon': info['id_aux'] if info else 0
                }
            entry['status'] = status
            entry['catalogVersion'] = version
            entries[itemName] = entry
            itemNames.append(itemName)
            if namespace not in representatives:
                representatives[namespace] = itemName

        self.entries = entries
        self.itemNames = itemNames
        self.representatives = representatives
        self.version = version
        for detail, savedChange in self.pendingDetails:
            self._applyDetail(detail, savedChange)
        self.indexing = None
        self._finishRequest()
        node = self.clientSystem.foodNutritionNode
        if node is not None:
            node.CatalogUpdated(canEdit)

    # 收包或建索引期间同步更新已显示的缓存，同时保留变更供新快照发布前重放。
    def ApplyDetail(self, detail, savedChange):
        if self.requestId is not None:
            self.pendingDetails.append((detail, savedChange))
        if self._applyDetail(detail, savedChange):
            node = self.clientSystem.foodNutritionNode
            if node is not None:
                node.CatalogUpdated()

    # 单项状态可以立即更新。只有连续的保存事件才能推进整个目录的版本，缺口由打开时补同步。
    def _applyDetail(self, detail, savedChange):
        entry = self.entries.get(detail['itemName'])
        if entry is None:
            return False
        version = detail['catalogVersion']
        if savedChange and version == self.version + 1:
            self.version = version
        if version < entry['catalogVersion']:
            return False
        filterChanged = (entry['status'] == 'pending') != (detail['status'] == 'pending')
        entry['status'] = detail['status']
        entry['catalogVersion'] = version
        return filterChanged

    # 超时或离开世界时丢弃未完成的分片。请求编号和计时器共同拦截迟到回包。
    def _finishRequest(self):
        if self.requestTimer is not None:
            self.gameComp.CancelTimer(self.requestTimer)
            self.requestTimer = None
        self.requestId = None
        self.chunks.clear()
        self.pendingDetails = []

    # 首次加载超时后可重试，已有的目录可继续浏览并在下次打开时校验。
    def RequestExpired(self, requestId):
        if self.requestTimer is None or requestId != self.requestId:
            return
        self.requestTimer = None
        self._finishRequest()
        node = self.clientSystem.foodNutritionNode
        if node is not None and self.itemNames is None:
            node.CatalogTimedOut()

    def Destroy(self):
        self._finishRequest()
        if self.indexing is not None:
            clientApi.StopCoroutine(self.indexing)
            self.indexing = None
