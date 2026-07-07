# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.ModSys.Diet.config as config

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
                'tracked': True
            })
        self.dietData = {'active': True, 'groups': defaultGroups, 'effectsText': '当前没有饮食效果'}
        self.itemAuxCache = {}
        compFactory = clientApi.GetEngineCompFactory()
        self.itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        if param:
            self.dietData = param['dietData']

    def Create(self):
        self.UpdateScreen(True)

    def Creat(self):
        self.Create()

    # 服务端同步只更新绑定数据源，控件树路径变化不会影响面板刷新。
    def UpdateDietData(self, data):
        self.dietData = data
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

    @ViewBinder.binding(ViewBinder.BF_BindString, "#diet_screen.effects")
    def bindEffectsText(self):
        return self.dietData['effectsText']

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
        if self.getGroupData(index)['tracked']:
            return self.getGroupDisplayColor(index)
        return (0.48, 0.48, 0.48)

    @ViewBinder.binding_collection(ViewBinder.BF_BindString, "diet_rows", "#diet_screen.row_tooltip")
    def bindRowTooltip(self, index):
        return self.getGroupData(index)['tooltip']

    @ViewBinder.binding_collection(ViewBinder.BF_BindColor, "diet_rows", "#diet_screen.row_tooltip_color")
    def bindRowTooltipColor(self, index):
        if self.getGroupData(index)['tracked']:
            return (0.62, 0.6, 0.56)
        return (0.42, 0.42, 0.42)

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
        if self.getGroupData(index)['tracked']:
            return self.getGroupDisplayColor(index)
        return (0.22, 0.22, 0.22)

    @ViewBinder.binding_collection(ViewBinder.BF_BindFloat, "diet_rows", "#diet_screen.row_bar_clip")
    def bindRowBarClip(self, index):
        groupData = self.getGroupData(index)
        if groupData['tracked']:
            return 1.0 - groupData['value']
        return 1.0
