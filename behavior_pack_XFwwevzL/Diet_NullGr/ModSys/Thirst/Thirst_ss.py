# -*- coding: utf-8 -*-

import math
import mod.server.extraServerApi as serverApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Disease.config as diseaseConfig
import Diet_NullGr.ModSys.Diet.config as dietConfig
import Diet_NullGr.ModSys.Thirst.config as config
import Diet_NullGr.ModSys.Thirst.Thirst as Thirst

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
compGame = compFactory.CreateGame(serverApi.GetLevelId())
gameTypeEnum = serverApi.GetMinecraftEnum().GameType
gameDifficultyEnum = serverApi.GetMinecraftEnum().GameDiffculty
actorDamageCause = serverApi.GetMinecraftEnum().ActorDamageCause
attrType = serverApi.GetMinecraftEnum().AttrType
playerActionType = serverApi.GetMinecraftEnum().PlayerActionType
attributeModifierOperation = serverApi.GetMinecraftEnum().AttributeModifierOperation
attributeOperands = serverApi.GetMinecraftEnum().AttributeOperands
engineNamespace = serverApi.GetEngineNamespace()
engineSystemName = serverApi.GetEngineSystemName()


class ServerSys(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.playerThirstData = {}
        self.tickCounter = 0
        self.ListenForEvent(engineNamespace, engineSystemName, "AddServerPlayerEvent", self, self.AddServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ClientLoadAddonsFinishServerEvent", self, self.ClientLoadAddonsFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "DelServerPlayerEvent", self, self.DelServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ActorUseItemServerEvent", self, self.ActorUseItemServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerEatFoodServerEvent", self, self.PlayerEatFoodServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ServerItemTryUseEvent", self, self.ServerItemTryUseEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerHungerChangeServerEvent", self, self.PlayerHungerChangeServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerRespawnFinishServerEvent", self, self.PlayerRespawnFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnPlayerActionServerEvent", self, self.OnPlayerActionServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "DimensionChangeServerEvent", self, self.DimensionChangeServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "GameTypeChangedServerEvent", self, self.GameTypeChangedServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnScriptTickServer", self, self.OnScriptTickServer)
        self.ListenForEvent(com.modName, config.csname, config.clientReadyEvent, self, self.ThirstClientReady)
        self.ListenForEvent(com.modName, com.csname, config.settingEventUpdate, self, self.DietSettingUpdate)
        print("[DietNullGr] thirst server ready")

    def AddServerPlayerEvent(self, args):
        playerId = args['id']
        # 单机 MCDK 不下发 Apollo 扩展字段，本模块只绑定所有运行环境都提供的玩家 ID。
        self.playerThirstData[playerId] = Thirst.loadPlayerData(playerId, compFactory)

    def ClientLoadAddonsFinishServerEvent(self, args):
        playerId = args['playerId']
        data = self._getPlayerData(playerId)
        data['sprinting'] = False
        # AddServerPlayerEvent 触发时实体尚未加载完成，必须等客户端加载完成后再清理固定 ID 的残留修饰符。
        self._updateSprintSpeedModifier(playerId, data)
        Thirst.syncToClient(self, playerId, data)
        Thirst.syncSettingToClient(self, playerId, data)

    def ThirstClientReady(self, args):
        playerId = args['__id__']
        data = self._getPlayerData(playerId)
        Thirst.syncToClient(self, playerId, data)
        Thirst.syncSettingToClient(self, playerId, data)

    def DietSettingUpdate(self, args):
        playerId = args['__id__']
        settingKey = args['key']
        value = args['value']
        if settingKey == config.settingEnabledKey:
            # 通用设置回调属于客户端输入边界，兼容引擎可能回传的布尔值、数字或字符串形式。
            enabled = not (value == False or value == 0 or value == "False" or value == "false" or value == "0")
            self.setThirstEnabled(playerId, enabled)
            return
        if settingKey != config.settingStyleKey or value not in config.styleOptions:
            return
        data = self._getPlayerData(playerId)
        if value == data['style']:
            return
        data['style'] = value
        # 样式只改变客户端表现，但仍由服务端落盘并回推 HUD 与设置控件，保证重进世界后选择不丢失。
        self._saveAndSync(playerId, True, True)

    def DelServerPlayerEvent(self, args):
        playerId = args['id']
        # 离开事件同样只依赖稳定的玩家 ID，避免读取单机不存在的转服字段。
        if playerId not in self.playerThirstData:
            return
        data = self.playerThirstData[playerId]
        data['sprinting'] = False
        data['sprintLimited'] = False
        data['sprintLimitSources'] = {}
        # DelServerPlayerEvent 触发前实体已被引擎移除，运行时修饰符随实体销毁；这里只回收在线状态并保存口渴数据。
        Thirst.savePlayerData(playerId, data, compFactory)
        del self.playerThirstData[playerId]

    def ServerItemTryUseEvent(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict']
        cancel = args['cancel']
        if itemDict['newItemName'] != config.woodenCupItemName:
            return

        playerPos = compFactory.CreatePos(playerId).GetPos()
        playerRot = compFactory.CreateRot(playerId).GetRot()
        rayDirection = serverApi.GetDirFromRot(playerRot)
        dimensionId = compFactory.CreateDimension(playerId).GetEntityDimensionId()
        blockInfoComp = compFactory.CreateBlockInfo(serverApi.GetLevelId())
        waterFound = False
        rayStepCount = int(config.waterFillReach / config.waterFillStep)
        for stepIndex in range(rayStepCount + 1):
            distance = stepIndex * config.waterFillStep
            blockPos = (
                int(math.floor(playerPos[0] + rayDirection[0] * distance)),
                int(math.floor(playerPos[1] + rayDirection[1] * distance)),
                int(math.floor(playerPos[2] + rayDirection[2] * distance))
            )
            blockName = blockInfoComp.GetBlockNew(blockPos, dimensionId)['name']
            if blockName == 'minecraft:air':
                continue
            waterFound = blockName in config.waterBlockNames
            break
        if not waterFound:
            return

        itemComp = compFactory.CreateItem(playerId)
        selectedSlot = itemComp.GetSelectSlotId()
        waterCupItemDict = {
            'newItemName': config.woodenWaterCupItemName,
            'newAuxValue': 0,
            'count': 1
        }
        if itemDict['count'] == 1:
            itemComp.SpawnItemToPlayerInv(waterCupItemDict, playerId, selectedSlot)
            return

        # 堆叠空杯必须先扣除一个再放入成品；背包无法接收时恢复原数量，保证装水事务不吞杯。
        if not itemComp.SetInvItemNum(selectedSlot, itemDict['count'] - 1):
            return
        if not itemComp.SpawnItemToPlayerInv(waterCupItemDict, playerId):
            itemComp.SetInvItemNum(selectedSlot, itemDict['count'])

    def ActorUseItemServerEvent(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict']
        stackSize = args['stackSize']
        itemName = args['itemName']
        itemAuxValue = args['auxValue']
        useMethod = args['useMethod']
        if itemName not in config.drinkItemValues:
            return
        drinkData = config.drinkItemValues[itemName]
        if drinkData['event'] != config.actorUseDrinkEvent:
            return
        # 该事件只在物品完整使用后触发，饮用中断不会结算补水，也不需要依赖背包变化反推结果。
        self.addThirstValue(playerId, Thirst.getDrinkItemValue(itemName, itemAuxValue))

    def PlayerEatFoodServerEvent(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict']
        hunger = args['hunger']
        nutrition = args['nutrition']
        itemName = itemDict['newItemName']
        itemAuxValue = itemDict['newAuxValue']
        if itemName not in config.drinkItemValues:
            return
        drinkData = config.drinkItemValues[itemName]
        if drinkData['event'] != config.playerEatDrinkEvent:
            return
        # 当前网易运行时会在牛奶完整饮用后抛出进食事件，与 Diet 营养结算共用同一个完成时机。
        self.addThirstValue(playerId, Thirst.getDrinkItemValue(itemName, itemAuxValue))

    def PlayerHungerChangeServerEvent(self, args):
        playerId = args['playerId']
        hungerBefore = args['hungerBefore']
        hunger = args['hunger']
        if hunger >= hungerBefore:
            return
        # 原版饥饿下降是当前接口能稳定提供的活动量代理；扣减先进入内存，统一等待周期保存。
        self._consumeAutomatically(playerId, (hungerBefore - hunger) * config.hungerDecayFactor)

    def OnPlayerActionServerEvent(self, args):
        playerId = args['playerId']
        actionType = args['actionType']
        if actionType == playerActionType.StartSprinting:
            sprinting = True
        elif actionType == playerActionType.StopSprinting:
            sprinting = False
        else:
            return
        data = self._getPlayerData(playerId)
        data['sprinting'] = sprinting
        # 疾跑动作状态与每秒刷新的口渴限制资格共同决定逆修饰符，任一状态变化都必须立即汇合。
        self._updateSprintSpeedModifier(playerId, data)

    def DimensionChangeServerEvent(self, args):
        playerId = args['playerId']
        fromDimensionId = args['fromDimensionId']
        toDimensionId = args['toDimensionId']
        fromX = args['fromX']
        fromY = args['fromY']
        fromZ = args['fromZ']
        toX = args['toX']
        toY = args['toY']
        toZ = args['toZ']
        data = self._getPlayerData(playerId)
        data['sprinting'] = False
        # 换维度会重建移动状态，主动撤销旧维度的逆修饰符，等待新的疾跑动作重新添加。
        self._updateSprintSpeedModifier(playerId, data)

    def GameTypeChangedServerEvent(self, args):
        playerId = args['playerId']
        oldGameType = args['oldGameType']
        newGameType = args['newGameType']
        playerIds = [playerId] if playerId else serverApi.GetPlayerList()
        for currentPlayerId in playerIds:
            gameType = newGameType if playerId else compGame.GetPlayerGameType(currentPlayerId)
            if (gameType != gameTypeEnum.Spectator and
                    (gameType != gameTypeEnum.Creative or dietConfig.creativeModeAffected)):
                continue
            data = self._getPlayerData(currentPlayerId)
            data['sprinting'] = False
            data['sprintLimited'] = False
            data['dehydrationTicks'] = 0
            # 模式冻结时立即撤销疾跑限制，口渴真值和疾病来源均原样保留。
            self._updateSprintSpeedModifier(currentPlayerId, data)

    def PlayerRespawnFinishServerEvent(self, args):
        playerId = args['playerId']
        data = self._getPlayerData(playerId)
        data['sprinting'] = False
        data['sprintLimited'] = False
        # 复活可能更换玩家实体，必须在口渴值早退判断前清理死亡前的疾跑事务。
        self._updateSprintSpeedModifier(playerId, data)
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        if not data['enabled'] or data['value'] == config.respawnValue:
            return
        oldDisplayValue = Thirst.getDisplayValue(data['value'])
        data['value'] = Thirst.clampThirstValue(config.respawnValue)
        data['dehydrationTicks'] = 0
        # 复活重置必须立即落盘，避免玩家在下一次批量保存前退出后又恢复为死亡前的低口渴值。
        self._saveAndSync(playerId, Thirst.getDisplayValue(data['value']) != oldDisplayValue, False)

    def OnScriptTickServer(self):
        self.tickCounter += 1
        if self.tickCounter % config.baseDecayIntervalTick == 0:
            baseDecay = config.baseDecayPerSecond * config.baseDecayIntervalTick / 20.0
            for playerId in serverApi.GetPlayerList():
                # 基础代谢与活动代谢共用自动扣减入口，确保模式过滤、dirty 标记和 HUD 跨档同步一致。
                self._consumeAutomatically(playerId, baseDecay)
                data = self._getPlayerData(playerId)
                sprintLimited = data['enabled'] and data['value'] <= config.criticalValue
                if sprintLimited and compGame.GetGameDiffculty() == gameDifficultyEnum.Peaceful:
                    sprintLimited = False
                if sprintLimited:
                    gameType = compGame.GetPlayerGameType(playerId)
                    sprintLimited = (gameType != gameTypeEnum.Spectator and
                                     (gameType != gameTypeEnum.Creative or dietConfig.creativeModeAffected))
                if sprintLimited != data['sprintLimited']:
                    data['sprintLimited'] = sprintLimited
                # 每秒将资格与动作状态汇合到真实属性，维度切换或接口偶发失败后也能自动收敛。
                self._updateSprintSpeedModifier(playerId, data)
        # 伤害资格每 tick 按当前模式判定，不复用低频刷新的冲刺标记，避免切换和平或创造时误伤。
        gameDifficulty = compGame.GetGameDiffculty()
        for playerId in serverApi.GetPlayerList():
            data = self._getPlayerData(playerId)
            gameType = compGame.GetPlayerGameType(playerId)
            if (not data['enabled'] or data['value'] > 0.0 or
                    gameDifficulty == gameDifficultyEnum.Peaceful or
                    gameType == gameTypeEnum.Spectator or
                    (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
                data['dehydrationTicks'] = 0
                continue
            data['dehydrationTicks'] += 1
            if data['dehydrationTicks'] < config.dehydrationDamageIntervalTick:
                continue
            data['dehydrationTicks'] = 0
            if gameDifficulty == gameDifficultyEnum.Easy:
                minHealth = config.easyDehydrationMinHealth
            elif gameDifficulty == gameDifficultyEnum.Normal:
                minHealth = config.normalDehydrationMinHealth
            else:
                minHealth = 0.0
            compAttr = compFactory.CreateAttr(playerId)
            health = compAttr.GetAttrValue(attrType.HEALTH)
            if health <= minHealth:
                continue
            damage = min(config.dehydrationDamage, health - minHealth)
            # 脱水伤害复用原版饥饿伤害来源以绕过护甲；生命下限已在调用前按当前难度裁剪。
            compHurt = compFactory.CreateHurt(playerId)
            compHurt.Hurt(damage, actorDamageCause.Starve, None, None, False)
        if self.tickCounter % config.dataSaveIntervalTick == 0:
            # 自动代谢的浮点小量合并到固定周期再写 ModAttr；退出与 Destroy 仍会强制保存兜底。
            for playerId in self.playerThirstData:
                data = self.playerThirstData[playerId]
                if data['dirty']:
                    Thirst.savePlayerData(playerId, data, compFactory)
                    data['dirty'] = False

    # 多个事件和公开接口都需要确保玩家数据已载入，统一入口避免重复创建缓存。
    def _getPlayerData(self, playerId):
        if playerId not in self.playerThirstData:
            self.playerThirstData[playerId] = Thirst.loadPlayerData(playerId, compFactory)
        return self.playerThirstData[playerId]

    # 疾跑动作与低口渴资格由不同事件维护，此处统一幂等增删只抵消原版疾跑倍率的速度修饰符。
    def _updateSprintSpeedModifier(self, playerId, data):
        compAttr = compFactory.CreateAttr(playerId)
        hasModifier = compAttr.HasModifier(attrType.SPEED, config.sprintLimitModifierId)
        gameType = compGame.GetPlayerGameType(playerId)
        modeAffected = (gameType != gameTypeEnum.Spectator and
                        (gameType != gameTypeEnum.Creative or dietConfig.creativeModeAffected))
        shouldLimitSpeed = modeAffected and data['sprinting'] and (data['sprintLimited'] or bool(data['sprintLimitSources']))
        if shouldLimitSpeed == hasModifier:
            return
        if shouldLimitSpeed:
            result = compAttr.AddModifier(
                attrType.SPEED,
                config.sprintLimitModifierId,
                config.sprintLimitModifierAmount,
                attributeModifierOperation.OperationMultiplyTotal,
                attributeOperands.OperandCurrent
            )
            if not result:
                print("[DietNullGr] 添加低口渴疾跑修饰符失败: {}".format(playerId))
            return
        result = compAttr.RemoveModifier(attrType.SPEED, config.sprintLimitModifierId)
        if not result:
            print("[DietNullGr] 移除低口渴疾跑修饰符失败: {}".format(playerId))

    # 公开接口和关键状态变动按“落盘→可选 HUD 同步→设置同步”的顺序完成同一事务。
    def _saveAndSync(self, playerId, syncHud, syncSetting):
        data = self.playerThirstData[playerId]
        Thirst.savePlayerData(playerId, data, compFactory)
        data['dirty'] = False
        if syncHud:
            Thirst.syncToClient(self, playerId, data)
        if syncSetting:
            Thirst.syncSettingToClient(self, playerId, data)

    # 基础代谢与饥饿代理都通过此入口过滤不消耗口渴的模式，并合并高频持久化写入。
    def _consumeAutomatically(self, playerId, amount):
        data = self._getPlayerData(playerId)
        if not data['enabled'] or data['value'] <= 0.0:
            return data['value']
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return data['value']
        if compGame.GetGameDiffculty() == gameDifficultyEnum.Peaceful:
            return data['value']
        # 高血糖与发烧共享同一疾病倍率入口，只取当前最高值，避免两种疾病同时存在时连乘。
        diseaseSys = serverApi.GetSystem(com.modName, diseaseConfig.ssname)
        amount *= diseaseSys.getThirstConsumptionMultiplier(playerId)
        oldDisplayValue = Thirst.getDisplayValue(data['value'])
        data['value'] = Thirst.clampThirstValue(data['value'] - amount)
        data['dirty'] = True
        if Thirst.getDisplayValue(data['value']) != oldDisplayValue:
            Thirst.syncToClient(self, playerId, data)
        return data['value']

    # 查询玩家当前口渴真值，返回值保留服务端浮点精度。
    def getThirstValue(self, playerId):
        return self._getPlayerData(playerId)['value']

    # 直接设置口渴真值；系统关闭时保持原值并拒绝玩法侧修改。
    def setThirstValue(self, playerId, value):
        data = self._getPlayerData(playerId)
        if not data['enabled']:
            return data['value']
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return data['value']
        newValue = Thirst.clampThirstValue(value)
        if newValue == data['value']:
            return newValue
        oldDisplayValue = Thirst.getDisplayValue(data['value'])
        data['value'] = newValue
        if newValue > 0.0:
            data['dehydrationTicks'] = 0
        if newValue > config.criticalValue and data['sprintLimited']:
            data['sprintLimited'] = False
            # 补水越过临界值时不等待下一次代谢周期，立即恢复原版疾跑倍率。
            self._updateSprintSpeedModifier(playerId, data)
        # 外部低频接口保持立即落盘兼容性；只有半格显示变化时才发 HUD 数据。
        self._saveAndSync(playerId, Thirst.getDisplayValue(newValue) != oldDisplayValue, False)
        return newValue

    # 在当前真值上增加指定数值，返回裁剪后的最新值。
    def addThirstValue(self, playerId, amount):
        data = self._getPlayerData(playerId)
        if not data['enabled']:
            return data['value']
        return self.setThirstValue(playerId, data['value'] + amount)

    # 从当前真值扣除指定数值，返回裁剪后的最新值。
    def consumeThirstValue(self, playerId, amount):
        data = self._getPlayerData(playerId)
        if not data['enabled']:
            return data['value']
        return self.setThirstValue(playerId, data['value'] - amount)

    # 查询通用设置中的口渴系统开关。
    def isThirstEnabled(self, playerId):
        return self._getPlayerData(playerId)['enabled']

    # 低口渴与疾病限制共用一个疾跑逆修饰符；来源集合保证任一限制解除时不会误删另一来源。
    def setSprintLimitSource(self, playerId, source, limited):
        data = self._getPlayerData(playerId)
        if limited:
            data['sprintLimitSources'][source] = True
        elif source in data['sprintLimitSources']:
            del data['sprintLimitSources'][source]
        self._updateSprintSpeedModifier(playerId, data)
        return bool(data['sprintLimitSources'])

    # 通用设置只改变启用状态，不重置口渴真值；HUD 与设置控件在保存后一起刷新。
    def setThirstEnabled(self, playerId, enabled):
        data = self._getPlayerData(playerId)
        enabled = bool(enabled)
        if enabled == data['enabled']:
            return enabled
        data['enabled'] = enabled
        if not enabled:
            data['dehydrationTicks'] = 0
            data['sprintLimited'] = False
            # 设置关闭属于即时事务，必须同步撤销仍在疾跑中的玩家修饰符。
            self._updateSprintSpeedModifier(playerId, data)
        self._saveAndSync(playerId, True, True)
        return enabled

    def Destroy(self):
        onlinePlayers = serverApi.GetPlayerList()
        for playerId in self.playerThirstData:
            data = self.playerThirstData[playerId]
            data['sprinting'] = False
            data['sprintLimited'] = False
            data['sprintLimitSources'] = {}
            # 热重载时玩家实体仍在线，需要回滚修饰符；世界关闭时实体可能已销毁，不再访问失效组件。
            if playerId in onlinePlayers:
                self._updateSprintSpeedModifier(playerId, data)
            Thirst.savePlayerData(playerId, data, compFactory)
