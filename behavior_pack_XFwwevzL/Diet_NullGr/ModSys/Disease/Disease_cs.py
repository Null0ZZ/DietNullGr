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
        self.visionStrengths = dict.fromkeys(config.visionFadeSettings, 0.0)
        self.visionTargetStrengths = self.visionStrengths.copy()
        self.enabledVisionPostProcesses = set()
        self.unavailableVisionPostProcesses = set()
        self.ricketsFractureVisionElapsedTick = -1
        self.ricketsFractureAspectRatio = 1.0
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
        # 重进存档后资源可能已恢复，允许此前失败的症状在需要时重新注册。
        self.unavailableVisionPostProcesses.clear()
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
        for postProcessName, (strengthParameter, fadeStep) in config.visionFadeSettings.items():
            previousStrength = self.visionStrengths[postProcessName]
            targetStrength = self.visionTargetStrengths[postProcessName]
            strength = previousStrength
            if strength < targetStrength:
                strength = min(targetStrength, strength + fadeStep)
            elif strength > targetStrength:
                strength = max(targetStrength, strength - fadeStep)
            self.visionStrengths[postProcessName] = strength
            if strength > 0.0:
                # 首个渐入帧才注册并开启效果，资源重载后用当前强度恢复。
                self._updateVisionPostProcess(postProcessName, ((strengthParameter, strength),))
            elif previousStrength > 0.0:
                # 淡出完成后关闭本模组的 pass，下次发作可以重新尝试。
                self._stopVisionPostProcess(postProcessName)

        if self.ricketsFractureVisionElapsedTick >= 0:
            # 骨折事件注册并写入零进度，此处只推进同一次演出并在结束时收掉。
            self.ricketsFractureVisionElapsedTick += 1
            if self.ricketsFractureVisionElapsedTick >= config.ricketsFractureVisionDurationTick:
                self._stopVisionPostProcess(config.ricketsFracturePostProcess)
                self.ricketsFractureVisionElapsedTick = -1
            else:
                progress = self.ricketsFractureVisionElapsedTick / float(config.ricketsFractureVisionDurationTick)
                if not self._updateVisionPostProcess(config.ricketsFracturePostProcess, (
                    (config.ricketsFractureProgressParameter, progress),
                    (config.ricketsFractureAspectRatioParameter, self.ricketsFractureAspectRatio)
                )):
                    self.ricketsFractureVisionElapsedTick = -1

    # 首次需要或渲染队列重建时补注册，再按症状写入本帧参数。
    def _updateVisionPostProcess(self, postProcessName, parameters):
        if postProcessName in self.unavailableVisionPostProcesses:
            return False
        if (postProcessName not in self.enabledVisionPostProcesses or
                not self.postProcessComp.CheckEnabledByName(postProcessName)):
            self.enabledVisionPostProcesses.discard(postProcessName)
            renderOrder = self.postProcessComp.GetPostProcessOrder()
            if not renderOrder or postProcessName not in renderOrder:
                # 默认追加到现有队列末尾。已有顺序更靠后的疾病效果时插在它前面，
                # 使骨折等演出保持原先的相对顺序，同时保留其他包条目的顺序。
                visionIndex = config.visionPostProcessOrder.index(postProcessName)
                laterVisionNames = config.visionPostProcessOrder[visionIndex + 1:]
                insertIndex = next((index for index, registeredName in enumerate(renderOrder or ())
                                    if registeredName in laterVisionNames), -1)
                if not self.postProcessComp.AddPostProcess(
                    config.visionPostProcessDefinitions[visionIndex], insertIndex
                ):
                    self.unavailableVisionPostProcesses.add(postProcessName)
                    print("[DietNullGr] 疾病后处理 {} 注册失败".format(postProcessName))
                    return False
            if not self.postProcessComp.SetEnableByName(postProcessName, True):
                self.unavailableVisionPostProcesses.add(postProcessName)
                print("[DietNullGr] 疾病后处理 {} 开启失败".format(postProcessName))
                return False
            self.enabledVisionPostProcesses.add(postProcessName)

        # 网易 3.9 开启 pass 会恢复默认参数，开启和写入放在同一回调内完成。
        for parameter, value in parameters:
            if not self.postProcessComp.SetParameter(postProcessName, parameter, value):
                # 参数写入失败时先撤销已开启的 pass，同一症状期间不再逐 Tick 重试。
                self._stopVisionPostProcess(postProcessName)
                self.unavailableVisionPostProcesses.add(postProcessName)
                print("[DietNullGr] 疾病后处理 {} 写入参数 {} 失败".format(postProcessName, parameter))
                return False
        return True

    # 结束本次症状时只关闭由疾病系统开启的效果，并清除本次失败记录。
    def _stopVisionPostProcess(self, postProcessName):
        if postProcessName in self.enabledVisionPostProcesses:
            self.postProcessComp.SetEnableByName(postProcessName, False)
            self.enabledVisionPostProcesses.remove(postProcessName)
        self.unavailableVisionPostProcesses.discard(postProcessName)

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
            self.visionTargetStrengths[config.constipationVisionPostProcess] = (
                config.constipationVisionInitialStrength + growRatio *
                (config.constipationVisionMaxStrength - config.constipationVisionInitialStrength)
            ) * reliefRatio
        else:
            self.visionTargetStrengths[config.constipationVisionPostProcess] = 0.0
        self.visionTargetStrengths[config.feverVisionPostProcess] = (
            config.feverVisionMaxStrength if 'fever' in self.activeDiseaseIds else 0.0
        )
        if hypoglycemiaSeconds >= config.hypoglycemiaLateSeconds:
            growRatio = min(
                1.0,
                (hypoglycemiaSeconds - config.hypoglycemiaLateSeconds) / config.hypoglycemiaVisionGrowSeconds
            )
            self.visionTargetStrengths[config.hypoglycemiaVisionPostProcess] = (
                config.hypoglycemiaVisionInitialStrength + growRatio *
                (config.hypoglycemiaVisionMaxStrength - config.hypoglycemiaVisionInitialStrength)
            )
        else:
            self.visionTargetStrengths[config.hypoglycemiaVisionPostProcess] = 0.0
        if 'rickets' not in self.activeDiseaseIds and self.ricketsFractureVisionElapsedTick >= 0:
            # 痊愈或停用疾病时中止一次性骨折演出，其余持续症状按各自强度淡出。
            self._stopVisionPostProcess(config.ricketsFracturePostProcess)
            self.ricketsFractureVisionElapsedTick = -1
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
            self.ricketsFractureAspectRatio = min(3.0, max(0.5, float(screenWidth) / float(screenHeight)))
            postProcessName = config.ricketsFracturePostProcess
            # 每次新的骨折事件从白闪首帧开始，进度由客户端 Tick 接续推进。
            self.unavailableVisionPostProcesses.discard(postProcessName)
            started = self._updateVisionPostProcess(postProcessName, (
                (config.ricketsFractureProgressParameter, 0.0),
                (config.ricketsFractureAspectRatioParameter, self.ricketsFractureAspectRatio)
            ))
            self.ricketsFractureVisionElapsedTick = 0 if started else -1
        playerId = clientApi.GetLocalPlayerId()
        customAudioComp = compFactory.CreateCustomAudio(levelId)
        customAudioComp.PlayCustomMusic(sound, (0, 0, 0), volume, pitch, False, playerId)

    def Destroy(self):
        for playerId in self.injectedPlayers:
            queryVariableComp = compFactory.CreateQueryVariable(playerId)
            queryVariableComp.Set(config.bodyScaleQuery, 1.0)
            queryVariableComp.Set(config.headScaleQuery, 1.0)
        for postProcessName in tuple(self.enabledVisionPostProcesses):
            self._stopVisionPostProcess(postProcessName)
        self.ricketsFractureVisionElapsedTick = -1
