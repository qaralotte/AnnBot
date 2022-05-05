# 帮助

from graia.ariadne.model import Group

import core.bot as bot

from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import MatchContent

from core.bot import app


def command_lists():
    return ('指令: \n'
            '1. /setu [可选 tag1] [可选 tag2] [可选 tag3]: 随机一张涩图\n'
            '2. /item [物品名称] [区服 (鸟/猫/猪/狗)]: FF14 市价查询\n'
            '3. /logs [副本名 / boss] [排名线] [rdps / adps] [国服 / 国际服] [版本 (x.y)]: FF14 logs 查询\n'
            '4. /image [图片]: 搜图\n'
            '5. /help: 相关信息查询\n'
            '6. [x]d[y]: 跑团 roll 点\n'
            '7. 再来一张: 随机一张上次 tags 的涩图')


@app.broadcast.receiver(GroupMessage, decorators=[MatchContent('/help')])
async def send_to_group(group: Group):
    await app.sendGroupMessage(group, MessageChain.create(
        ('这里是安可露的自用机器人, 仅供本人娱乐使用\n'
         f'版本: {bot.version()}\n'
         f'{command_lists()}')
    ))
