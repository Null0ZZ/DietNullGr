# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.ModSys.Diet.config as config

ScreenNode = clientApi.GetScreenNodeCls()


class DietUI(ScreenNode):
    def __init__(self, namespace, uiKey, param):
        ScreenNode.__init__(self, namespace, uiKey, param)
        if param:
            self.dietData = param['dietData']
        else:
            self.dietData = {'active': True, 'groups': [], 'effectsText': '当前没有饮食效果'}

    def Create(self):
        closeButton = self.GetBaseUIControl('/root/close_button').asButton()
        closeButton.AddTouchEventParams({"isSwallow": True})
        closeButton.SetButtonTouchUpCallback(self.CloseDietScreen)
        self.UpdateDietData(self.dietData)

    def Creat(self):
        self.Create()

    # 关闭按钮必须通过 PushScreen 栈弹出，避免残留 UI 节点阻塞后续打开。
    def CloseDietScreen(self, args):
        clientApi.PopScreen()

    # 服务端同步后刷新整张面板，所有控件路径固定，避免动态创建 UI 导致控件树不可审查。
    def UpdateDietData(self, data):
        self.dietData = data
        titleLabel = self.GetBaseUIControl('/root/title').asLabel()
        if data['active']:
            titleLabel.SetText('均衡饮食')
            titleLabel.SetTextColor((0.96, 0.94, 0.86))
        else:
            titleLabel.SetText('均衡饮食（已暂停）')
            titleLabel.SetTextColor((0.78, 0.78, 0.78))
        effectLabel = self.GetBaseUIControl('/root/effects').asLabel()
        effectLabel.SetText(data['effectsText'])
        groups = data['groups']
        for index in range(0, len(config.groupOrder)):
            groupData = groups[index]
            rowPath = '/root/row{}'.format(index)
            itemRenderer = self.GetBaseUIControl(rowPath + '/icon').asItemRenderer()
            nameLabel = self.GetBaseUIControl('/root/row_name{}'.format(index)).asLabel()
            percentLabel = self.GetBaseUIControl('/root/row_percent{}'.format(index)).asLabel()
            barFill = self.GetBaseUIControl(rowPath + '/bar_fill').asImage()
            color = groupData['color']
            progress = groupData['value']
            itemRenderer.SetUiItem(groupData['icon'], 0)
            nameLabel.SetText(groupData['name'])
            percentLabel.SetText('{}%%'.format(int(progress * 100.0)))
            nameLabel.SetTextColor((color[0] / 255.0, color[1] / 255.0, color[2] / 255.0))
            barFill.SetSpriteColor((color[0] / 255.0, color[1] / 255.0, color[2] / 255.0))
            barFill.SetSpriteClipRatio(1.0 - progress)
