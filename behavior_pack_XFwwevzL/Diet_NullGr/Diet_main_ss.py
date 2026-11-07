# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Disease.config as diseaseConfig
import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Diet.Diet as Diet
import Diet_NullGr.ModSys.Diet.FoodNutrition as FoodNutrition
import Diet_NullGr.ModSys.Thirst.config as thirstConfig
import Diet_NullGr.ModSys.TipMessage.config as tipMessageConfig

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
compGame = compFactory.CreateGame(levelId)
gameTypeEnum = serverApi.GetMinecraftEnum().GameType
engineNamespace = serverApi.GetEngineNamespace()
engineSystemName = serverApi.GetEngineSystemName()


# 目录权限与写入复核使用同一判定，以引擎提供的房主和在线玩家权限为准。
def canEditFoodNutrition(playerId):
    if playerId == serverApi.GetHostPlayerId():
        return True
    abilities = compFactory.CreatePlayer(playerId).GetPlayerAbilities()
    return bool(abilities and abilities['op'])


class DietServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.playerDietData = {}
        self.deadPlayers = {}
        self.tickCounter = 0
        self.foodNutrition = FoodNutrition.FoodNutritionRules(
            compFactory.CreateExtraData(levelId), compFactory.CreateItem(levelId)
        )
        self.foodCatalogScan = None
        self.foodCatalogWaiters = {}
        self.ListenForEvent(engineNamespace, engineSystemName, "AddServerPlayerEvent", self, self.AddServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ClientLoadAddonsFinishServerEvent", self, self.ClientLoadAddonsFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "DelServerPlayerEvent", self, self.DelServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerEatFoodServerEvent", self, self.PlayerEatFoodServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerHungerChangeServerEvent", self, self.PlayerHungerChangeServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerDieEvent", self, self.PlayerDieEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerRespawnFinishServerEvent", self, self.PlayerRespawnFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "GameTypeChangedServerEvent", self, self.GameTypeChangedServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "CommandEvent", self, self.CommandEvent)
        # 奖励和低值惩罚依赖 Tick 周期刷新，必须显式监听引擎事件，否则只会停留在普通方法定义。
        self.ListenForEvent(engineNamespace, engineSystemName, "OnScriptTickServer", self, self.OnScriptTickServer)
        self.ListenForEvent(com.modName, com.csname, "DietClientReady", self, self.DietClientReady)
        self.ListenForEvent(com.modName, com.csname, config.settingEventUpdate, self, self.DietSettingUpdate)
        self.ListenForEvent(com.modName, com.csname, config.foodCatalogRequest, self, self.FoodCatalogRequest)
        self.ListenForEvent(com.modName, com.csname, config.foodDetailRequest, self, self.FoodDetailRequest)
        self.ListenForEvent(com.modName, com.csname, config.foodRuleRequest, self, self.FoodRuleRequest)
        print("[DietNullGr] server ready")

    def AddServerPlayerEvent(self, args):
        playerId = args['id']
        # 本地 MCDK 单机环境不会下发 Apollo 专用字段，本模块只依赖稳定的玩家 id 建立存档缓存。
        self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)

    def ClientLoadAddonsFinishServerEvent(self, args):
        playerId = args['playerId']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
            self._suspendPlayerRuntime(playerId)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        Diet.syncSettingToClient(self, playerId, self.playerDietData[playerId])

    def DietClientReady(self, args):
        playerId = args['__id__']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
            self._suspendPlayerRuntime(playerId)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        Diet.syncSettingToClient(self, playerId, self.playerDietData[playerId])

    def DietSettingUpdate(self, args):
        playerId = args['__id__']
        settingKey = args['key']
        value = args['value']
        # 口渴和疾病设置共用客户端设置事件，但分别由独立服务端系统持久化，主系统不重复解释这些 key。
        if settingKey in thirstConfig.settingKeys or settingKey in diseaseConfig.settingKeys:
            return
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        # 通用设置开关先落服务端存档，再同步面板和设置控件，避免客户端本地状态先行造成计算分叉。
        settingResult = Diet.applySetting(self.playerDietData[playerId], settingKey, value)
        if settingResult['changed']:
            Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
            Diet.syncToClient(self, playerId, self.playerDietData[playerId])
            Diet.syncSettingToClient(self, playerId, self.playerDietData[playerId])
        if settingResult['message']:
            self._queueTipMessage(
                playerId,
                tipMessageConfig.dietSettingKey,
                settingResult['color'] + settingResult['message'],
                tipMessageConfig.priorityNormal
            )

    def DelServerPlayerEvent(self, args):
        playerId = args['id']
        self.foodCatalogWaiters.pop(playerId, None)
        # 退出时同样只依赖玩家 id 写回 ModAttr，Apollo 转服字段不参与本模块状态链路。
        if playerId in self.playerDietData:
            Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
            del self.playerDietData[playerId]
        if playerId in self.deadPlayers:
            del self.deadPlayers[playerId]

    def FoodCatalogRequest(self, args):
        playerId = args['__id__']
        if 'requestId' not in args or type(args['requestId']) is not int:
            return
        requestId = args['requestId']
        if self.foodNutrition.foodIds is not None:
            self._sendFoodCatalog(playerId, requestId, self.foodNutrition.buildCatalog())
            return
        # 首次打开者共享同一次分帧扫描，同一客户端只保留最新请求。
        self.foodCatalogWaiters[playerId] = requestId
        if self.foodCatalogScan is None:
            self.foodCatalogScan = serverApi.StartCoroutine(self.foodNutrition.scanFoods(), self.FoodCatalogReady)

    # 扫描完成后才回包，退出世界的客户端已从等待表移除。
    def FoodCatalogReady(self):
        self.foodCatalogScan = None
        waiters = self.foodCatalogWaiters
        self.foodCatalogWaiters = {}
        entries = self.foodNutrition.buildCatalog()
        for playerId, requestId in waiters.items():
            self._sendFoodCatalog(playerId, requestId, entries)

    # 同一请求的分片使用一个修订号，避免大量物品一次发送挤满事件包。
    def _sendFoodCatalog(self, playerId, requestId, entries):
        chunkSize = config.foodCatalogChunkSize
        totalChunks = max(1, (len(entries) + chunkSize - 1) // chunkSize)
        canEdit = canEditFoodNutrition(playerId)
        revision = self.foodNutrition.snapshot['revision']
        for index in range(totalChunks):
            self.NotifyToClient(playerId, config.foodNutritionResponse, {
                'kind': 'catalog', 'requestId': requestId, 'canEdit': canEdit, 'revision': revision,
                'index': index, 'total': totalChunks, 'entries': entries[index * chunkSize:(index + 1) * chunkSize]
            })

    def FoodDetailRequest(self, args):
        playerId = args['__id__']
        if 'requestId' not in args or 'itemName' not in args or type(args['requestId']) is not int:
            return
        requestId = args['requestId']
        itemName = args['itemName']
        detail = None
        if isinstance(itemName, (str, type(u''))) and itemName in self.foodNutrition.foodTagsById:
            detail = self.foodNutrition.buildDetail(itemName)
        self.NotifyToClient(playerId, config.foodNutritionResponse, {
            'kind': 'detail', 'requestId': requestId, 'canEdit': canEditFoodNutrition(playerId), 'detail': detail
        })

    def FoodRuleRequest(self, args):
        playerId = args['__id__']
        if ('requestId' not in args or type(args['requestId']) is not int or
                any(key not in args for key in ('itemName', 'previousUnits', 'desiredUnits'))):
            return
        requestId = args['requestId']
        itemName = args['itemName']
        previousUnits = args['previousUnits']
        desiredUnits = args['desiredUnits']
        canEdit = canEditFoodNutrition(playerId)
        detail = None
        code = 'invalid'
        if isinstance(itemName, (str, type(u''))) and itemName in self.foodNutrition.foodTagsById:
            code = self.foodNutrition.writeRule(itemName, previousUnits, desiredUnits) if canEdit else 'permission'
            detail = self.foodNutrition.buildDetail(itemName)
        # 模型已完成权限后的校验和落盘，回执与变更事件只传播当前生效快照。
        self.NotifyToClient(playerId, config.foodNutritionResponse, {
            'kind': 'write', 'requestId': requestId, 'canEdit': canEdit, 'code': code, 'detail': detail
        })
        if code == 'saved':
            for otherPlayerId in serverApi.GetPlayerList():
                if otherPlayerId != playerId:
                    self.NotifyToClient(otherPlayerId, config.foodNutritionResponse, {'kind': 'changed', 'detail': detail})

    def PlayerEatFoodServerEvent(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict']
        hunger = args['hunger']
        nutrition = args['nutrition']
        itemName = itemDict['newItemName']
        itemAuxValue = itemDict['newAuxValue']
        # 装水木杯借用 food 组件提供完整饮用时序，补水由 Thirst 系统结算，不进入营养和疾病进食链路。
        if itemName in thirstConfig.hydrationOnlyItemNames:
            return
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
            return
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        data = self.playerDietData[playerId]
        gainValues = {}
        beforeValues = None
        if data['active']:
            manualUnits = self.foodNutrition.snapshot['rules'].get(itemName)
            # 手动提示需要区分计划增量与封顶后实际到账的增量，疾病仍使用原结算结果。
            if manualUnits is not None:
                beforeValues = data['values'].copy()
            gainValues = Diet.applyFoodGain(data, itemName, itemAuxValue, hunger, nutrition,
                                           self.foodNutrition.itemComp, manualUnits)
        # 真实进食总要结算患病症状；只有取得营养增益时才增加有效进食次数并推进恢复。
        diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
        diseaseSys.recordFoodEat(playerId, data, gainValues)
        if not gainValues:
            return
        Diet.savePlayerData(playerId, data, compFactory)
        Diet.syncToClient(self, playerId, data)
        # 进食提示在保存后基于最新数值生成：先告知本次补充，再对其他低值营养给出补充建议。
        foodGainMessages = Diet.buildFoodGainMessages(data, gainValues, beforeValues)
        gainMessage = foodGainMessages['gainMessage']
        if gainMessage:
            # 原生提示会解析单个百分号，手动增量的单位需要转义后才能显示。
            if beforeValues is not None:
                gainMessage = gainMessage.replace('%', '%%')
            self._queueTipMessage(
                playerId,
                tipMessageConfig.dietFoodGainKey,
                "§a" + gainMessage,
                tipMessageConfig.priorityNormal
            )
        if foodGainMessages['warningMessage']:
            self._queueTipMessage(
                playerId,
                tipMessageConfig.dietFoodWarningKey,
                "§e" + foodGainMessages['warningMessage'],
                tipMessageConfig.priorityWarning
            )

    def PlayerHungerChangeServerEvent(self, args):
        playerId = args['playerId']
        hungerBefore = args['hungerBefore']
        hunger = args['hunger']
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
            return
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        data = self.playerDietData[playerId]
        if not data['active'] or hunger >= hungerBefore:
            return
        # 网易引擎已提供饥饿值变化事件，这里只在真实下降事件里执行 Diet 原版衰减，避免每 tick 轮询属性。
        beforeValues = Diet.copyDietValues(data)
        metabolicPoints = hungerBefore - hunger
        changed = Diet.applyHungerDecay(data, metabolicPoints)
        # 即使营养值已经为零无法继续衰减，真实饥饿下降仍要推进疾病代谢点。
        diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
        diseaseSys.queueMetabolism(playerId, metabolicPoints)
        if not changed:
            return
        nutritionAlertMessages = Diet.buildNutritionAlertMessages(beforeValues, data)
        Diet.savePlayerData(playerId, data, compFactory)
        Diet.syncToClient(self, playerId, data)
        if nutritionAlertMessages:
            self._queueTipMessage(
                playerId,
                tipMessageConfig.dietNutritionAlertKey,
                "§e" + "\n".join(nutritionAlertMessages),
                tipMessageConfig.priorityWarning
            )
            self.NotifyToClient(playerId, config.lowNutritionAlertEvent, {
                'sound': config.lowNutritionAlertSound,
                'volume': config.lowNutritionAlertVolume,
                'pitch': config.lowNutritionAlertPitch
            })

    def PlayerDieEvent(self, args):
        playerId = args['id']
        attacker = args['attacker']
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
            return
        if playerId in self.deadPlayers:
            return
        self.deadPlayers[playerId] = True
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        # 死亡惩罚必须在死亡事件里立即落盘；玩家复活前退出或停服时，退出保存不会覆盖回未扣除的数据。
        Diet.applyDeathPenalty(self.playerDietData[playerId])
        Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])

    def PlayerRespawnFinishServerEvent(self, args):
        playerId = args['playerId']
        if playerId not in self.deadPlayers:
            return
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        # 死亡事件已经完成扣除和保存；复活完成只负责刷新客户端并清理死亡事务标记。
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        del self.deadPlayers[playerId]

    def GameTypeChangedServerEvent(self, args):
        playerId = args['playerId']
        oldGameType = args['oldGameType']
        newGameType = args['newGameType']
        playerIds = [playerId] if playerId else serverApi.GetPlayerList()
        for currentPlayerId in playerIds:
            gameType = newGameType if playerId else compGame.GetPlayerGameType(currentPlayerId)
            if (gameType == gameTypeEnum.Spectator or
                    (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
                # 模式切换只撤销本模组运行时效果，营养存档保持冻结，返回生存后继续使用原值。
                self._suspendPlayerRuntime(currentPlayerId)

    def CommandEvent(self, args):
        entityId = args['entityId']
        command = args['command']
        if entityId not in self.playerDietData:
            self.playerDietData[entityId] = Diet.loadPlayerData(entityId, compFactory)
        diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
        if diseaseSys.handleCommand(entityId, command):
            args['cancel'] = True
            return
        commandResult = Diet.handleCommand(command, self.playerDietData[entityId])
        if not commandResult['handled']:
            return
        args['cancel'] = True
        if commandResult['changed']:
            Diet.savePlayerData(entityId, self.playerDietData[entityId], compFactory)
            Diet.syncToClient(self, entityId, self.playerDietData[entityId])
            Diet.syncSettingToClient(self, entityId, self.playerDietData[entityId])
        if commandResult['openUi']:
            Diet.syncToClient(self, entityId, self.playerDietData[entityId])
            Diet.syncSettingToClient(self, entityId, self.playerDietData[entityId])
            self.NotifyToClient(entityId, "OpenDietScreen", {})
        if commandResult['message']:
            self._queueTipMessage(
                entityId,
                tipMessageConfig.dietCommandKey,
                commandResult['color'] + commandResult['message'],
                tipMessageConfig.priorityImportant
            )

    def OnScriptTickServer(self):
        self.tickCounter += 1
        if self.tickCounter % config.effectRefreshTick != 0:
            return
        for playerId in serverApi.GetPlayerList():
            if playerId not in self.playerDietData:
                self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
            data = self.playerDietData[playerId]
            gameType = compGame.GetPlayerGameType(playerId)
            if (gameType == gameTypeEnum.Spectator or
                    (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
                continue
            if data['active']:
                diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
                matchedResults = Diet.applyEffects(
                    playerId,
                    data,
                    compFactory,
                    diseaseSys.hasActiveDisease(playerId),
                    diseaseSys.isSugarRushPaused(playerId)
                )
                # 提示必须与本轮实际施加结果保持一致；疾病接管低值惩罚时，返回结果中不会包含普通惩罚。
                lowPenaltyMessage = Diet.buildLowPenaltyEffectMessage(data, matchedResults)
                if lowPenaltyMessage:
                    self._queueTipMessage(
                        playerId,
                        tipMessageConfig.dietLowPenaltyKey,
                        "§c" + lowPenaltyMessage,
                        tipMessageConfig.priorityWarning
                    )

    # 登录和模式切换共用此事务，撤销全部饮食效果及尚未展示的饮食提示，但不修改营养存档。
    def _suspendPlayerRuntime(self, playerId):
        compEffect = compFactory.CreateEffect(playerId)
        removedEffectNames = {}
        for effectId in config.effectOrder:
            for statusEffect in config.dietEffects[effectId]['statusEffects']:
                effectName = statusEffect['name']
                if effectName not in removedEffectNames:
                    compEffect.RemoveEffectFromEntity(effectName)
                    removedEffectNames[effectName] = True
        for penaltyId in config.penaltyOrder:
            for statusEffect in config.dietPenalties[penaltyId]['statusEffects']:
                effectName = statusEffect['name']
                if effectName not in removedEffectNames:
                    compEffect.RemoveEffectFromEntity(effectName)
                    removedEffectNames[effectName] = True
        tipMessageSys = serverApi.GetSystem(com.modName, tipMessageConfig.ssname)
        for messageKey in (
                tipMessageConfig.dietFoodGainKey,
                tipMessageConfig.dietFoodWarningKey,
                tipMessageConfig.dietNutritionAlertKey,
                tipMessageConfig.dietLowPenaltyKey):
            tipMessageSys.removeTip(playerId, messageKey)

    # 多个服务端回调共享同一提示服务，冻结模式不再提交 Diet 消息。
    def _queueTipMessage(self, playerId, messageKey, message, priority):
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not config.creativeModeAffected)):
            return
        tipMessageSys = serverApi.GetSystem(com.modName, tipMessageConfig.ssname)
        tipMessageSys.enqueueTip(playerId, messageKey, message, priority)

    def Destroy(self):
        if self.foodCatalogScan is not None:
            serverApi.StopCoroutine(self.foodCatalogScan)
        self.foodCatalogWaiters.clear()
        for playerId in self.playerDietData:
            Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
