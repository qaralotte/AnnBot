# 跑团 roll 点

import random
import re

from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import App
from graia.ariadne.message.parser.base import MatchRegex
from graia.ariadne.model import Group

from core.bot import app


def find_all(msgs):
    pattern = '[0-9]+d[0-9]+'
    compiler = re.compile(pattern)
    return compiler.findall(str(msgs))


# (次数, 范围)
def read(s):
    pattern = '[0-9]+'
    compiler = re.compile(pattern)
    matches = compiler.findall(s)
    return int(matches[0]), int(matches[1])


@app.broadcast.receiver(GroupMessage, decorators=[MatchRegex(regex=r'[\s\S]*[0-9]+d[0-9]+[\s\S]*')])
async def send_to_group(group: Group, messages: MessageChain):
    messages = messages.asSendable()

    # 如果是分享的链接, 则直接匹配失败 (返回空数组)
    if messages.include(App):
        return

    # 同上
    if str(messages).startswith('http'):
        return

    matches = find_all(messages)

    # 如果匹配失败则跳过
    if len(matches) == 0:
        return

    outmsgs = MessageChain.create()
    for match in matches:
        tm, rg = read(match)
        if tm < 1 or tm > 65535:
            await app.sendGroupMessage(group, MessageChain.create('错误: 范围超限\n请确保值在范围之内 [1-65535]d[♾️]'))
            return
        for i in range(0, tm):
            if len(outmsgs) != 0:
                outmsgs.append('\n')

            result = random.randint(1, rg)
            outmsgs.append(str(result))

    await app.sendGroupMessage(group, outmsgs)
