# 「开启 / 关闭」 指令
# 管理员限定

from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group

from message import util
from core.bot import app

commands = [
    'roll',
    'setu',
    'item',
    'logs',
    'image',
    '再来一张',
    '复读',
]


# 禁用命令
@app.broadcast.receiver(GroupMessage, decorators=[MatchContent('/disable ')])
async def send_to_group(group: Group, messages: MessageChain):
    messages = messages.asSendable()
    
    args = util.getargs(messages)


# 启用命令
@app.broadcast.receiver(GroupMessage, decorators=[MatchContent('/enable ')])
async def send_to_group(group: Group, messages: MessageChain):
    messages = messages.asSendable()
