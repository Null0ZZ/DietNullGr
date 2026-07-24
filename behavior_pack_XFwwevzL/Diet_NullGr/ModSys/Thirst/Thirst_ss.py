# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Thirst.config as config
import Diet_NullGr.ModSys.Thirst.Thirst as Thirst

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
compGame = compFactory.CreateGame(serverApi.GetLevelId())
gameTypeEnum = serverApi.GetMinecraftEnum().GameType
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
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerHungerChangeServerEvent", self, self.PlayerHungerChangeServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "PlayerRespawnFinishServerEvent", self, self.PlayerRespawnFinishServerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnScriptTickServer", self, self.OnScriptTickServer)
        self.ListenForEvent(com.modName, config.csname, config.clientReadyEvent, self, self.ThirstClientReady)
        self.ListenForEvent(com.modName, com.csname, config.settingEventUpdate, self, self.DietSettingUpdate)
        print("[DietNullGr] thirst server ready")

    def AddServerPlayerEvent(self, args):
        playerId = args['id']
        self.playerThirstData[playerId] = Thirst.loadPlayerData(playerId, compFactory)

    def ClientLoadAddonsFinishServerEvent(self, args):
        playerId = args['playerId']
        data = self._getPlayerData(playerId)
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
        if settingKey != config.settingEnabledKey:
            return
        # 通用设置回调属于客户端输入边界，兼容引擎可能回传的布尔值、数字或字符串形式。
        enabled = not (value == False or value == 0 or value == "False" or value == "false" or value == "0")
        self.setThirstEnabled(playerId, enabled)

    def DelServerPlayerEvent(self, args):
        playerId = args['id']
        if playerId not in self.playerThirstData:
            return
        Thirst.savePlayerData(playerId, self.playerThirstData[playerId], compFactory)
        del self.playerThirstData[playerId]

    def PlayerHungerChangeServerEvent(self, args):
        playerId = args['playerId']
        hungerBefore = args['hungerBefore']
        hunger = args['hunger']
        if hunger >= hungerBefore:
            return
        # 原版饥饿下降是当前接口能稳定提供的活动量代理；扣减先进入内存，统一等待周期保存。
        self._consumeAutomatically(playerId, (hungerBefore - hunger) * config.hungerDecayFactor)

    def PlayerRespawnFinishServerEvent(self, args):
        playerId = args['playerId']
        data = self._getPlayerData(playerId)
        if not data['enabled'] or data['value'] == config.respawnValue:
            return
        oldDisplayValue = Thirst.getDisplayValue(data['value'])
        data['value'] = Thirst.clampThirstValue(config.respawnValue)
        # 复活重置必须立即落盘，避免玩家在下一次批量保存前退出后又恢复为死亡前的低口渴值。
        self._saveAndSync(playerId, Thirst.getDisplayValue(data['value']) != oldDisplayValue, False)

    def OnScriptTickServer(self):
        self.tickCounter += 1
        if self.tickCounter % config.baseDecayIntervalTick == 0:
            baseDecay = config.baseDecayPerSecond * config.baseDecayIntervalTick / 20.0
            for playerId in serverApi.GetPlayerList():
                # 基础代谢与活动代谢共用自动扣减入口，确保模式过滤、dirty 标记和 HUD 跨档同步一致。
                self._consumeAutomatically(playerId, baseDecay)
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
        if gameType == gameTypeEnum.Creative or gameType == gameTypeEnum.Spectator:
            return data['value']
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
        newValue = Thirst.clampThirstValue(value)
        if newValue == data['value']:
            return newValue
        oldDisplayValue = Thirst.getDisplayValue(data['value'])
        data['value'] = newValue
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

    # 通用设置只改变启用状态，不重置口渴真值；HUD 与设置控件在保存后一起刷新。
    def setThirstEnabled(self, playerId, enabled):
        data = self._getPlayerData(playerId)
        enabled = bool(enabled)
        if enabled == data['enabled']:
            return enabled
        data['enabled'] = enabled
        self._saveAndSync(playerId, True, True)
        return enabled

    def Destroy(self):
        for playerId in self.playerThirstData:
            Thirst.savePlayerData(playerId, self.playerThirstData[playerId], compFactory)
