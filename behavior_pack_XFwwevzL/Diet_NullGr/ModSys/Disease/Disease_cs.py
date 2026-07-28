# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as dietConfig
import Diet_NullGr.ModSys.Disease.config as config

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
playerActionType = clientApi.GetMinecraftEnum().PlayerActionType
engineNamespace = clientApi.GetEngineNamespace()
engineSystemName = clientApi.GetEngineSystemName()


class ClientSys(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.diseaseData = {
            'active': [],
            'activeCount': 0,
            'maxActiveCount': config.maxActiveCount,
            'validEatCount': 0
        }
        self.activeDiseaseIds = {}
        self.playerVisualData = {}
        self.renderedVisualData = {}
        self.injectedPlayers = {}
        self.tickCounter = 0
        self.lastSuccessfulJumpTick = -config.hypoglycemiaJumpIntervalTick
        self.blurRadius = 0.0
        self.blurTargetRadius = 0.0
        self.diseaseOwnsBlur = False
        self.postProcessComp = compFactory.CreatePostProcess(levelId)
        self.ListenForEvent(engineNamespace, engineSystemName, "UiInitFinished", self, self.UiInitFinished)
        self.ListenForEvent(engineNamespace, engineSystemName, "AddPlayerCreatedClientEvent", self, self.AddPlayerCreatedClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "RemovePlayerAOIClientEvent", self, self.RemovePlayerAOIClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ClientJumpButtonPressDownEvent", self, self.ClientJumpButtonPressDownEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnLocalPlayerStartJumpClientEvent", self, self.OnLocalPlayerStartJumpClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnLocalPlayerActionClientEvent", self, self.OnLocalPlayerActionClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnScriptTickClient", self, self.OnScriptTickClient)
        self.ListenForEvent(com.modName, config.ssname, config.syncEvent, self, self.DiseaseSyncData)
        self.ListenForEvent(com.modName, config.ssname, config.visualEvent, self, self.DiseaseVisualSync)
        self.ListenForEvent(com.modName, config.ssname, config.symptomEvent, self, self.DiseaseSymptom)
        print("[DietNullGr] disease client ready")

    def UiInitFinished(self, args):
        playerId = clientApi.GetLocalPlayerId()
        if playerId not in self.injectedPlayers:
            # Add-on 重载可能不会重放本地玩家皮肤完成事件；UI 初始化完成后补做同一套渲染注入，再向服务端请求视觉状态。
            self.AddPlayerCreatedClientEvent({'playerId': playerId})
        self.NotifyToServer(config.clientReadyEvent, {})

    def AddPlayerCreatedClientEvent(self, args):
        playerId = args['playerId']
        queryVariableComp = compFactory.CreateQueryVariable(playerId)
        queryVariableComp.Register(config.bodyScaleQuery, 1.0)
        queryVariableComp.Register(config.headScaleQuery, 1.0)
        actorRenderComp = compFactory.CreateActorRender(playerId)
        actorRenderComp.AddPlayerAnimation(config.playerScaleAnimationKey, config.playerScaleAnimation)
        actorRenderComp.AddPlayerAnimationIntoState(
            'root',
            'third_person',
            config.playerScaleAnimationKey,
            '1.0'
        )
        actorRenderComp.RebuildPlayerRender()
        self.injectedPlayers[playerId] = True
        if playerId not in self.renderedVisualData:
            self.renderedVisualData[playerId] = {
                'bodyScale': 1.0,
                'headScale': 1.0
            }
        visualData = self.renderedVisualData[playerId]
        queryVariableComp.Set(config.bodyScaleQuery, float(visualData['bodyScale']))
        queryVariableComp.Set(config.headScaleQuery, float(visualData['headScale']))
        # AOI 玩家每次创建或换肤都会重建渲染，注入完成后只请求该玩家当前倍率。
        self.NotifyToServer(config.visualReadyEvent, {'playerId': playerId})

    def RemovePlayerAOIClientEvent(self, args):
        playerId = args['playerId']
        if playerId in self.injectedPlayers:
            del self.injectedPlayers[playerId]
        if playerId in self.playerVisualData:
            del self.playerVisualData[playerId]
        if playerId in self.renderedVisualData:
            del self.renderedVisualData[playerId]

    def ClientJumpButtonPressDownEvent(self, args):
        continueJump = args['continueJump']
        if 'hypoglycemia' not in self.activeDiseaseIds:
            return
        if self.tickCounter - self.lastSuccessfulJumpTick < config.hypoglycemiaJumpIntervalTick:
            args['continueJump'] = False

    def OnLocalPlayerStartJumpClientEvent(self, args):
        if 'hypoglycemia' in self.activeDiseaseIds:
            self.lastSuccessfulJumpTick = self.tickCounter
        if 'rickets' in self.activeDiseaseIds:
            self.NotifyToServer(config.jumpEvent, {})

    def OnLocalPlayerActionClientEvent(self, args):
        actionType = args['actionType']
        if actionType != playerActionType.StartSprinting or 'hypoglycemia' not in self.activeDiseaseIds:
            return
        playerId = clientApi.GetLocalPlayerId()
        compFactory.CreateActorMotion(playerId).EndSprinting()

    def OnScriptTickClient(self):
        self.tickCounter += 1
        scaleStep = (config.maximumBoneScale - 1.0) / float(config.visualScaleFadeTick)
        # 服务端事件只更新目标倍率，客户端逐 Tick 逼近目标，使痊愈和远端玩家重建都平滑收敛。
        for playerId in self.injectedPlayers:
            if playerId not in self.playerVisualData:
                continue
            if playerId not in self.renderedVisualData:
                self.renderedVisualData[playerId] = {
                    'bodyScale': 1.0,
                    'headScale': 1.0
                }
            targetData = self.playerVisualData[playerId]
            renderedData = self.renderedVisualData[playerId]
            changed = False
            for scaleName in ('bodyScale', 'headScale'):
                targetScale = float(targetData[scaleName])
                renderedScale = renderedData[scaleName]
                if renderedScale < targetScale:
                    renderedData[scaleName] = min(targetScale, renderedScale + scaleStep)
                    changed = True
                elif renderedScale > targetScale:
                    renderedData[scaleName] = max(targetScale, renderedScale - scaleStep)
                    changed = True
            if changed:
                queryVariableComp = compFactory.CreateQueryVariable(playerId)
                queryVariableComp.Set(config.bodyScaleQuery, float(renderedData['bodyScale']))
                queryVariableComp.Set(config.headScaleQuery, float(renderedData['headScale']))
        if self.blurRadius < self.blurTargetRadius:
            self.blurRadius = min(
                self.blurTargetRadius,
                self.blurRadius + config.gaussianBlurMaxRadius / float(config.gaussianBlurFadeTick)
            )
        elif self.blurRadius > self.blurTargetRadius:
            self.blurRadius = max(
                self.blurTargetRadius,
                self.blurRadius - config.gaussianBlurMaxRadius / float(config.gaussianBlurFadeTick)
            )
        if self.blurTargetRadius > 0.0 and not self.diseaseOwnsBlur:
            # 后处理是客户端全局状态；已有其他界面占用时不抢占，也不在疾病恢复时误关闭它。
            if not self.postProcessComp.CheckGaussianBlurEnabled():
                self.postProcessComp.SetEnableGaussianBlur(True)
                self.diseaseOwnsBlur = True
        if (self.diseaseOwnsBlur and self.blurTargetRadius > 0.0 and
                not self.postProcessComp.CheckGaussianBlurEnabled()):
            # 其他界面关闭时可能顺手关闭全局模糊；疾病仍持续则在下一 Tick 恢复症状表现。
            self.postProcessComp.SetEnableGaussianBlur(True)
        if self.diseaseOwnsBlur and self.blurRadius > 0.0:
            self.postProcessComp.SetGaussianBlurRadius(self.blurRadius)
        if self.diseaseOwnsBlur and self.blurRadius <= 0.0 and self.blurTargetRadius <= 0.0:
            self.postProcessComp.SetEnableGaussianBlur(False)
            self.diseaseOwnsBlur = False

    def DiseaseSyncData(self, args):
        active = args['active']
        activeCount = args['activeCount']
        maxActiveCount = args['maxActiveCount']
        validEatCount = args['validEatCount']
        self.diseaseData = {
            'active': active,
            'activeCount': activeCount,
            'maxActiveCount': maxActiveCount,
            'validEatCount': validEatCount
        }
        self.activeDiseaseIds = {}
        hypoglycemiaSeconds = -1
        for diseaseData in active:
            diseaseId = diseaseData['id']
            self.activeDiseaseIds[diseaseId] = True
            if diseaseId == 'hypoglycemia':
                hypoglycemiaSeconds = diseaseData['activeSeconds']
        if hypoglycemiaSeconds >= config.hypoglycemiaLateSeconds:
            growRatio = min(
                1.0,
                (hypoglycemiaSeconds - config.hypoglycemiaLateSeconds) / config.gaussianBlurGrowSeconds
            )
            self.blurTargetRadius = config.gaussianBlurMaxRadius * (0.1 + growRatio * 0.9)
        else:
            self.blurTargetRadius = 0.0
        if 'hypoglycemia' in self.activeDiseaseIds:
            playerId = clientApi.GetLocalPlayerId()
            compFactory.CreateActorMotion(playerId).EndSprinting()
        mainClientSys = clientApi.GetSystem(com.modName, com.csname)
        uiNode = clientApi.GetUI(com.modName, dietConfig.uiKey)
        # 关闭或热重载后主系统可能仍保留陈旧 uiNode，只有 UI 管理器返回当前实例时才刷新。
        if mainClientSys.uiNode and uiNode:
            uiNode.UpdateDiseaseData(self.diseaseData)

    def DiseaseVisualSync(self, args):
        playerId = args['playerId']
        bodyScale = args['bodyScale']
        headScale = args['headScale']
        self.playerVisualData[playerId] = {
            'bodyScale': bodyScale,
            'headScale': headScale
        }
        if playerId not in self.injectedPlayers:
            return
        if playerId not in self.renderedVisualData:
            self.renderedVisualData[playerId] = {
                'bodyScale': 1.0,
                'headScale': 1.0
            }

    def DiseaseSymptom(self, args):
        sound = args['sound']
        volume = args['volume']
        pitch = args['pitch']
        playerId = clientApi.GetLocalPlayerId()
        customAudioComp = compFactory.CreateCustomAudio(levelId)
        customAudioComp.PlayCustomMusic(sound, (0, 0, 0), volume, pitch, False, playerId)

    def Destroy(self):
        for playerId in self.injectedPlayers:
            queryVariableComp = compFactory.CreateQueryVariable(playerId)
            queryVariableComp.Set(config.bodyScaleQuery, 1.0)
            queryVariableComp.Set(config.headScaleQuery, 1.0)
        if self.diseaseOwnsBlur:
            self.postProcessComp.SetEnableGaussianBlur(False)
            self.diseaseOwnsBlur = False
