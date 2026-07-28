# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Disease.config as diseaseConfig
import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Diet.Diet as Diet
import Diet_NullGr.ModSys.Thirst.config as thirstConfig

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
engineNamespace = serverApi.GetEngineNamespace()
engineSystemName = serverApi.GetEngineSystemName()


class DietServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.playerDietData = {}
        self.deadPlayers = {}
        self.tickCounter = 0
        self.ListenForEvent(engineNamespace, engineSystemName, "AddServerPlayerEvent", self, self.AddServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ClientLoadAddonsFinishServerEvent", self, self.ClientLoadAddonsFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "DelServerPlayerEvent", self, self.DelServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerEatFoodServerEvent", self, self.PlayerEatFoodServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerHungerChangeServerEvent", self, self.PlayerHungerChangeServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerDieEvent", self, self.PlayerDieEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerRespawnFinishServerEvent", self, self.PlayerRespawnFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "CommandEvent", self, self.CommandEvent)
        # 奖励和低值惩罚依赖 Tick 周期刷新，必须显式监听引擎事件，否则只会停留在普通方法定义。
        self.ListenForEvent(engineNamespace, engineSystemName, "OnScriptTickServer", self, self.OnScriptTickServer)
        self.ListenForEvent(com.modName, com.csname, "DietClientReady", self, self.DietClientReady)
        self.ListenForEvent(com.modName, com.csname, config.settingEventUpdate, self, self.DietSettingUpdate)
        print("[DietNullGr] server ready")

    def AddServerPlayerEvent(self, args):
        playerId = args['id']
        # 本地 MCDK 单机环境不会下发 Apollo 专用字段，本模块只依赖稳定的玩家 id 建立存档缓存。
        self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)

    def ClientLoadAddonsFinishServerEvent(self, args):
        playerId = args['playerId']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        Diet.syncSettingToClient(self, playerId, self.playerDietData[playerId])

    def DietClientReady(self, args):
        playerId = args['__id__']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        Diet.syncSettingToClient(self, playerId, self.playerDietData[playerId])

    def DietSettingUpdate(self, args):
        playerId = args['__id__']
        settingKey = args['key']
        value = args['value']
        # 口渴设置与均衡饮食共用客户端设置事件，但由独立服务端系统持久化，旧服务不重复解释这些 key。
        if settingKey in thirstConfig.settingKeys:
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
            Diet.sendMessage(playerId, compFactory, settingResult['message'], settingResult['color'])

    def DelServerPlayerEvent(self, args):
        playerId = args['id']
        # 退出时同样只依赖玩家 id 写回 ModAttr，Apollo 转服字段不参与本模块状态链路。
        if playerId in self.playerDietData:
            Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
            del self.playerDietData[playerId]
        if playerId in self.deadPlayers:
            del self.deadPlayers[playerId]

    def PlayerEatFoodServerEvent(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict']
        hunger = args['hunger']
        nutrition = args['nutrition']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
        data = self.playerDietData[playerId]
        gainValues = {}
        if data['active']:
            itemName = itemDict['newItemName']
            itemAuxValue = itemDict['newAuxValue']
            compItem = compFactory.CreateItem(serverApi.GetLevelId())
            gainValues = Diet.applyFoodGain(data, itemName, itemAuxValue, hunger, nutrition, compItem)
        # 真实进食总要结算患病症状；只有取得营养增益时才增加有效进食次数并推进恢复。
        diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
        diseaseSys.recordFoodEat(playerId, data, gainValues)
        if not gainValues:
            return
        Diet.savePlayerData(playerId, data, compFactory)
        Diet.syncToClient(self, playerId, data)
        # 进食提示在保存后基于最新数值生成：先告知本次补充，再对其他低值营养给出补充建议。
        foodGainMessages = Diet.buildFoodGainMessages(data, gainValues)
        Diet.sendMessage(playerId, compFactory, foodGainMessages['gainMessage'], "§a")
        if foodGainMessages['warningMessage']:
            Diet.sendMessage(playerId, compFactory, foodGainMessages['warningMessage'], "§e")

    def PlayerHungerChangeServerEvent(self, args):
        playerId = args['playerId']
        hungerBefore = args['hungerBefore']
        hunger = args['hunger']
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
        for message in nutritionAlertMessages:
            Diet.sendMessage(playerId, compFactory, message, "§e")
        if nutritionAlertMessages:
            self.NotifyToClient(playerId, config.lowNutritionAlertEvent, {
                'sound': config.lowNutritionAlertSound,
                'volume': config.lowNutritionAlertVolume,
                'pitch': config.lowNutritionAlertPitch
            })

    def PlayerDieEvent(self, args):
        playerId = args['id']
        attacker = args['attacker']
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

    def CommandEvent(self, args):
        entityId = args['entityId']
        command = args['command']
        diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
        if diseaseSys.handleCommand(entityId, command):
            args['cancel'] = True
            return
        if entityId not in self.playerDietData:
            self.playerDietData[entityId] = Diet.loadPlayerData(entityId, compFactory)
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
            Diet.sendMessage(entityId, compFactory, commandResult['message'], commandResult['color'])

    def OnScriptTickServer(self):
        self.tickCounter += 1
        if self.tickCounter % config.effectRefreshTick != 0:
            return
        for playerId in serverApi.GetPlayerList():
            if playerId not in self.playerDietData:
                self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory)
            data = self.playerDietData[playerId]
            if data['active']:
                diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
                Diet.applyEffects(
                    playerId,
                    data,
                    compFactory,
                    diseaseSys.hasActiveDisease(playerId),
                    diseaseSys.isSugarRushPaused(playerId)
                )

    def Destroy(self):
        for playerId in self.playerDietData:
            Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
