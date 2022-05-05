# 复读姬

from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from core.bot import app
from message.history import HistoryMap

# 重复 n 次就自动复读一次
REPLY_PATIENCE = 3

# 群消息历史记录 key: group_id
group_history = HistoryMap()


# 是否可以复读 (连续三条消息一样)
def can_reply(group):
    last_msgs = MessageChain.create()
    flag = False
    
    for i, msgs in enumerate(reversed(group_history[group.id])):
        # 第一句话跳过检查
        if i == 0:
            last_msgs = msgs
            continue
        
        # 如果上一句消息与这一句不同，则复读失败
        if last_msgs != msgs:
            if flag:
                # 如果是刚刚好复读到第三条则符合条件
                return True
            return False
        
        # 条件达成
        if i == REPLY_PATIENCE - 1:
            if len(group_history[group.id]) == REPLY_PATIENCE:
                return True
            
            flag = True
        
        if i == REPLY_PATIENCE:
            # 防止无限递归复读
            return False
        
        last_msgs = msgs
    
    return False


@app.broadcast.receiver(GroupMessage, priority=100)  # 优先度最低
async def send_to_group(group: Group, messages: MessageChain):
    messages = messages.asSendable()
    
    # 群消息历史记录
    group_history.put(group.id, messages)
    
    if can_reply(group):
        await app.sendGroupMessage(group, group_history.top(group.id))
