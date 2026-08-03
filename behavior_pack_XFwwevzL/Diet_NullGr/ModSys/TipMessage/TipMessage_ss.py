# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Diet_NullGr.ModSys.TipMessage.config as config
import Diet_NullGr.ModSys.TipMessage.TipMessage as TipMessage

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
compGame = compFactory.CreateGame(serverApi.GetLevelId())
engineNamespace = serverApi.GetEngineNamespace()
engineSystemName = serverApi.GetEngineSystemName()


class ServerSys(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.playerTipStates = {}
        self.tickCounter = 0
        self.ListenForEvent(engineNamespace, engineSystemName, "AddServerPlayerEvent", self, self.AddServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "DelServerPlayerEvent", self, self.DelServerPlayerEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnScriptTickServer", self, self.OnScriptTickServer)
        print("[DietNullGr] tip message server ready")

    def AddServerPlayerEvent(self, args):
        playerId = args['id']
        # 各服务端系统接收玩家加入事件的先后顺序不固定，保留其他系统可能已经提交的首批提示。
        if playerId not in self.playerTipStates:
            self.playerTipStates[playerId] = TipMessage.createPlayerState()

    def DelServerPlayerEvent(self, args):
        playerId = args['id']
        if playerId in self.playerTipStates:
            del self.playerTipStates[playerId]

    def OnScriptTickServer(self):
        self.tickCounter += 1
        for playerId in self.playerTipStates:
            message = TipMessage.takeReadyMessage(self.playerTipStates[playerId], self.tickCounter)
            if message:
                compGame.SetOneTipMessage(playerId, message)

    # Diet 与 Disease 只通过这个稳定入口提交提示，确保跨系统消息进入同一个玩家批次。
    def enqueueTip(self, playerId, messageKey, message, priority):
        if playerId not in self.playerTipStates:
            self.playerTipStates[playerId] = TipMessage.createPlayerState()
        TipMessage.queueMessage(
            self.playerTipStates[playerId],
            self.tickCounter,
            messageKey,
            message,
            priority
        )

    # 状态类提示失效时从待播批次撤销，已经显示的悬浮窗仍按展示保护期自然消失。
    def removeTip(self, playerId, messageKey):
        if playerId in self.playerTipStates:
            TipMessage.removeMessage(self.playerTipStates[playerId], messageKey)

    def Destroy(self):
        self.playerTipStates = {}
