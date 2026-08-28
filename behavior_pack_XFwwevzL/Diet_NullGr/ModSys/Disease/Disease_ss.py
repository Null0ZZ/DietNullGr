# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Disease.config as config
import Diet_NullGr.ModSys.Disease.Disease as Disease
import Diet_NullGr.ModSys.Diet.config as dietConfig
import Diet_NullGr.ModSys.Diet.Diet as Diet
import Diet_NullGr.ModSys.Thirst.config as thirstConfig
import Diet_NullGr.ModSys.TipMessage.config as tipMessageConfig

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
compGame = compFactory.CreateGame(serverApi.GetLevelId())
blockInfoComp = compFactory.CreateBlockInfo(serverApi.GetLevelId())
minecraftEnum = serverApi.GetMinecraftEnum()
playerActionType = minecraftEnum.PlayerActionType
actorDamageCause = minecraftEnum.ActorDamageCause
attrType = minecraftEnum.AttrType
gameTypeEnum = minecraftEnum.GameType
engineNamespace = serverApi.GetEngineNamespace()
engineSystemName = serverApi.GetEngineSystemName()


class ServerSys(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.playerDiseaseData = {}
        self.pendingMetabolism = {}
        self.crouchStates = {}
        self.swimmingPlayers = {}
        self.jumpDamageCooldowns = {}
        self.jumpSequences = {}
        self.nauseaCooldowns = {}
        self.tickCounter = 0
        self.ListenForEvent(engineNamespace, engineSystemName, "AddServerPlayerEvent", self, self.AddServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ClientLoadAddonsFinishServerEvent", self, self.ClientLoadAddonsFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "DelServerPlayerEvent", self, self.DelServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerDieEvent", self, self.PlayerDieEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerRespawnFinishServerEvent", self, self.PlayerRespawnFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnPlayerActionServerEvent", self, self.OnPlayerActionServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ActuallyHurtServerEvent", self, self.ActuallyHurtServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ActorHurtServerEvent", self, self.ActorHurtServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "GameTypeChangedServerEvent", self, self.GameTypeChangedServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnScriptTickServer", self, self.OnScriptTickServer)
        self.ListenForEvent(com.modName, config.csname, config.clientReadyEvent, self, self.DiseaseClientReady)
        self.ListenForEvent(com.modName, config.csname, config.visualReadyEvent, self, self.DiseaseVisualReady)
        self.ListenForEvent(com.modName, config.csname, config.jumpEvent, self, self.DiseasePlayerJump)
        self.ListenForEvent(com.modName, com.csname, config.settingEventUpdate, self, self.DietSettingUpdate)
        print("[DietNullGr] disease server ready")

    def AddServerPlayerEvent(self, args):
        playerId = args['id']
        self.playerDiseaseData[playerId] = Disease.loadPlayerData(playerId, compFactory)
        self.jumpDamageCooldowns[playerId] = 0
        self.jumpSequences[playerId] = 0
        self.nauseaCooldowns[playerId] = 0

    def ClientLoadAddonsFinishServerEvent(self, args):
        playerId = args['playerId']
        data = self._getPlayerData(playerId)
        gameType = compGame.GetPlayerGameType(playerId)
        modeAffected = (gameType != gameTypeEnum.Spectator and
                        (gameType != gameTypeEnum.Creative or dietConfig.creativeModeAffected))
        if data['enabled'] and modeAffected:
            self._updateHypoglycemiaSprintLimit(playerId, data)
            self._refreshDiseaseEffects(playerId, data)
            self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))
        elif not data['enabled']:
            # 关闭状态可能来自上次存档，实体加载完成后必须再次收敛效果、疾跑来源和全员视觉。
            self._clearDiseaseSystemState(playerId, data)
        else:
            self._suspendDiseaseEffects(playerId, data)
        Disease.syncSettingToClient(self, playerId, data)
        for visualPlayerId in serverApi.GetPlayerList():
            visualData = self._getPlayerData(visualPlayerId)
            self.NotifyToClient(playerId, config.visualEvent, self._buildVisualData(visualPlayerId, visualData))

    def DiseaseClientReady(self, args):
        playerId = args['__id__']
        data = self._getPlayerData(playerId)
        gameType = compGame.GetPlayerGameType(playerId)
        modeAffected = (gameType != gameTypeEnum.Spectator and
                        (gameType != gameTypeEnum.Creative or dietConfig.creativeModeAffected))
        if data['enabled'] and modeAffected:
            self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))
        elif not data['enabled']:
            # 热重载可能只重新触发客户端就绪，关闭状态仍需走完整清理事务，不能依赖玩家重进世界。
            self._clearDiseaseSystemState(playerId, data)
        else:
            self._suspendDiseaseEffects(playerId, data)
        Disease.syncSettingToClient(self, playerId, data)
        # 新客户端完成 AOI 玩家渲染注入后补发全部视觉状态，避免服务端状态先于实体创建到达。
        for visualPlayerId in serverApi.GetPlayerList():
            visualData = self._getPlayerData(visualPlayerId)
            self.NotifyToClient(playerId, config.visualEvent, self._buildVisualData(visualPlayerId, visualData))

    def DietSettingUpdate(self, args):
        playerId = args['__id__']
        settingKey = args['key']
        value = args['value']
        if settingKey != config.settingEnabledKey:
            return
        data = self._getPlayerData(playerId)
        # 通用设置回调属于客户端输入边界，兼容引擎可能回传的布尔值、数字或字符串形式。
        enabled = not (value == False or value == 0 or value == "False" or value == "false" or value == "0")
        if enabled == data['enabled']:
            return
        data['enabled'] = enabled
        if not enabled:
            # 总开关关闭必须同时清空持久状态、运行时症状和客户端表现，避免任一链路残留旧疾病。
            self._clearDiseaseSystemState(playerId, data)
        else:
            Disease.savePlayerData(playerId, data, compFactory)
        Disease.syncSettingToClient(self, playerId, data)

    def GameTypeChangedServerEvent(self, args):
        playerId = args['playerId']
        oldGameType = args['oldGameType']
        newGameType = args['newGameType']
        playerIds = [playerId] if playerId else serverApi.GetPlayerList()
        for currentPlayerId in playerIds:
            gameType = newGameType if playerId else compGame.GetPlayerGameType(currentPlayerId)
            data = self._getPlayerData(currentPlayerId)
            if (gameType == gameTypeEnum.Spectator or
                    (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
                # 疾病进度留在服务端存档中，只暂停效果、症状、提示和客户端外观。
                self._suspendDiseaseEffects(currentPlayerId, data)
            elif data['enabled']:
                self._updateHypoglycemiaSprintLimit(currentPlayerId, data)
                self._refreshDiseaseEffects(currentPlayerId, data)
                self.NotifyToClient(currentPlayerId, config.syncEvent, Disease.buildClientData(data))
                self.BroadcastToAllClient(config.visualEvent, self._buildVisualData(currentPlayerId, data))

    def DiseaseVisualReady(self, args):
        clientPlayerId = args['__id__']
        visualPlayerId = args['playerId']
        onlinePlayers = serverApi.GetPlayerList()
        if clientPlayerId not in onlinePlayers or visualPlayerId not in onlinePlayers:
            return
        visualData = self._getPlayerData(visualPlayerId)
        self.NotifyToClient(clientPlayerId, config.visualEvent, self._buildVisualData(visualPlayerId, visualData))

    def DelServerPlayerEvent(self, args):
        playerId = args['id']
        if playerId in self.playerDiseaseData:
            Disease.savePlayerData(playerId, self.playerDiseaseData[playerId], compFactory)
            del self.playerDiseaseData[playerId]
        if playerId in self.pendingMetabolism:
            del self.pendingMetabolism[playerId]
        if playerId in self.crouchStates:
            del self.crouchStates[playerId]
        if playerId in self.swimmingPlayers:
            del self.swimmingPlayers[playerId]
        if playerId in self.jumpDamageCooldowns:
            del self.jumpDamageCooldowns[playerId]
        if playerId in self.jumpSequences:
            del self.jumpSequences[playerId]
        if playerId in self.nauseaCooldowns:
            del self.nauseaCooldowns[playerId]

    def PlayerDieEvent(self, args):
        playerId = args['id']
        attacker = args['attacker']
        customTag = args['customTag']
        cause = args['cause']
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        data = self._getPlayerData(playerId)
        cured = Disease.resetAfterDeath(data)
        if playerId in self.pendingMetabolism:
            del self.pendingMetabolism[playerId]
        if playerId in self.crouchStates:
            del self.crouchStates[playerId]
        if playerId in self.swimmingPlayers:
            del self.swimmingPlayers[playerId]
        self.jumpDamageCooldowns[playerId] = 0
        self.nauseaCooldowns[playerId] = 0
        self._finishDiseaseChanges(playerId, data, [], cured)

    def PlayerRespawnFinishServerEvent(self, args):
        playerId = args['playerId']
        data = self._getPlayerData(playerId)
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            self._suspendDiseaseEffects(playerId, data)
            return
        self._updateHypoglycemiaSprintLimit(playerId, data)
        self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))
        self.BroadcastToAllClient(config.visualEvent, self._buildVisualData(playerId, data))

    def OnPlayerActionServerEvent(self, args):
        playerId = args['playerId']
        actionType = args['actionType']
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            if playerId in self.crouchStates:
                del self.crouchStates[playerId]
            if playerId in self.swimmingPlayers:
                del self.swimmingPlayers[playerId]
            return
        if actionType == playerActionType.StartSwimming:
            self.swimmingPlayers[playerId] = True
            # 游泳开始会中断正在记录的下蹲事务，避免出水后的 StopSneaking 被误结算。
            if playerId in self.crouchStates:
                del self.crouchStates[playerId]
            return
        if actionType == playerActionType.StopSwimming:
            if playerId in self.swimmingPlayers:
                del self.swimmingPlayers[playerId]
            return
        if actionType == playerActionType.StartSneaking:
            data = self._getPlayerData(playerId)
            if 'constipation' not in data['active']:
                return
            groundedData = self._getGroundedFootData(playerId)
            if groundedData is None:
                return
            self.crouchStates[playerId] = {
                'startTick': self.tickCounter,
                'footPos': groundedData['footPos'],
                'dimensionId': groundedData['dimensionId']
            }
            return
        if actionType != playerActionType.StopSneaking or playerId not in self.crouchStates:
            return
        crouchState = self.crouchStates[playerId]
        del self.crouchStates[playerId]
        if self.tickCounter - crouchState['startTick'] < config.constipationSneakHoldTick:
            return
        data = self._getPlayerData(playerId)
        if 'constipation' not in data['active']:
            return
        groundedData = self._getGroundedFootData(playerId)
        if groundedData is None or groundedData['dimensionId'] != crouchState['dimensionId']:
            return
        if abs(groundedData['footPos'][1] - crouchState['footPos'][1]) > config.constipationMaxVerticalMove:
            return
        # 一次完整站立→下蹲→站立事务只在结束事件结算，按住下蹲不会重复累计。
        cured = Disease.recordConstipationSquat(data)
        if cured:
            # 下蹲治愈先完成效果和数据收敛，再只给患者播放音效，并逐个向所有在线玩家显示同一条 tip。
            self._finishDiseaseChanges(playerId, data, [], ['constipation'])
            self.NotifyToClient(playerId, config.symptomEvent, {
                'symptomId': config.constipationReliefSymptom,
                'sound': config.constipationReliefSound,
                'volume': config.constipationReliefSoundVolume,
                'pitch': config.constipationReliefSoundPitch
            })
            playerName = compFactory.CreateName(playerId).GetName()
            broadcastKey = tipMessageConfig.constipationBroadcastKeyPrefix + playerId
            for onlinePlayerId in serverApi.GetPlayerList():
                self._queueTipMessage(
                    onlinePlayerId,
                    broadcastKey,
                    "{}玩家拉了一坨大的".format(playerName),
                    tipMessageConfig.priorityNormal
                )
            return
        Disease.savePlayerData(playerId, data, compFactory)
        self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))
        self.BroadcastToAllClient(config.visualEvent, self._buildVisualData(playerId, data))
        self._queueTipMessage(
            playerId,
            tipMessageConfig.constipationProgressKey,
            serverApi.GenerateColor("GREEN") + "便秘缓解进度：{}/{}。".format(
                data['constipationSquatCount'], config.constipationSquatRequired),
            tipMessageConfig.priorityProgress
        )

    def ActuallyHurtServerEvent(self, args):
        srcId = args['srcId']
        projectileId = args['projectileId']
        entityId = args['entityId']
        damage = args['damage']
        invulnerableTime = args['invulnerableTime']
        lastHurt = args['lastHurt']
        cause = args['cause']
        customTag = args['customTag']
        if entityId not in self.playerDiseaseData or cause != actorDamageCause.Fall:
            return
        gameType = compGame.GetPlayerGameType(entityId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        if 'rickets' not in self.playerDiseaseData[entityId]['active']:
            return
        # 当前官方事件只允许修改 damage；在实际伤害结算事件中放大它即可改变本次摔落伤害。
        args['damage'] = float(damage) * config.ricketsFallDamageMultiplier

    def ActorHurtServerEvent(self, args):
        entityId = args['entityId']
        cause = args['cause']
        damage = args['damage']
        absorbedDamage = args['absorbedDamage']
        customTag = args['customTag']
        if entityId not in self.playerDiseaseData or damage <= 0.0:
            return
        gameType = compGame.GetPlayerGameType(entityId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        if 'scurvy' not in self.playerDiseaseData[entityId]['active']:
            return
        compEffect = compFactory.CreateEffect(entityId)
        compEffect.AddEffectToEntity('mining_fatigue', 8, 0, False)

    def DiseasePlayerJump(self, args):
        playerId = args['__id__']
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        data = self._getPlayerData(playerId)
        if 'rickets' not in data['active'] or self.jumpDamageCooldowns[playerId] > 0:
            return
        self.jumpSequences[playerId] += 1
        playerSeed = 0
        for character in playerId:
            playerSeed += ord(character)
        roll = (self.jumpSequences[playerId] * 37 + data['activeSeconds']['rickets'] * 11 + playerSeed) % 100
        if roll >= config.ricketsJumpDamageChance:
            return
        self.jumpDamageCooldowns[playerId] = config.ricketsJumpDamageCooldownTick
        self._hurtWithoutKilling(playerId)
        self.NotifyToClient(playerId, config.symptomEvent, {
            'symptomId': config.ricketsFractureSymptom,
            'sound': config.ricketsFractureSound,
            'volume': config.ricketsFractureSoundVolume,
            'pitch': config.ricketsFractureSoundPitch
        })

    def OnScriptTickServer(self):
        self.tickCounter += 1
        for playerId in self.jumpDamageCooldowns:
            gameType = compGame.GetPlayerGameType(playerId)
            if (gameType == gameTypeEnum.Spectator or
                    (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
                continue
            if self.jumpDamageCooldowns[playerId] > 0:
                self.jumpDamageCooldowns[playerId] -= 1

        # 饥饿事件只排队代谢量；下一 Tick 再读取口渴真值，规避 Diet 与 Thirst 监听顺序不确定。
        for playerId in list(self.pendingMetabolism):
            metabolicPoints = self.pendingMetabolism[playerId]
            del self.pendingMetabolism[playerId]
            data = self._getPlayerData(playerId)
            gameType = compGame.GetPlayerGameType(playerId)
            if (gameType == gameTypeEnum.Spectator or
                    (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
                continue
            if not data['enabled']:
                continue
            snapshot = self._buildNutritionSnapshot(playerId)
            result = Disease.advanceMetabolism(data, metabolicPoints, snapshot)
            Disease.savePlayerData(playerId, data, compFactory)
            if result['diagnosed'] or result['cured']:
                self._finishDiseaseChanges(playerId, data, result['diagnosed'], result['cured'])
            elif data['active']:
                self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))

        if self.tickCounter % 20 != 0:
            return
        for playerId in serverApi.GetPlayerList():
            data = self._getPlayerData(playerId)
            gameType = compGame.GetPlayerGameType(playerId)
            if (gameType == gameTypeEnum.Spectator or
                    (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
                continue
            if not data['enabled']:
                continue
            snapshot = self._buildNutritionSnapshot(playerId)
            cured = Disease.applyNutritionRecovery(data, 0.0, snapshot)
            for diseaseId in Disease.advanceSeconds(data, 1):
                if diseaseId not in cured:
                    cured.append(diseaseId)
            if cured:
                self._finishDiseaseChanges(playerId, data, [], cured)
            elif data['active']:
                self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))
                self.BroadcastToAllClient(config.visualEvent, self._buildVisualData(playerId, data))

            if self.nauseaCooldowns[playerId] > 0:
                self.nauseaCooldowns[playerId] -= 1
            if self.nauseaCooldowns[playerId] <= 0:
                self._triggerIntermittentNausea(playerId, data)
            if self.tickCounter % config.effectRefreshTick == 0:
                self._refreshDiseaseEffects(playerId, data)
        if self.tickCounter % config.dataSaveTick == 0:
            for playerId in self.playerDiseaseData:
                Disease.savePlayerData(playerId, self.playerDiseaseData[playerId], compFactory)

    # 任何真实进食都按进食前患病状态结算症状；有效营养增益才参与计数与饮食恢复。
    def recordFoodEat(self, playerId, dietData, gainValues):
        data = self._getPlayerData(playerId)
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        if not data['enabled']:
            return
        activeBefore = list(data['active'])
        cured = []
        if gainValues:
            snapshot = self._buildNutritionSnapshot(playerId, dietData)
            cured = Disease.recordValidEat(data, snapshot)
            if 'hypoglycemia' in cured and 'grains' not in gainValues:
                data['protectionSeconds']['hypoglycemia'] = config.hypoglycemiaQuickProtectionSeconds
        if 'constipation' in activeBefore:
            compEffect = compFactory.CreateEffect(playerId)
            compEffect.AddEffectToEntity('nausea', config.nauseaDuration, 0, False)
        if 'mouth_ulcer' in activeBefore:
            self._queueTipMessage(
                playerId,
                tipMessageConfig.diseaseSymptomKey,
                "§c口腔溃疡传来一阵刺痛。",
                tipMessageConfig.priorityWarning
            )
            self.NotifyToClient(playerId, config.symptomEvent, {
                'symptomId': config.mouthUlcerPainSymptom,
                'sound': 'game.player.hurt',
                'volume': 1.0,
                'pitch': 1.0
            })
            playerSeed = 0
            for character in playerId:
                playerSeed += ord(character)
            if (data['validEatCount'] * 53 + self.tickCounter * 17 + playerSeed) % 100 < 25:
                self._hurtWithoutKilling(playerId)
        if not gainValues:
            return
        Disease.savePlayerData(playerId, data, compFactory)
        if cured:
            self._finishDiseaseChanges(playerId, data, [], cured)
        else:
            self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))

    # Diet 饥饿回调只累计本轮真实下降量，疾病系统下一 Tick 使用最新口渴值统一判定。
    def queueMetabolism(self, playerId, metabolicPoints):
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        if not self._getPlayerData(playerId)['enabled']:
            return
        if playerId in self.pendingMetabolism:
            self.pendingMetabolism[playerId] += metabolicPoints
        else:
            self.pendingMetabolism[playerId] = metabolicPoints

    # 口渴系统只通过此公开入口读取疾病倍率，高血糖与发烧取较高值而不连乘。
    def getThirstConsumptionMultiplier(self, playerId):
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return 1.0
        data = self._getPlayerData(playerId)
        if 'fever' in data['active']:
            return config.feverThirstMultiplier
        if 'hyperglycemia' in data['active']:
            return config.hyperglycemiaThirstMultiplier
        return 1.0

    # Diet 奖惩刷新通过此入口暂停普通低营养惩罚。
    def hasActiveDisease(self, playerId):
        return bool(self._getPlayerData(playerId)['active'])

    # 高血糖期间暂停糖分冲刺，其他疾病不影响该奖励。
    def isSugarRushPaused(self, playerId):
        return 'hyperglycemia' in self._getPlayerData(playerId)['active']

    # `/diet disease <id>` 只塑造营养条件，确诊仍服从有效进食、代谢、保护期与槽位规则。
    def handleCommand(self, playerId, command, dietData):
        text = command[1:] if command.startswith('/') else command
        parts = text.split()
        if len(parts) < 2 or parts[0] != 'diet' or parts[1] != 'disease':
            return False
        if not config.debugCommandEnabled:
            return False
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return True
        data = self._getPlayerData(playerId)
        if not data['enabled']:
            self._queueTipMessage(
                playerId,
                tipMessageConfig.diseaseCommandKey,
                "§e疾病系统已关闭。",
                tipMessageConfig.priorityImportant
            )
            return True
        if len(parts) == 2 or parts[2] == 'status':
            names = []
            for diseaseId in data['active']:
                names.append(config.diseases[diseaseId]['name'])
            message = "当前疾病：{}。".format('、'.join(names) if names else '无')
            self._queueTipMessage(
                playerId,
                tipMessageConfig.diseaseCommandKey,
                "§e" + message,
                tipMessageConfig.priorityImportant
            )
            return True
        if parts[2] == 'clear':
            cured = list(data['active'])
            for diseaseId in cured:
                Disease.cureDisease(data, diseaseId, False)
            self._finishDiseaseChanges(playerId, data, [], cured)
            return True
        diseaseId = parts[2]
        if diseaseId not in config.diseases:
            self._queueTipMessage(
                playerId,
                tipMessageConfig.diseaseCommandKey,
                "§c未知疾病：{}。".format(diseaseId),
                tipMessageConfig.priorityImportant
            )
            return True
        snapshot = self._buildNutritionSnapshot(playerId, dietData)
        if not Disease.isDiseaseAvailable(diseaseId, snapshot):
            self._queueTipMessage(
                playerId,
                tipMessageConfig.diseaseCommandKey,
                "§c均衡饮食或该疾病所需的营养、口渴追踪未开启。",
                tipMessageConfig.priorityImportant
            )
            return True
        nutritionProfile = config.debugCommandNutritionProfiles[diseaseId]
        for groupId in dietConfig.groupOrder:
            dietData['values'][groupId] = nutritionProfile[groupId]
        thirstSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        thirstSys.setThirstValue(playerId, nutritionProfile['thirst'] * config.thirstMaxValue)
        dietSys = serverApi.GetSystem(com.modName, com.ssname)
        Diet.savePlayerData(playerId, dietData, compFactory)
        Diet.syncToClient(dietSys, playerId, dietData)
        self._queueTipMessage(
            playerId,
            tipMessageConfig.diseaseCommandKey,
            "§e已将营养条件调整为{}的触发状态。继续消耗饥饿值后，系统会按有效进食次数、保护期和槽位规则自然判定。".format(
                config.diseases[diseaseId]['name']
            ),
            tipMessageConfig.priorityImportant
        )
        return True

    # 多个事件共享同一份玩家疾病缓存，统一入口保证首次访问也会恢复 ModAttr。
    def _getPlayerData(self, playerId):
        if playerId not in self.playerDiseaseData:
            self.playerDiseaseData[playerId] = Disease.loadPlayerData(playerId, compFactory)
            self.jumpDamageCooldowns[playerId] = 0
            self.jumpSequences[playerId] = 0
            self.nauseaCooldowns[playerId] = 0
        return self.playerDiseaseData[playerId]

    # 疾病条件必须在同一时刻读取 Diet 与 Thirst 服务端真值，客户端显示值不参与判定。
    def _buildNutritionSnapshot(self, playerId, dietData=None):
        if dietData is None:
            dietSys = serverApi.GetSystem(com.modName, com.ssname)
            dietData = dietSys.playerDietData[playerId]
        thirstSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        thirstData = {
            'value': thirstSys.getThirstValue(playerId),
            'enabled': thirstSys.isThirstEnabled(playerId)
        }
        return Disease.buildNutritionSnapshot(dietData, thirstData)

    # 创造或旁观模式只冻结疾病运行时表现，服务端疾病进度保持不变，返回生存后可继续结算。
    def _suspendDiseaseEffects(self, playerId, data):
        tipMessageSys = serverApi.GetSystem(com.modName, tipMessageConfig.ssname)
        tipMessageSys.removeTip(playerId, tipMessageConfig.constipationProgressKey)
        tipMessageSys.removeTip(playerId, tipMessageConfig.diseaseSymptomKey)
        tipMessageSys.removeTip(playerId, tipMessageConfig.diseaseChangeKey)
        if playerId in self.pendingMetabolism:
            del self.pendingMetabolism[playerId]
        if playerId in self.crouchStates:
            del self.crouchStates[playerId]
        if playerId in self.swimmingPlayers:
            del self.swimmingPlayers[playerId]
        compEffect = compFactory.CreateEffect(playerId)
        for diseaseId in config.diseaseOrder:
            compEffect.RemoveEffectFromEntity(config.diseases[diseaseId]['customEffect'])
        for effectName in ('slowness', 'weakness', 'nausea', 'mining_fatigue'):
            compEffect.RemoveEffectFromEntity(effectName)
        thirstSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        thirstSys.setSprintLimitSource(playerId, config.hypoglycemiaSprintLimitSource, False)
        clientData = Disease.buildClientData(data)
        clientData['active'] = []
        clientData['activeCount'] = 0
        self.NotifyToClient(playerId, config.syncEvent, clientData)
        self.BroadcastToAllClient(config.visualEvent, {
            'playerId': playerId,
            'bodyScale': 1.0,
            'headScale': 1.0
        })

    # 总开关关闭和关闭存档恢复共用此事务，统一清理状态、效果、疾跑来源及所有客户端骨骼表现。
    def _clearDiseaseSystemState(self, playerId, data):
        Disease.clearAllDiseaseState(data)
        # 疾病关闭后撤销所有尚未展示的疾病状态提示，避免展示锁结束时播放失效内容。
        tipMessageSys = serverApi.GetSystem(com.modName, tipMessageConfig.ssname)
        tipMessageSys.removeTip(playerId, tipMessageConfig.constipationProgressKey)
        tipMessageSys.removeTip(playerId, tipMessageConfig.diseaseSymptomKey)
        tipMessageSys.removeTip(playerId, tipMessageConfig.diseaseChangeKey)
        if playerId in self.pendingMetabolism:
            del self.pendingMetabolism[playerId]
        if playerId in self.crouchStates:
            del self.crouchStates[playerId]
        self.jumpDamageCooldowns[playerId] = 0
        self.jumpSequences[playerId] = 0
        self.nauseaCooldowns[playerId] = 0
        compEffect = compFactory.CreateEffect(playerId)
        for diseaseId in config.diseaseOrder:
            compEffect.RemoveEffectFromEntity(config.diseases[diseaseId]['customEffect'])
        for effectName in ('slowness', 'weakness', 'nausea', 'mining_fatigue'):
            compEffect.RemoveEffectFromEntity(effectName)
        self._updateHypoglycemiaSprintLimit(playerId, data)
        Disease.savePlayerData(playerId, data, compFactory)
        self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))
        self.BroadcastToAllClient(config.visualEvent, self._buildVisualData(playerId, data))

    # 确诊/痊愈事务按“效果→疾跑来源→保存→本地数据→全员视觉”顺序一次性收敛。
    def _finishDiseaseChanges(self, playerId, data, diagnosed, cured):
        compEffect = compFactory.CreateEffect(playerId)
        changeMessages = []
        if 'constipation' in cured:
            # 痊愈提示提交前先撤销尚未展示的下蹲进度，避免聚合批次在治愈后播报旧进度。
            tipMessageSys = serverApi.GetSystem(com.modName, tipMessageConfig.ssname)
            tipMessageSys.removeTip(playerId, tipMessageConfig.constipationProgressKey)
        for diseaseId in cured:
            compEffect.RemoveEffectFromEntity(config.diseases[diseaseId]['customEffect'])
            changeMessages.append("§a{}已经缓解。".format(config.diseases[diseaseId]['name']))
        self._refreshDiseaseEffects(playerId, data)
        for diseaseId in diagnosed:
            diseaseConfig = config.diseases[diseaseId]
            changeMessages.append(
                "§c你患上了{}，请打开饮食界面查看症状和缓解方式。".format(diseaseConfig['name'])
            )
        if changeMessages:
            self._queueTipMessage(
                playerId,
                tipMessageConfig.diseaseChangeKey,
                "\n".join(changeMessages),
                tipMessageConfig.priorityImportant
            )
        self._updateHypoglycemiaSprintLimit(playerId, data)
        Disease.savePlayerData(playerId, data, compFactory)
        self.NotifyToClient(playerId, config.syncEvent, Disease.buildClientData(data))
        self.BroadcastToAllClient(config.visualEvent, self._buildVisualData(playerId, data))

    # 自定义效果负责效果栏，原版短效果负责症状；短周期刷新不会误删其他模组同名效果。
    def _refreshDiseaseEffects(self, playerId, data):
        if not data['enabled']:
            return
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        compEffect = compFactory.CreateEffect(playerId)
        for diseaseId in data['active']:
            diseaseConfig = config.diseases[diseaseId]
            remainingSeconds = diseaseConfig['maxActiveSeconds'] - data['activeSeconds'][diseaseId]
            duration = max(1, remainingSeconds + config.customEffectDurationPadding)
            compEffect.AddEffectToEntity(diseaseConfig['customEffect'], duration, 0, False)
        if 'hyperglycemia' in data['active']:
            compEffect.AddEffectToEntity('slowness', config.statusEffectDuration, 0, False)
        if 'fever' in data['active'] or 'scurvy' in data['active']:
            compEffect.AddEffectToEntity('weakness', config.statusEffectDuration, 0, False)

    # 低血糖疾跑资格交给 Thirst 的共享来源集合，避免与低口渴逆修饰符重复叠加。
    def _updateHypoglycemiaSprintLimit(self, playerId, data):
        thirstSys = serverApi.GetSystem(com.modName, thirstConfig.ssname)
        gameType = compGame.GetPlayerGameType(playerId)
        modeAffected = (gameType != gameTypeEnum.Spectator and
                        (gameType != gameTypeEnum.Creative or dietConfig.creativeModeAffected))
        thirstSys.setSprintLimitSource(
            playerId,
            config.hypoglycemiaSprintLimitSource,
            modeAffected and 'hypoglycemia' in data['active']
        )

    # 三种间歇反胃共用专属时长和冷却，便秘的进食反胃仍按独立时长结算。
    def _triggerIntermittentNausea(self, playerId, data):
        shouldTrigger = False
        if 'hypoglycemia' in data['active']:
            seconds = data['activeSeconds']['hypoglycemia']
            shouldTrigger = (seconds >= config.hypoglycemiaLateSeconds and
                             (seconds - config.hypoglycemiaLateSeconds) % config.hypoglycemiaNauseaIntervalSeconds == 0)
        if not shouldTrigger and 'hyperglycemia' in data['active']:
            seconds = data['activeSeconds']['hyperglycemia']
            shouldTrigger = seconds > 0 and seconds % config.hyperglycemiaNauseaIntervalSeconds == 0
        if not shouldTrigger and 'fever' in data['active']:
            seconds = data['activeSeconds']['fever']
            shouldTrigger = seconds > 0 and seconds % config.feverNauseaIntervalSeconds == 0
        if not shouldTrigger:
            return
        compEffect = compFactory.CreateEffect(playerId)
        compEffect.AddEffectToEntity('nausea', config.intermittentNauseaDuration, 0, False)
        self.nauseaCooldowns[playerId] = config.nauseaSharedCooldownSeconds

    # 下蹲只在非骑乘、非旁观且脚下是实体方块时有效，同时返回脚部位置供结束事件校验腾空。
    def _getGroundedFootData(self, playerId):
        if compFactory.CreateRide(playerId).IsEntityRiding():
            return None
        if playerId in self.swimmingPlayers:
            return None
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return None
        footPos = compFactory.CreatePos(playerId).GetFootPos()
        dimensionId = compFactory.CreateDimension(playerId).GetEntityDimensionId()
        footBlockPos = (
            int(footPos[0] // 1),
            int(footPos[1] // 1),
            int(footPos[2] // 1)
        )
        footBlockName = blockInfoComp.GetBlockNew(footBlockPos, dimensionId)['name']
        if footBlockName in config.invalidBodyBlocks:
            return None
        blockPos = (
            int(footPos[0] // 1),
            int((footPos[1] - 0.1) // 1),
            int(footPos[2] // 1)
        )
        blockName = blockInfoComp.GetBlockNew(blockPos, dimensionId)['name']
        if blockName in config.invalidGroundBlocks:
            return None
        return {
            'footPos': footPos,
            'dimensionId': dimensionId
        }

    # 趣味症状伤害统一保护最后一点生命，避免进食或跳跃直接杀死玩家。
    def _hurtWithoutKilling(self, playerId):
        compAttr = compFactory.CreateAttr(playerId)
        health = compAttr.GetAttrValue(attrType.HEALTH)
        if health <= config.minimumHealthAfterSymptom:
            return False
        damage = min(config.symptomDamage, health - config.minimumHealthAfterSymptom)
        compHurt = compFactory.CreateHurt(playerId)
        # 网易 3.9 的 Hurt 组件会拒绝 Custom 伤害来源；Magic 支持无攻击者伤害并保留症状伤害的生命下限。
        compHurt.Hurt(damage, actorDamageCause.Magic, None, None, False)
        return True

    # 客户端只接收最终骨骼倍率，碰撞箱和服务端属性保持不变。
    def _buildVisualData(self, playerId, data):
        bodyScale = 1.0
        headScale = 1.0
        gameType = compGame.GetPlayerGameType(playerId)
        modeAffected = (gameType != gameTypeEnum.Spectator and
                        (gameType != gameTypeEnum.Creative or dietConfig.creativeModeAffected))
        if modeAffected and 'constipation' in data['active']:
            growRatio = min(1.0, data['activeSeconds']['constipation'] / config.constipationBodyGrowSeconds)
            reliefRatio = 1.0 - data['constipationSquatCount'] / float(config.constipationSquatRequired)
            bodyScale += (config.constipationMaximumBodyScale - 1.0) * growRatio * reliefRatio
        if modeAffected and 'fever' in data['active']:
            growRatio = min(1.0, data['activeSeconds']['fever'] / config.feverHeadGrowSeconds)
            headScale += (config.feverMaximumHeadScale - 1.0) * growRatio
        return {
            'playerId': playerId,
            'bodyScale': bodyScale,
            'headScale': headScale
        }

    # 多个疾病事务共享同一提示服务，冻结模式不再提交疾病消息。
    def _queueTipMessage(self, playerId, messageKey, message, priority):
        gameType = compGame.GetPlayerGameType(playerId)
        if (gameType == gameTypeEnum.Spectator or
                (gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected)):
            return
        tipMessageSys = serverApi.GetSystem(com.modName, tipMessageConfig.ssname)
        tipMessageSys.enqueueTip(playerId, messageKey, message, priority)

    def Destroy(self):
        onlinePlayers = serverApi.GetPlayerList()
        for playerId in self.playerDiseaseData:
            data = self.playerDiseaseData[playerId]
            if playerId in onlinePlayers:
                for diseaseId in data['active']:
                    compEffect = compFactory.CreateEffect(playerId)
                    compEffect.RemoveEffectFromEntity(config.diseases[diseaseId]['customEffect'])
                self.BroadcastToAllClient(config.visualEvent, {
                    'playerId': playerId,
                    'bodyScale': 1.0,
                    'headScale': 1.0
                })
                self._updateHypoglycemiaSprintLimit(playerId, {'active': []})
            Disease.savePlayerData(playerId, data, compFactory)
