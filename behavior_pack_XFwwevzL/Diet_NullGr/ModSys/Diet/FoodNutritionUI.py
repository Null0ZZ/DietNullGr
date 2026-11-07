# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com
import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Diet.FoodNutrition as FoodNutrition

ScreenNode = clientApi.GetScreenNodeCls()
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()

# 原版 base_screen 把自定义内容挂在安全区内，动态控件必须从实际挂载路径查找。
viewportPath = ('/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix'
                '/safezone_screen_panel/root_screen_panel/viewport')
windowPath = viewportPath + '/window'
confirmPath = viewportPath + '/confirm'
inkColor = (0.20, 0.16, 0.13)
selectedColor = (1.0, 0.98, 0.94)
statusNames = {'pending': '未设置', 'auto': '自动计算', 'manual': '已自定义'}
writeMessages = {
    'permission': '编辑权限已变更，当前为只读',
    'conflict': '其他管理员已修改这份规则，请核对后再保存',
    'invalid': '食物或营养数值无效',
    'storage': '世界存档写入失败，请重试',
    'timeout': '暂未确认保存结果，请重试'
}


class FoodNutritionUI(ScreenNode):
    def __init__(self, namespace, uiKey, param):
        ScreenNode.__init__(self, namespace, uiKey, param)
        self.clientSystem = clientApi.GetSystem(com.modName, com.csname)
        compFactory = clientApi.GetEngineCompFactory()
        levelId = clientApi.GetLevelId()
        self.itemComp = compFactory.CreateItem(levelId)
        self.gameComp = compFactory.CreateGame(levelId)
        self.controls = {}
        self.groupRows = []
        self.tiles = []
        self.namespaceRowCounts = {}
        self.entries = {}
        self.itemNames = []
        self.representatives = {}
        self.catalogChunks = {}
        self.earlyChanges = {}
        self.indexing = None
        self.catalogReady = False
        self.keyword = ''
        self.showConfigured = False
        self.selectedNamespace = ''
        self.namespaces = []
        self.page = 0
        self.pageCount = 1
        self.visibleFoods = []
        self.matches = []
        self.canEdit = False
        self.selectedItem = None
        self.detail = None
        self.initialUnits = []
        self.restorePending = False
        self.confirmTarget = None
        self.pendingWrite = None
        self.request = None
        self.requestTimer = None
        self.closed = False

    def Create(self):
        if self.controls:
            return
        self.clientSystem.foodNutritionNode = self
        for path in (
                'title', 'back', 'close', 'catalog', 'catalog/search', 'catalog/clear', 'catalog/pending',
                'catalog/configured', 'catalog/matchCount', 'catalog/namespaceTitle', 'catalog/namespaceBackground',
                'catalog/all', 'catalog/namespaceScroll', 'catalog/tiles', 'catalog/notice', 'catalog/retry',
                'catalog/page', 'catalog/previous', 'catalog/next', 'detail', 'detail/itemBackground',
                'detail/itemIcon', 'detail/itemName', 'detail/itemStatus', 'detail/source', 'detail/columnTitle',
                'detail/feedback', 'detail/scope', 'detail/restore', 'detail/save'):
            self.controls[path] = self.GetBaseUIControl(windowPath + '/' + path)
        for path in ('back', 'close'):
            self._bindButton(self.controls[path], self.Navigate)
        for name in ('clear', 'pending', 'configured', 'all', 'retry', 'previous', 'next'):
            self._bindButton(self.controls['catalog/' + name], self.CatalogAction)
        for name in ('restore', 'save'):
            self._bindButton(self.controls['detail/' + name], self.DetailAction)
        for name in ('stay', 'discard', 'save'):
            self._bindButton(self.GetBaseUIControl(confirmPath + '/box/' + name), self.ConfirmAction)

        for index, groupId in enumerate(config.groupOrder):
            path = windowPath + '/detail/group' + str(index)
            row = {name: self.GetBaseUIControl(path + '/' + name)
                   for name in ('icon', 'group', 'minus', 'value', 'readOnly', 'plus')}
            row['panel'] = self.GetBaseUIControl(path)
            group = config.groups[groupId]
            info = self.itemComp.GetItemBasicInfo(group['icon'], 0)
            row['icon'].SetPropertyBag({'#item_id_aux': info['id_aux']})
            row['group'].asLabel().SetText(group['name'])
            self._bindButton(row['minus'], self.DetailAction)
            self._bindButton(row['plus'], self.DetailAction)
            self.groupRows.append(row)

        for index in range(12):
            name = 'tile' + str(index)
            button = self.CreateChildControl('food_nutrition.foodTile', name, self.controls['catalog/tiles'], False)
            path = windowPath + '/catalog/tiles/' + name
            self._bindButton(button, self.SelectFood)
            self.tiles.append((button, self.GetBaseUIControl(path + '/icon'), self.GetBaseUIControl(path + '/name')))
            button.SetVisible(False)
        self.RefreshLayout()
        self._requestCatalog()

    def Creat(self):
        self.Create()

    def OnActive(self):
        if self.catalogReady and self.selectedItem is None:
            self._refreshCatalog()

    def Destroy(self):
        self.closed = True
        self._finishRequest()
        if self.indexing is not None:
            clientApi.StopCoroutine(self.indexing)
            self.indexing = None
        if self.clientSystem.foodNutritionNode is self:
            self.clientSystem.foodNutritionNode = None

    # 动态物品格和命名空间行与固定按钮走同一套触摸回调，点击仅在抬手时提交。
    def _bindButton(self, control, callback):
        button = control.asButton()
        button.AddTouchEventParams({'isSwallow': True})
        button.SetButtonTouchUpCallback(callback)

    # 按实际 UI 单位计算列数和行数，窄屏保留可点击的物品格和独立分类栏。
    def RefreshLayout(self):
        if self.closed or not self.controls:
            return
        viewportWidth, viewportHeight = self.GetBaseUIControl(viewportPath).GetSize()
        width = min(332, max(178, int(viewportWidth) - 12)) if viewportWidth else 332
        height = min(222, max(177, int(viewportHeight) - 12)) if viewportHeight else 222
        self.GetBaseUIControl(windowPath).SetSize((width, height), True)
        rightWidth = 99 if width >= 277 else max(66, width * 35 // 100)
        gridWidth = width - rightWidth - 25
        gridHeight = height - 99
        right = gridWidth + 16
        self.columns = min(4, max(2, (gridWidth + 4) // 48))
        self.rows = min(3, max(1, (gridHeight + 4) // 33))
        self.tileWidth = (gridWidth - (self.columns - 1) * 4) // self.columns
        self.tileHeight = (gridHeight - (self.rows - 1) * 4) // self.rows
        self.namespaceWidth = rightWidth - 5
        tabWidth = min(45, (gridWidth - 28) // 2)
        rowTop = 80
        rowHeight = min(19, (height - rowTop - 42) // 5)
        positions = (
            ('catalog/search', 9, 27, width - 38, 18),
            ('catalog/clear', width - 26, 27, 17, 18),
            ('catalog/pending', 9, 50, tabWidth, 17),
            ('catalog/configured', 12 + tabWidth, 50, tabWidth, 17),
            ('catalog/matchCount', 16 + tabWidth * 2, 50, max(21, gridWidth - tabWidth * 2 - 7), 17),
            ('catalog/namespaceTitle', right + 1, 50, rightWidth - 4, 17),
            ('catalog/namespaceBackground', right, 70, rightWidth, gridHeight),
            ('catalog/all', right + 2, 72, self.namespaceWidth, 19),
            ('catalog/namespaceScroll', right + 2, 93, self.namespaceWidth, max(13, gridHeight - 25)),
            ('catalog/tiles', 9, 70, gridWidth, gridHeight),
            ('catalog/notice', 9, 72 + max(0, gridHeight // 2 - 18), gridWidth, 24),
            ('catalog/retry', 9 + max(0, (gridWidth - 54) // 2), 70 + gridHeight // 2 + 9, 54, 17),
            ('catalog/page', 9, height - 24, max(33, gridWidth - 41), 18),
            ('catalog/previous', gridWidth - 29, height - 24, 18, 18),
            ('catalog/next', gridWidth - 9, height - 24, 18, 18),
            ('detail/itemBackground', 9, 26, width - 18, 29),
            ('detail/itemName', 42, 27, width - 52, 14),
            ('detail/itemStatus', 42, 40, width - 52, 13),
            ('detail/source', 9, 55, width - 18, 12),
            ('detail/columnTitle', 9, rowTop - 13, width - 18, 12),
            ('detail/feedback', 9, height - 42, width - 18, 16),
            ('detail/scope', 9, height - 25, max(52, width - 133), 18)
        )
        for path, x, y, controlWidth, controlHeight in positions:
            self.controls[path].SetPosition((x, y))
            self.controls[path].SetSize((controlWidth, controlHeight), True)
        for index, row in enumerate(self.groupRows):
            row['panel'].SetPosition((9, rowTop + index * rowHeight))
            row['panel'].SetSize((width - 18, rowHeight - 1), True)
            iconSize = min(16, rowHeight - 2)
            row['icon'].SetSize((iconSize, iconSize))
        if self.catalogReady and self.selectedItem is None:
            self._refreshCatalog()
        else:
            self.UpdateScreen(True)

    # 单个界面同时只等待一种请求；客户端系统分配跨开关界面不重复的编号。
    def _sendRequest(self, event, values, timeout=8.0):
        self._finishRequest()
        self.clientSystem.foodNutritionRequestId += 1
        requestId = self.clientSystem.foodNutritionRequestId
        self.request = (event, requestId)
        values['requestId'] = requestId
        self.requestTimer = self.gameComp.AddTimer(timeout, self.RequestExpired, requestId)
        self.clientSystem.NotifyToServer(event, values)

    # 完成、关闭或发起新请求时取消旧计时器，迟到回包按请求编号丢弃。
    def _finishRequest(self):
        if self.requestTimer is not None:
            self.gameComp.CancelTimer(self.requestTimer)
            self.requestTimer = None
        self.request = None

    # 清单失败可在原界面重试；等待分片和物品名称索引期间保持加载提示。
    def _requestCatalog(self):
        self.catalogChunks.clear()
        self.controls['catalog/retry'].SetVisible(False)
        self.controls['catalog/notice'].SetVisible(True)
        self.controls['catalog/notice'].asLabel().SetText('正在读取世界食物…')
        self._sendRequest(config.foodCatalogRequest, {}, 20.0)

    # 保存超时不能推断服务端失败，先读回当前单项规则再决定是否保留草稿。
    def RequestExpired(self, requestId):
        if self.closed or self.request is None or requestId != self.request[1]:
            return
        event = self.request[0]
        self.requestTimer = None
        self.request = None
        if event == config.foodCatalogRequest:
            self.controls['catalog/notice'].asLabel().SetText('目录读取超时，请重试')
            self.controls['catalog/retry'].SetVisible(True)
        elif event == config.foodRuleRequest:
            self.controls['detail/feedback'].asLabel().SetText('正在确认保存结果…')
            self._sendRequest(config.foodDetailRequest, {'itemName': self.selectedItem})
        elif self.pendingWrite is not None:
            self._finishWrite('timeout', None)
        else:
            self.controls['detail/feedback'].asLabel().SetText('详情读取超时，请返回后重试')

    # 目录分片先按编号组装；规则变动与当前详情通过修订号避免回填旧状态。
    def ReceiveResponse(self, args):
        kind = args['kind']
        if self.closed:
            return
        if kind == 'changed':
            detail = args['detail']
            if not self._applyStatus(detail):
                return
            if self.catalogReady and self.selectedItem is None:
                self._refreshCatalog()
            elif (self.selectedItem == detail['itemName'] and self.detail is not None and
                  self.request is None and not self._hasDraft()):
                self._showDetail(detail, True)
            return
        if self.request is None or self.request[1] != args['requestId']:
            return
        self.canEdit = args['canEdit']
        if kind == 'catalog':
            self.catalogChunks[args['index']] = args['entries']
            if len(self.catalogChunks) == args['total']:
                rows = [row for index in range(args['total']) for row in self.catalogChunks[index]]
                self.catalogChunks.clear()
                self._finishRequest()
                # 本地化名称和图标也分帧读取，整份索引就绪后搜索才开始显示结果。
                self.indexing = clientApi.StartCoroutine(self._indexCatalog(rows, args['revision']), self.CatalogIndexed)
            return
        self._finishRequest()
        detail = args['detail']
        if kind == 'write':
            self._finishWrite(args['code'], detail)
        elif self.pendingWrite is not None:
            desiredUnits = self.pendingWrite[0]
            code = 'same' if detail is not None and detail['manualUnits'] == desiredUnits else 'timeout'
            self._finishWrite(code, detail)
        elif detail is not None:
            self._applyStatus(detail)
            self._showDetail(detail, True)
        else:
            self.controls['detail/feedback'].asLabel().SetText('该食物暂不可用，请返回列表')

    # 索引只在目录接收完时构造，搜索和分页不再查询引擎物品信息。
    def _indexCatalog(self, rows, revision):
        for index, (itemName, status) in enumerate(rows):
            if index and index % config.foodCatalogBatchSize == 0:
                yield
            info = self.itemComp.GetItemBasicInfo(itemName, 0)
            label = info['itemName'] if info and info['itemName'] else itemName
            namespace = itemName.split(':', 1)[0]
            self.entries[itemName] = {
                'label': label, 'searchName': FoodNutrition.foodSearchText(label), 'namespace': namespace,
                'icon': info['id_aux'] if info else 0, 'status': status, 'revision': revision
            }
            self.itemNames.append(itemName)
            if namespace not in self.representatives:
                self.representatives[namespace] = itemName

    # 索引期间积攒的世界变更在首屏渲染前合并，避免先显示旧的待设置清单。
    def CatalogIndexed(self):
        self.indexing = None
        if self.closed:
            return
        self.catalogReady = True
        for detail in self.earlyChanges.values():
            self._applyStatus(detail)
        self.earlyChanges.clear()
        self._refreshCatalog()

    # 只有同物品较新的状态才覆盖索引，联机保存后的增量与分页互不干扰。
    def _applyStatus(self, detail):
        itemName = detail['itemName']
        if itemName not in self.entries:
            if not self.catalogReady and (itemName not in self.earlyChanges or
                                          detail['revision'] > self.earlyChanges[itemName]['revision']):
                self.earlyChanges[itemName] = detail
            return False
        entry = self.entries[itemName]
        if detail['revision'] < entry['revision']:
            return False
        entry['revision'] = detail['revision']
        entry['status'] = detail['status']
        return True

    # 搜索、切页签和保存回到列表时重新统计命中；单纯翻页只更新左侧物品格。
    def _refreshCatalog(self):
        if not self.catalogReady:
            return
        self.matches, counts = FoodNutrition.filterFoodCatalog(
            self.itemNames, self.entries, self.showConfigured, self.selectedNamespace, self.keyword
        )
        if self.selectedNamespace and self.selectedNamespace not in counts:
            counts[self.selectedNamespace] = 0
        self.namespaces = sorted(namespace for namespace in counts if namespace)
        for name, selected in (('pending', not self.showConfigured), ('configured', self.showConfigured)):
            path = windowPath + '/catalog/' + name
            self.GetBaseUIControl(path + '/selected').SetVisible(selected)
            self.GetBaseUIControl(path + '/caption').asLabel().SetTextColor(selectedColor if selected else inkColor)
        matchCount = '{} 种'.format(len(self.matches))
        self.controls['catalog/matchCount'].asLabel().SetText(matchCount)
        allPath = windowPath + '/catalog/all'
        self.GetBaseUIControl(allPath + '/selected').SetVisible(not self.selectedNamespace)
        self.GetBaseUIControl(allPath + '/icon').SetVisible(False)
        for name, value in (('name', '全部'), ('count', str(counts['']))):
            label = self.GetBaseUIControl(allPath + '/' + name).asLabel()
            label.SetText(value)
            label.SetTextColor(inkColor if self.selectedNamespace else selectedColor)
        self._renderNamespaces(counts)
        self._renderPage()

    # 滚动内容的路径随触控模式变化，按当前路径复用行控件，缩短列表时隐藏多余行。
    def _renderNamespaces(self, counts):
        scroll = self.controls['catalog/namespaceScroll'].asScrollView()
        contentPath = scroll.GetScrollViewContentPath()
        content = self.GetBaseUIControl(contentPath)
        previousCount = self.namespaceRowCounts.get(contentPath, 0)
        rowHeight = 21 if self.namespaceWidth >= 89 else 31
        for index, namespace in enumerate(self.namespaces):
            name = 'namespace' + str(index)
            path = contentPath + '/' + name
            if index >= previousCount:
                row = self.CreateChildControl('food_nutrition.namespaceRow', name, content, False)
                self._bindButton(row, self.SelectNamespace)
            else:
                row = self.GetBaseUIControl(path)
            row.SetPosition((0, index * rowHeight))
            # 桌面滚动条占用内容右边的空间，预留宽度让计数保持完整可见。
            row.SetSize((self.namespaceWidth - 8, rowHeight - 2), True)
            row.SetVisible(True)
            selected = self.selectedNamespace == namespace
            self.GetBaseUIControl(path + '/selected').SetVisible(selected)
            icon = self.GetBaseUIControl(path + '/icon')
            icon.SetPropertyBag({'#item_id_aux': self.entries[self.representatives[namespace]]['icon']})
            for child, value in (('name', namespace), ('count', str(counts[namespace]))):
                label = self.GetBaseUIControl(path + '/' + child).asLabel()
                label.SetText(value)
                label.SetTextColor(selectedColor if selected else inkColor)
        for index in range(len(self.namespaces), previousCount):
            self.GetBaseUIControl(contentPath + '/namespace' + str(index)).SetVisible(False)
        self.namespaceRowCounts[contentPath] = max(previousCount, len(self.namespaces))
        content.SetSize((self.namespaceWidth, max(1, rowHeight * len(self.namespaces))))

    # 分页只绘制当前切片，返回目录后页数减少时回落到末页。
    def _renderPage(self):
        pageSize = self.columns * self.rows
        self.pageCount = max(1, (len(self.matches) + pageSize - 1) // pageSize)
        self.page = min(max(0, self.page), self.pageCount - 1)
        start = self.page * pageSize
        self.visibleFoods = self.matches[start:start + pageSize]
        for index, (button, icon, label) in enumerate(self.tiles):
            shown = index < len(self.visibleFoods)
            button.SetVisible(shown)
            if shown:
                entry = self.entries[self.visibleFoods[index]]
                column = index % self.columns
                row = index // self.columns
                button.SetPosition((column * (self.tileWidth + 4), row * (self.tileHeight + 4)))
                # 背景、图标锚点和名称宽度都依赖格子尺寸，重排时要同时更新子控件。
                button.SetSize((self.tileWidth, self.tileHeight), True)
                icon.SetPropertyBag({'#item_id_aux': entry['icon']})
                label.asLabel().SetText(entry['label'])
        empty = not self.matches
        self.controls['catalog/notice'].SetVisible(empty)
        if empty:
            self.controls['catalog/notice'].asLabel().SetText('没有匹配的食物' if self.keyword else '此分类暂无食物')
        self.controls['catalog/page'].asLabel().SetText('{}/{} 页'.format(self.page + 1, self.pageCount))
        for button, enabled in (('previous', self.page > 0), ('next', self.page + 1 < self.pageCount)):
            control = self.controls['catalog/' + button]
            control.SetVisible(self.pageCount > 1)
            control.SetTouchEnable(enabled)
            control.SetAlpha(1.0 if enabled else 0.50)
        self.UpdateScreen(True)

    @ViewBinder.binding(ViewBinder.BF_EditChanged, "#food_nutrition.search")
    def SearchChanged(self, args):
        text = args['Text']
        if text != self.keyword:
            self.keyword = text
            self.page = 0
            self._refreshCatalog()
        return ViewRequest.Nothing

    @ViewBinder.binding(ViewBinder.BF_EditFinished, "#food_nutrition.search")
    def SearchFinished(self, args):
        return self.SearchChanged(args)

    @ViewBinder.binding(ViewBinder.BF_BindString, "#food_nutrition.search_text")
    def BindSearchText(self):
        return self.keyword

    def CatalogAction(self, args):
        name = args['ButtonPath'].rsplit('/', 1)[-1]
        if name == 'retry':
            self._requestCatalog()
        elif name in ('previous', 'next'):
            self.page += 1 if name == 'next' else -1
            self._renderPage()
        else:
            if name == 'clear':
                self.keyword = ''
                self.controls['catalog/search'].asTextEditBox().SetEditText('')
            elif name == 'all':
                self.selectedNamespace = ''
            else:
                self.showConfigured = name == 'configured'
                self.selectedNamespace = ''
            self.page = 0
            self._refreshCatalog()

    def SelectNamespace(self, args):
        path = args['ButtonPath']
        index = int(path.rsplit('/namespace', 1)[-1])
        if index < len(self.namespaces):
            self.selectedNamespace = self.namespaces[index]
            self.page = 0
            self._refreshCatalog()

    def SelectFood(self, args):
        path = args['ButtonPath']
        index = int(path.rsplit('/tile', 1)[-1])
        if index >= len(self.visibleFoods):
            return
        self.selectedItem = self.visibleFoods[index]
        self.detail = None
        self.restorePending = False
        entry = self.entries[self.selectedItem]
        self.controls['title'].asLabel().SetText('设置食物营养')
        self.GetBaseUIControl(windowPath + '/back/caption').asLabel().SetText('‹ 食物列表')
        self.controls['catalog'].SetVisible(False)
        self.controls['detail'].SetVisible(True)
        self.controls['detail/itemIcon'].SetPropertyBag({'#item_id_aux': entry['icon']})
        self.controls['detail/itemName'].asLabel().SetText(entry['label'])
        self.controls['detail/itemStatus'].asLabel().SetText('正在读取规则…')
        self.controls['detail/source'].asLabel().SetText('')
        self.controls['detail/feedback'].asLabel().SetText('')
        self.controls['detail/save'].SetVisible(False)
        self.controls['detail/restore'].SetVisible(False)
        for row in self.groupRows:
            row['panel'].SetVisible(False)
        self.UpdateScreen(True)
        self._sendRequest(config.foodDetailRequest, {'itemName': self.selectedItem})

    # 详情回执统一刷新状态和可编辑性；冲突时更新基准值但保留玩家输入。
    def _showDetail(self, detail, resetDraft):
        self.detail = detail
        manualUnits = detail['manualUnits']
        referenceUnits = detail['referenceUnits']
        shownUnits = manualUnits if manualUnits is not None else referenceUnits
        self.initialUnits = shownUnits if shownUnits is not None else [0] * len(config.groupOrder)
        status = statusNames[detail['status']]
        if not self.canEdit:
            status += ' · 只读'
        elif detail['status'] == 'auto' and referenceUnits is not None:
            status += ' · 实测基础参考'
        self.controls['detail/itemStatus'].asLabel().SetText(status)
        source = ''
        if detail['autoGroups']:
            groups = '、'.join(config.groups[groupId]['name'] for groupId in detail['autoGroups'])
            source = '{} · {}'.format('、'.join(detail['autoSources']), groups)
        self.controls['detail/source'].asLabel().SetText(source)
        self.controls['detail/save'].SetVisible(self.canEdit)
        self.controls['detail/restore'].SetVisible(self.canEdit and manualUnits is not None)
        for index, row in enumerate(self.groupRows):
            row['panel'].SetVisible(True)
            for name in ('minus', 'plus', 'value'):
                row[name].SetVisible(self.canEdit)
                row[name].SetTouchEnable(True)
            row['readOnly'].SetVisible(not self.canEdit)
            readonly = '—' if shownUnits is None else FoodNutrition.formatFoodUnits(shownUnits[index])
            row['readOnly'].asLabel().SetText(readonly)
            if resetDraft:
                row['value'].asTextEditBox().SetEditText(FoodNutrition.formatFoodUnits(self.initialUnits[index]))
        if resetDraft:
            self.restorePending = False
            self.controls['detail/feedback'].asLabel().SetText('')
        self.controls['detail/save'].SetTouchEnable(True)
        self.controls['detail/restore'].SetTouchEnable(True)
        self.UpdateScreen(True)

    # 离开确认与保存读取实际编辑框，确保手机键盘提交后的文字也参与校验。
    def _readDraft(self):
        return [FoodNutrition.parseFoodUnits(row['value'].asTextEditBox().GetEditText()) for row in self.groupRows]

    # 五项合法但等于基准值时可直接退出；暂存恢复默认同样属于未保存改动。
    def _hasDraft(self):
        return (self.detail is not None and self.canEdit and
                (self.restorePending or self._readDraft() != self.initialUnits))

    def DetailAction(self, args):
        path = args['ButtonPath']
        name = path.rsplit('/', 1)[-1]
        if self.detail is None or not self.canEdit or self.pendingWrite is not None:
            return
        if name == 'save':
            self._saveDraft(None)
        elif name == 'restore':
            self.restorePending = True
            defaults = self.detail['referenceUnits']
            if defaults is None:
                defaults = [0] * len(config.groupOrder)
            for index, row in enumerate(self.groupRows):
                row['value'].asTextEditBox().SetEditText(FoodNutrition.formatFoodUnits(defaults[index]))
            message = '保存后恢复自动计算' if self.detail['autoGroups'] else '保存后回到待设置'
            self.controls['detail/feedback'].asLabel().SetText(message)
        else:
            rowName = path.split('/')[-2]
            row = self.groupRows[int(rowName[len('group'):])]
            editor = row['value'].asTextEditBox()
            units = FoodNutrition.parseFoodUnits(editor.GetEditText())
            if units is None:
                self.controls['detail/feedback'].asLabel().SetText('请输入 0–100，步进 0.5')
                return
            self.restorePending = False
            units = max(0, min(config.foodNutritionMaxUnits, units + (1 if name == 'plus' else -1)))
            editor.SetEditText(FoodNutrition.formatFoodUnits(units))
            self.controls['detail/feedback'].asLabel().SetText('')

    # 保存等待期间冻结控件，回执或读回后再决定留在详情还是继续此前的返回操作。
    def _saveDraft(self, target):
        values = self._readDraft()
        if None in values:
            self.controls['detail/feedback'].asLabel().SetText('请输入 0–100，步进 0.5')
            return
        defaults = self.detail['referenceUnits']
        if defaults is None:
            defaults = [0] * len(config.groupOrder)
        desired = None if self.restorePending and values == defaults else values
        self.pendingWrite = (desired, target)
        for row in self.groupRows:
            for name in ('value', 'minus', 'plus'):
                row[name].SetTouchEnable(False)
        self.controls['detail/save'].SetTouchEnable(False)
        self.controls['detail/restore'].SetTouchEnable(False)
        self.controls['detail/feedback'].asLabel().SetText('正在保存世界规则…')
        self._sendRequest(config.foodRuleRequest, {
            'itemName': self.selectedItem, 'previousUnits': self.detail['manualUnits'], 'desiredUnits': desired
        })

    # 服务端确认后再变更列表状态；失败和冲突继续显示原草稿供核对。
    def _finishWrite(self, code, detail):
        desired, target = self.pendingWrite
        self.pendingWrite = None
        saved = code in ('saved', 'same')
        if detail is not None:
            self._applyStatus(detail)
        self._showDetail(detail if detail is not None else self.detail, saved)
        if saved:
            message = '已恢复默认' if desired is None else '已保存 · 下次进食生效'
            self.controls['detail/feedback'].asLabel().SetText(message)
            if target is not None:
                self._leave(target)
        else:
            message = writeMessages[code]
            if code == 'conflict' and detail is not None:
                latest = detail['manualUnits']
                if latest is not None:
                    message = '规则已变化 · 最新值 {}'.format(' / '.join(FoodNutrition.formatFoodUnits(value)
                                                                  for value in latest))
                else:
                    message = '规则已变化 · 当前为{}'.format(statusNames[detail['status']])
            self.controls['detail/feedback'].asLabel().SetText(message)

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#food_nutrition.back")
    def BackKey(self, args):
        if self.confirmTarget is not None:
            self.confirmTarget = None
            self.GetBaseUIControl(confirmPath).SetVisible(False)
        else:
            self._navigate('catalog' if self.selectedItem is not None else 'close')
        return ViewRequest.Nothing

    def Navigate(self, args):
        path = args['ButtonPath']
        target = 'catalog' if self.selectedItem is not None and path.endswith('/back') else 'close'
        self._navigate(target)

    # 返回键、关闭和点击返回都经过同一个草稿门槛。
    def _navigate(self, target):
        if self.pendingWrite is not None:
            return
        if self._hasDraft():
            self.confirmTarget = target
            self.GetBaseUIControl(confirmPath).SetVisible(True)
        else:
            self._leave(target)

    def ConfirmAction(self, args):
        name = args['ButtonPath'].rsplit('/', 1)[-1]
        target = self.confirmTarget
        self.confirmTarget = None
        self.GetBaseUIControl(confirmPath).SetVisible(False)
        if name == 'save':
            self._saveDraft(target)
        elif name == 'discard':
            self._leave(target)

    # 详情是同一界面的内层，回清单保留查询和分页，关闭才真正弹栈。
    def _leave(self, target):
        if target == 'close':
            self.Destroy()
            clientApi.PopScreen()
            return
        self._finishRequest()
        self.selectedItem = None
        self.detail = None
        self.restorePending = False
        self.controls['title'].asLabel().SetText('食物营养')
        self.GetBaseUIControl(windowPath + '/back/caption').asLabel().SetText('‹ 均衡饮食')
        self.controls['detail'].SetVisible(False)
        self.controls['catalog'].SetVisible(True)
        self._refreshCatalog()
