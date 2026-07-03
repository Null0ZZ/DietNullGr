# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Diet.Diet as Diet

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()
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
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerDieEvent", self, self.PlayerDieEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerRespawnFinishServerEvent", self, self.PlayerRespawnFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "CommandEvent", self, self.CommandEvent)
        self.ListenForEvent(com.modName, com.csname, "DietClientReady", self, self.DietClientReady)
        self.ListenForEvent(com.modName, com.csname, config.settingEventUpdate, self, self.DietSettingUpdate)
        print("[DietNullGr] server ready")

    def AddServerPlayerEvent(self, args):
        playerId = args['id']
        # 本地 MCDK 单机环境不会下发 Apollo 专用字段，本模块只依赖稳定的玩家 id 建立存档缓存。
        self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory, minecraftEnum)

    def ClientLoadAddonsFinishServerEvent(self, args):
        playerId = args['playerId']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory, minecraftEnum)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        Diet.syncSettingToClient(self, playerId, self.playerDietData[playerId])

    def DietClientReady(self, args):
        playerId = args['__id__']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory, minecraftEnum)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        Diet.syncSettingToClient(self, playerId, self.playerDietData[playerId])

    def DietSettingUpdate(self, args):
        playerId = args['__id__']
        settingKey = args['key']
        value = args['value']
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory, minecraftEnum)
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
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory, minecraftEnum)
        data = self.playerDietData[playerId]
        if not data['active']:
            return
        itemName = itemDict['newItemName']
        itemAuxValue = itemDict['newAuxValue']
        compItem = compFactory.CreateItem(serverApi.GetLevelId())
        applied = Diet.applyFoodGain(data, itemName, itemAuxValue, hunger, nutrition, compItem)
        if not applied:
            return
        Diet.savePlayerData(playerId, data, compFactory)
        Diet.syncToClient(self, playerId, data)
        Diet.sendMessage(playerId, compFactory, "均衡饮食: {} 已记录".format(itemName), "§a")

    def PlayerDieEvent(self, args):
        playerId = args['id']
        attacker = args['attacker']
        self.deadPlayers[playerId] = True

    def PlayerRespawnFinishServerEvent(self, args):
        playerId = args['playerId']
        if playerId not in self.deadPlayers:
            return
        if playerId not in self.playerDietData:
            self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory, minecraftEnum)
        # 上游默认死亡惩罚会把所有饮食值按 AMOUNT 方式扣到最低值，这里在复活完成后处理，避免玩家死亡过程中的实体属性不可读。
        Diet.applyDeathPenalty(self.playerDietData[playerId])
        Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
        Diet.syncToClient(self, playerId, self.playerDietData[playerId])
        del self.deadPlayers[playerId]

    def CommandEvent(self, args):
        entityId = args['entityId']
        command = args['command']
        if entityId not in self.playerDietData:
            self.playerDietData[entityId] = Diet.loadPlayerData(entityId, compFactory, minecraftEnum)
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
        for playerId in serverApi.GetPlayerList():
            if playerId not in self.playerDietData:
                self.playerDietData[playerId] = Diet.loadPlayerData(playerId, compFactory, minecraftEnum)
            data = self.playerDietData[playerId]
            attrComp = compFactory.CreateAttr(playerId)
            hunger = attrComp.GetAttrValue(minecraftEnum.AttrType.HUNGER)
            if data['active'] and hunger < data['prevHunger']:
                # Diet 原版只在饥饿条被消耗时衰减，本地记录上一帧饥饿值来复刻这一链路。
                Diet.applyHungerDecay(data, data['prevHunger'] - hunger)
                Diet.savePlayerData(playerId, data, compFactory)
                Diet.syncToClient(self, playerId, data)
            data['prevHunger'] = hunger
            if data['active'] and self.tickCounter % config.effectRefreshTick == 0:
                Diet.applyEffects(playerId, data, compFactory)

    def Destroy(self):
        for playerId in self.playerDietData:
            Diet.savePlayerData(playerId, self.playerDietData[playerId], compFactory)
