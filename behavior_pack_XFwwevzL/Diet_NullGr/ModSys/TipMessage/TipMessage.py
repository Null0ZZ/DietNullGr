# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.TipMessage.config as config


# 每名玩家只保留当前展示锁和一个待播批次，持续产生的消息不会形成长期队列。
def createPlayerState():
    return {
        'visibleUntilTick': 0,
        'firstPendingTick': 0,
        'nextOrder': 0,
        'pendingMessages': {}
    }


# 固定窗口从首条消息开始计时；同一聚合键只更新内容，不延长窗口或增加队列长度。
def queueMessage(state, currentTick, messageKey, message, priority):
    pendingMessages = state['pendingMessages']
    if not pendingMessages:
        state['firstPendingTick'] = currentTick
    if messageKey in pendingMessages:
        order = pendingMessages[messageKey]['order']
    else:
        state['nextOrder'] += 1
        order = state['nextOrder']
    pendingMessages[messageKey] = {
        'message': message,
        'priority': priority,
        'order': order
    }


# 状态结束时主动撤销尚未展示的旧提示，避免痊愈后继续显示过期进度。
def removeMessage(state, messageKey):
    pendingMessages = state['pendingMessages']
    if messageKey in pendingMessages:
        del pendingMessages[messageKey]
    if not pendingMessages:
        state['firstPendingTick'] = 0


# 展示锁结束后一次取出整个批次；超出条数上限时优先保留高优先级消息并给出汇总数量。
def takeReadyMessage(state, currentTick):
    pendingMessages = state['pendingMessages']
    if not pendingMessages:
        return ""
    if currentTick < state['firstPendingTick'] + config.mergeWindowTick:
        return ""
    if currentTick < state['visibleUntilTick']:
        return ""

    messageDataList = sorted(
        pendingMessages.values(),
        key=lambda messageData: (-messageData['priority'], messageData['order'])
    )
    mergedMessages = []
    for messageData in messageDataList[:config.maximumMergedMessageCount]:
        mergedMessages.append(messageData['message'])
    omittedCount = len(messageDataList) - len(mergedMessages)
    if omittedCount > 0:
        mergedMessages.append(
            config.omittedMessageColor + "另有{}条提示。".format(omittedCount)
        )

    state['pendingMessages'] = {}
    state['firstPendingTick'] = 0
    state['visibleUntilTick'] = currentTick + config.displayHoldTick
    return config.messageSeparator.join(mergedMessages)
