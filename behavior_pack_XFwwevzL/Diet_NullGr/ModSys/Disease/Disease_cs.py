# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as dietConfig
import Diet_NullGr.ModSys.Disease.config as config

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
compGame = compFactory.CreateGame(levelId)
engineNamespace = clientApi.GetEngineNamespace()
engineSystemName = clientApi.GetEngineSystemName()


class ClientSys(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.diseaseData = {
            'active': [],
            'activeCount': 0,
            'maxActiveCount': config.maxActiveCount,
            'validEatCount': 0,
            'constipationSquatCount': 0
        }
        self.activeDiseaseIds = {}
        self.playerVisualData = {}
        self.renderedVisualData = {}
        self.injectedPlayers = {}
        self.tickCounter = 0
        self.lastSuccessfulJumpTick = -config.hypoglycemiaJumpIntervalTick
        self.constipationVisionStrength = 0.0
        self.constipationVisionTargetStrength = 0.0
        self.diseaseOwnsConstipationVision = False
        self.hypoglycemiaVisionStrength = 0.0
        self.hypoglycemiaVisionTargetStrength = 0.0
        self.diseaseOwnsHypoglycemiaVision = False
        self.ricketsFractureVisionElapsedTick = -1
        self.ricketsFractureAspectRatio = 1.0
        self.diseaseOwnsRicketsFractureVision = False
        self.postProcessComp = compFactory.CreatePostProcess(levelId)
        self.ListenForEvent(engineNamespace, engineSystemName, "UiInitFinished", self, self.UiInitFinished)
        self.ListenForEvent(engineNamespace, engineSystemName, "AddPlayerCreatedClientEvent", self, self.AddPlayerCreatedClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "RemovePlayerAOIClientEvent", self, self.RemovePlayerAOIClientEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "ClientJumpButtonPressDownEvent", self, self.ClientJumpButtonPressDownEvent)
        self.ListenForEvent(engineNamespace, engineSystemName, "OnLocalPlayerStartJumpClientEvent", self, self.OnLocalPlayerStartJumpClientEvent)
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

    def OnScriptTickClient(self):
        self.tickCounter += 1
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
            for scaleName, maximumScale in (
                ('bodyScale', config.constipationMaximumBodyScale),
                ('headScale', config.feverMaximumHeadScale)
            ):
                scaleStep = (maximumScale - 1.0) / float(config.visualScaleFadeTick)
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
        if self.constipationVisionStrength < self.constipationVisionTargetStrength:
            self.constipationVisionStrength = min(
                self.constipationVisionTargetStrength,
                self.constipationVisionStrength +
                config.constipationVisionMaxStrength / float(config.constipationVisionFadeTick)
            )
        elif self.constipationVisionStrength > self.constipationVisionTargetStrength:
            self.constipationVisionStrength = max(
                self.constipationVisionTargetStrength,
                self.constipationVisionStrength -
                config.constipationVisionMaxStrength / float(config.constipationVisionFadeTick)
            )
        if self.constipationVisionStrength > 0.0:
            # 便秘和低血糖各自持有独立 pass；持续患病时先写强度再恢复被资源重载关闭的横波效果。
            self.postProcessComp.SetParameter(
                config.constipationVisionPostProcess,
                config.constipationVisionStrengthParameter,
                self.constipationVisionStrength
            )
            if (not self.diseaseOwnsConstipationVision or
                    not self.postProcessComp.CheckEnabledByName(config.constipationVisionPostProcess)):
                self.postProcessComp.SetEnableByName(config.constipationVisionPostProcess, True)
                self.diseaseOwnsConstipationVision = True
        elif (self.diseaseOwnsConstipationVision and
              self.constipationVisionTargetStrength <= 0.0):
            # 痊愈或疾病暂停后先完成淡出再关闭 pass，避免横向扭曲突然跳回原画。
            self.postProcessComp.SetParameter(
                config.constipationVisionPostProcess,
                config.constipationVisionStrengthParameter,
                0.0
            )
            self.postProcessComp.SetEnableByName(config.constipationVisionPostProcess, False)
            self.diseaseOwnsConstipationVision = False
        if self.hypoglycemiaVisionStrength < self.hypoglycemiaVisionTargetStrength:
            self.hypoglycemiaVisionStrength = min(
                self.hypoglycemiaVisionTargetStrength,
                self.hypoglycemiaVisionStrength +
                config.hypoglycemiaVisionMaxStrength / float(config.hypoglycemiaVisionFadeTick)
            )
        elif self.hypoglycemiaVisionStrength > self.hypoglycemiaVisionTargetStrength:
            self.hypoglycemiaVisionStrength = max(
                self.hypoglycemiaVisionTargetStrength,
                self.hypoglycemiaVisionStrength -
                config.hypoglycemiaVisionMaxStrength / float(config.hypoglycemiaVisionFadeTick)
            )
        if self.hypoglycemiaVisionStrength > 0.0:
            # 自定义后处理只归疾病模块所有；先写强度再开启，避免默认参数造成一帧强重影。
            self.postProcessComp.SetParameter(
                config.hypoglycemiaVisionPostProcess,
                config.hypoglycemiaVisionStrengthParameter,
                self.hypoglycemiaVisionStrength
            )
            if (not self.diseaseOwnsHypoglycemiaVision or
                    not self.postProcessComp.CheckEnabledByName(config.hypoglycemiaVisionPostProcess)):
                # 资源重载或其他流程关闭效果后，低血糖仍持续时必须在下一 Tick 恢复表现。
                self.postProcessComp.SetEnableByName(config.hypoglycemiaVisionPostProcess, True)
                self.diseaseOwnsHypoglycemiaVision = True
        elif (self.diseaseOwnsHypoglycemiaVision and
              self.hypoglycemiaVisionTargetStrength <= 0.0):
            # 淡出完成后再关闭渲染 pass，确保痊愈过程不会突然跳回清晰画面。
            self.postProcessComp.SetParameter(
                config.hypoglycemiaVisionPostProcess,
                config.hypoglycemiaVisionStrengthParameter,
                0.0
            )
            self.postProcessComp.SetEnableByName(config.hypoglycemiaVisionPostProcess, False)
            self.diseaseOwnsHypoglycemiaVision = False
        if self.ricketsFractureVisionElapsedTick >= 0:
            # 骨折事件先在回调中写入零进度；之后逐 Tick 推进同一段 14 Tick 演出，结束时只关闭自己的 pass。
            self.ricketsFractureVisionElapsedTick += 1
            fractureProgress = min(
                1.0,
                self.ricketsFractureVisionElapsedTick / float(config.ricketsFractureVisionDurationTick)
            )
            self.postProcessComp.SetParameter(
                config.ricketsFracturePostProcess,
                config.ricketsFractureProgressParameter,
                fractureProgress
            )
            if self.ricketsFractureVisionElapsedTick >= config.ricketsFractureVisionDurationTick:
                self.postProcessComp.SetEnableByName(config.ricketsFracturePostProcess, False)
                self.ricketsFractureVisionElapsedTick = -1
                self.diseaseOwnsRicketsFractureVision = False
            elif (not self.diseaseOwnsRicketsFractureVision or
                  not self.postProcessComp.CheckEnabledByName(config.ricketsFracturePostProcess)):
                # 短演出期间若资源重载关闭了 pass，下一 Tick 继续当前进度，避免连带重启低血糖效果。
                self.postProcessComp.SetEnableByName(config.ricketsFracturePostProcess, True)
                self.postProcessComp.SetParameter(
                    config.ricketsFracturePostProcess,
                    config.ricketsFractureProgressParameter,
                    fractureProgress
                )
                self.postProcessComp.SetParameter(
                    config.ricketsFracturePostProcess,
                    config.ricketsFractureAspectRatioParameter,
                    self.ricketsFractureAspectRatio
                )
                self.diseaseOwnsRicketsFractureVision = True

    def DiseaseSyncData(self, args):
        active = args['active']
        activeCount = args['activeCount']
        maxActiveCount = args['maxActiveCount']
        validEatCount = args['validEatCount']
        constipationSquatCount = args['constipationSquatCount']
        self.diseaseData = {
            'active': active,
            'activeCount': activeCount,
            'maxActiveCount': maxActiveCount,
            'validEatCount': validEatCount,
            'constipationSquatCount': constipationSquatCount
        }
        self.activeDiseaseIds = {}
        constipationSeconds = -1
        hypoglycemiaSeconds = -1
        for diseaseData in active:
            diseaseId = diseaseData['id']
            self.activeDiseaseIds[diseaseId] = True
            if diseaseId == 'constipation':
                constipationSeconds = diseaseData['activeSeconds']
            elif diseaseId == 'hypoglycemia':
                hypoglycemiaSeconds = diseaseData['activeSeconds']
        if constipationSeconds >= 0:
            growRatio = min(1.0, constipationSeconds / config.constipationVisionGrowSeconds)
            reliefRatio = 1.0 - constipationSquatCount / float(config.constipationSquatRequired)
            self.constipationVisionTargetStrength = (
                config.constipationVisionInitialStrength + growRatio *
                (config.constipationVisionMaxStrength - config.constipationVisionInitialStrength)
            ) * reliefRatio
        else:
            self.constipationVisionTargetStrength = 0.0
        if hypoglycemiaSeconds >= config.hypoglycemiaLateSeconds:
            growRatio = min(
                1.0,
                (hypoglycemiaSeconds - config.hypoglycemiaLateSeconds) / config.hypoglycemiaVisionGrowSeconds
            )
            self.hypoglycemiaVisionTargetStrength = (
                config.hypoglycemiaVisionInitialStrength + growRatio *
                (config.hypoglycemiaVisionMaxStrength - config.hypoglycemiaVisionInitialStrength)
            )
        else:
            self.hypoglycemiaVisionTargetStrength = 0.0
        if 'rickets' not in self.activeDiseaseIds and self.diseaseOwnsRicketsFractureVision:
            # 痊愈或疾病总开关关闭时立即收掉一次性骨折演出，不触碰仍由低血糖持有的后处理。
            self.postProcessComp.SetParameter(
                config.ricketsFracturePostProcess,
                config.ricketsFractureProgressParameter,
                1.0
            )
            self.postProcessComp.SetEnableByName(config.ricketsFracturePostProcess, False)
            self.ricketsFractureVisionElapsedTick = -1
            self.diseaseOwnsRicketsFractureVision = False
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
        symptomId = args['symptomId']
        sound = args['sound']
        volume = args['volume']
        pitch = args['pitch']
        if symptomId == config.ricketsFractureSymptom:
            screenWidth, screenHeight = compGame.GetScreenSize()
            aspectRatio = min(3.0, max(0.5, float(screenWidth) / float(screenHeight)))
            # 先重置进度和宽高比再开启 pass，确保首次触发和冷却后的重复触发都从白闪首帧开始。
            self.ricketsFractureVisionElapsedTick = 0
            self.ricketsFractureAspectRatio = aspectRatio
            self.postProcessComp.SetParameter(
                config.ricketsFracturePostProcess,
                config.ricketsFractureProgressParameter,
                0.0
            )
            self.postProcessComp.SetParameter(
                config.ricketsFracturePostProcess,
                config.ricketsFractureAspectRatioParameter,
                aspectRatio
            )
            if (not self.diseaseOwnsRicketsFractureVision or
                    not self.postProcessComp.CheckEnabledByName(config.ricketsFracturePostProcess)):
                self.postProcessComp.SetEnableByName(config.ricketsFracturePostProcess, True)
                # 网易 3.9 首次激活 pass 会恢复 JSON 默认参数，开启后重写才能保住本机屏幕比例和零进度首帧。
                self.postProcessComp.SetParameter(
                    config.ricketsFracturePostProcess,
                    config.ricketsFractureProgressParameter,
                    0.0
                )
                self.postProcessComp.SetParameter(
                    config.ricketsFracturePostProcess,
                    config.ricketsFractureAspectRatioParameter,
                    aspectRatio
                )
            self.diseaseOwnsRicketsFractureVision = True
        playerId = clientApi.GetLocalPlayerId()
        customAudioComp = compFactory.CreateCustomAudio(levelId)
        customAudioComp.PlayCustomMusic(sound, (0, 0, 0), volume, pitch, False, playerId)

    def Destroy(self):
        for playerId in self.injectedPlayers:
            queryVariableComp = compFactory.CreateQueryVariable(playerId)
            queryVariableComp.Set(config.bodyScaleQuery, 1.0)
            queryVariableComp.Set(config.headScaleQuery, 1.0)
        if self.diseaseOwnsConstipationVision:
            self.postProcessComp.SetParameter(
                config.constipationVisionPostProcess,
                config.constipationVisionStrengthParameter,
                0.0
            )
            self.postProcessComp.SetEnableByName(config.constipationVisionPostProcess, False)
            self.diseaseOwnsConstipationVision = False
        if self.diseaseOwnsHypoglycemiaVision:
            self.postProcessComp.SetParameter(
                config.hypoglycemiaVisionPostProcess,
                config.hypoglycemiaVisionStrengthParameter,
                0.0
            )
            self.postProcessComp.SetEnableByName(config.hypoglycemiaVisionPostProcess, False)
            self.diseaseOwnsHypoglycemiaVision = False
        if self.diseaseOwnsRicketsFractureVision:
            self.postProcessComp.SetParameter(
                config.ricketsFracturePostProcess,
                config.ricketsFractureProgressParameter,
                1.0
            )
            self.postProcessComp.SetEnableByName(config.ricketsFracturePostProcess, False)
            self.ricketsFractureVisionElapsedTick = -1
            self.diseaseOwnsRicketsFractureVision = False
