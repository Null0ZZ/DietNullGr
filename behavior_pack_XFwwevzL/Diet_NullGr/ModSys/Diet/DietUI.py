# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Disease.config as diseaseConfig

ScreenNode = clientApi.GetScreenNodeCls()
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()


class DietUI(ScreenNode):
    def __init__(self, namespace, uiKey, param):
        ScreenNode.__init__(self, namespace, uiKey, param)
        defaultGroups = []
        for groupId in config.groupOrder:
            groupConfig = config.groups[groupId]
            defaultGroups.append({
                'id': groupId,
                'name': groupConfig['name'],
                'tooltip': groupConfig['tooltip'],
                'icon': groupConfig['icon'],
                'color': groupConfig['color'],
                'value': groupConfig['defaultValue'],
                'tracked': True,
                'diseaseRelated': False
            })
        self.dietData = {'active': True, 'groups': defaultGroups}
        self.diseaseData = {'active': []}
        self.emptyDiseaseData = {
            'id': '',
            'name': '',
            'icon': '',
            'durationText': '',
            'progressText': '',
            'symptom': '',
            'cause': '',
            'relief': '',
            'groups': []
        }
        self.itemAuxCache = {}
        compFactory = clientApi.GetEngineCompFactory()
        self.itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        if param:
            self.dietData = param['dietData']

    def Create(self):
        # 疾病同步可能早于面板创建，打开面板时必须先接回疾病客户端系统保存的最新快照。
        diseaseClientSys = clientApi.GetSystem(com.modName, diseaseConfig.csname)
        if diseaseClientSys and diseaseClientSys.diseaseData is not None:
            self.diseaseData = diseaseClientSys.diseaseData
        self.refreshDiseaseGroupFlags()
        self.UpdateScreen(True)

    def Creat(self):
        self.Create()

    # 服务端同步只更新绑定数据源，控件树路径变化不会影响面板刷新。
    def UpdateDietData(self, data):
        self.dietData = data
        self.refreshDiseaseGroupFlags()
        self.UpdateScreen(True)

    # 疾病变化与营养变化使用独立同步事件，面板打开期间由疾病客户端系统直接刷新此数据源。
    def UpdateDiseaseData(self, data):
        self.diseaseData = data
        self.refreshDiseaseGroupFlags()
        self.UpdateScreen(True)

    # 关闭按钮通过绑定事件弹出 PushScreen 栈，避免控件路径变化导致回调注册失败。
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#diet_screen.close")
    def CloseDietScreen(self, args):
        clientApi.PopScreen()
        return ViewRequest.Nothing

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.title")
    def bindTitle(self):
        if self.dietData['active']:
            return '均衡饮食'
        return '均衡饮食（已暂停）'

    @ViewBinder.binding(ViewBinder.BF_BindColor, "#diet_screen.title_color")
    def bindTitleColor(self):
        if self.dietData['active']:
            return (0.96, 0.94, 0.86)
        return (0.78, 0.78, 0.78)

    # 多个行绑定都按集合索引读取同一份同步数据，集中入口能保证字段来源一致。
    def getGroupData(self, index):
        return self.dietData['groups'][index]

    # item_renderer 的绑定只能写 id_aux，缓存组件查询结果避免每次绑定刷新重复查。
    def getItemAux(self, itemId):
        if itemId in self.itemAuxCache:
            return self.itemAuxCache[itemId]
        itemInfo = self.itemComp.GetItemBasicInfo(itemId)
        if itemInfo:
            self.itemAuxCache[itemId] = itemInfo['id_aux']
        else:
            self.itemAuxCache[itemId] = 131072
        return self.itemAuxCache[itemId]

    # 配置颜色是 0-255 整数，UI 绑定颜色需要 0-1 浮点值。
    def getGroupDisplayColor(self, index):
        color = self.getGroupData(index)['color']
        return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)

    # 疾病同步先把关联组压成营养行标量，绑定刷新时不再跨读第二套集合数据。
    def refreshDiseaseGroupFlags(self):
        diseaseGroups = {}
        for diseaseData in self.diseaseData['active']:
            for groupId in diseaseData['groups']:
                diseaseGroups[groupId] = True
        for groupData in self.dietData['groups']:
            groupData['diseaseRelated'] = groupData['id'] in diseaseGroups

    # 百分比颜色沿用旧面板阈值，绑定刷新和原手动刷新表现保持一致。
    def getPercentColor(self, progress):
        if progress >= 0.75:
            return config.percentColorHealthy
        if progress >= 0.5:
            return config.percentColorCaution
        if progress >= 0.25:
            return config.percentColorWarning
        return config.percentColorDanger

    @ViewBinder.binding_collection(ViewBinder.BF_BindInt, "diet_rows", "#diet_screen.row_icon_aux")
    def bindRowIconAux(self, index):
        return self.getItemAux(self.getGroupData(index)['icon'])

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "diet_rows", "#diet_screen.row_name")
    def bindRowName(self, index):
        return self.getGroupData(index)['name']

    @ViewBinder.binding_collection(ViewBinder.BF_BindColor, "diet_rows", "#diet_screen.row_name_color")
    def bindRowNameColor(self, index):
        groupData = self.getGroupData(index)
        if not groupData['tracked']:
            return (0.48, 0.48, 0.48)
        if groupData['diseaseRelated']:
            return config.diseaseGroupHighlightColor
        return self.getGroupDisplayColor(index)

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "diet_rows", "#diet_screen.row_tooltip")
    def bindRowTooltip(self, index):
        return self.getGroupData(index)['tooltip']

    @ViewBinder.binding_collection(ViewBinder.BF_BindColor, "diet_rows", "#diet_screen.row_tooltip_color")
    def bindRowTooltipColor(self, index):
        groupData = self.getGroupData(index)
        if not groupData['tracked']:
            return (0.42, 0.42, 0.42)
        if groupData['diseaseRelated']:
            return config.diseaseGroupTooltipColor
        return (0.62, 0.6, 0.56)

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "diet_rows", "#diet_screen.row_percent")
    def bindRowPercent(self, index):
        groupData = self.getGroupData(index)
        if groupData['tracked']:
            return str(int(groupData['value'] * 100.0)) + '%'
        return '关闭'

    @ViewBinder.binding_collection(ViewBinder.BF_BindColor, "diet_rows", "#diet_screen.row_percent_color")
    def bindRowPercentColor(self, index):
        groupData = self.getGroupData(index)
        if groupData['tracked']:
            return self.getPercentColor(groupData['value'])
        return (0.56, 0.56, 0.56)

    @ViewBinder.binding_collection(ViewBinder.BF_BindColor, "diet_rows", "#diet_screen.row_bar_color")
    def bindRowBarColor(self, index):
        groupData = self.getGroupData(index)
        if not groupData['tracked']:
            return (0.22, 0.22, 0.22)
        if groupData['diseaseRelated']:
            return config.diseaseGroupHighlightColor
        return self.getGroupDisplayColor(index)

    @ViewBinder.binding_collection(ViewBinder.BF_BindFloat, "diet_rows", "#diet_screen.row_bar_clip")
    def bindRowBarClip(self, index):
        groupData = self.getGroupData(index)
        if groupData['tracked']:
            return 1.0 - groupData['value']
        return 1.0

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#diet_screen.disease_healthy_visible")
    def bindDiseaseHealthyVisible(self):
        return len(self.diseaseData['active']) == 0

    # 疾病最多同时两种，两个固定标量卡槽可避开同屏多集合刷新时的引擎类型错误。
    def getDiseaseData(self, index):
        if index < len(self.diseaseData['active']):
            return self.diseaseData['active'][index]
        return self.emptyDiseaseData

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#diet_screen.disease_slot_0_visible")
    def bindDiseaseSlot0Visible(self):
        return len(self.diseaseData['active']) > 0

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_0_icon")
    def bindDiseaseSlot0Icon(self):
        return self.getDiseaseData(0)['icon']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_0_name")
    def bindDiseaseSlot0Name(self):
        return self.getDiseaseData(0)['name']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_0_duration")
    def bindDiseaseSlot0Duration(self):
        return self.getDiseaseData(0)['durationText']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_0_progress")
    def bindDiseaseSlot0Progress(self):
        return self.getDiseaseData(0)['progressText']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_0_symptom")
    def bindDiseaseSlot0Symptom(self):
        return "症状：" + self.getDiseaseData(0)['symptom']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_0_cause")
    def bindDiseaseSlot0Cause(self):
        return "病因：" + self.getDiseaseData(0)['cause']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_0_relief")
    def bindDiseaseSlot0Relief(self):
        return "缓解：" + self.getDiseaseData(0)['relief']

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#diet_screen.disease_slot_1_visible")
    def bindDiseaseSlot1Visible(self):
        return len(self.diseaseData['active']) > 1

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_1_icon")
    def bindDiseaseSlot1Icon(self):
        return self.getDiseaseData(1)['icon']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_1_name")
    def bindDiseaseSlot1Name(self):
        return self.getDiseaseData(1)['name']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_1_duration")
    def bindDiseaseSlot1Duration(self):
        return self.getDiseaseData(1)['durationText']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_1_progress")
    def bindDiseaseSlot1Progress(self):
        return self.getDiseaseData(1)['progressText']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_1_symptom")
    def bindDiseaseSlot1Symptom(self):
        return "症状：" + self.getDiseaseData(1)['symptom']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_1_cause")
    def bindDiseaseSlot1Cause(self):
        return "病因：" + self.getDiseaseData(1)['cause']

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.disease_slot_1_relief")
    def bindDiseaseSlot1Relief(self):
        return "缓解：" + self.getDiseaseData(1)['relief']
