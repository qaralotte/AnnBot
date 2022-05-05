# 随机涩图

import json
import urllib.parse
import requests

import message.util as util

from graia.ariadne import get_running
from graia.ariadne.adapter import Adapter
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.exception import RemoteException
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At
from graia.ariadne.message.parser.base import MatchContent, MatchRegex
from graia.ariadne.model import Group, Member

from core.bot import app
from message.history import HistoryMap

SETUAPI = 'https://api.lolicon.app/setu/v2'

# 群涩图历史记录 key: (group_id. member_id)
group_history = HistoryMap()


# 根据 tags 发送对应的 get 请求链接
def get(tags):
    param = urllib.parse.urlencode(list(tags))
    
    url = SETUAPI + (f'?{param}' if len(param) != 0 else '')
    
    resp = requests.get(url)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        jsonobj = json.loads(resp.text)
        return jsonobj
    else:
        return None


# 将 json 转化成可读的图片信息
async def analysis(data):
    img_data = await download(str(data['urls']['original']))
    title = str(data['title'])
    author = str(data['author'])
    pid = str(data["pid"])
    url = f'https://www.pixiv.net/artworks/{pid}'
    return img_data, title, author, pid, url


# 替换原 pixiv 链接为国内镜像链接 (暂时)
async def download(url):
    url = url.replace("i.pixiv.cat", "o.i.edcms.pw")
    session = get_running(Adapter).session
    session.headers['referer'] = 'https://pixivic.com/'
    
    async with session.get(url) as r:
        data = await r.read()
        return data


@app.broadcast.receiver(GroupMessage, decorators=[MatchRegex(regex=r'^/setu[\s\S]*')])
async def send_to_group(group: Group, sender: Member, messages: MessageChain):
    messages = messages.asSendable()
    
    args = util.getargs(messages)
    
    if len(args) > 3:
        await app.sendGroupMessage(group, MessageChain.create('错误: tag 数超出限制 (最多3个)'))
        return
    
    tags = set()
    for arg in args:
        tags.add(('tag', str(arg)))
    
    jsonobj = get(tags)
    if jsonobj is None:
        await app.sendGroupMessage(group, MessageChain.create("错误: 涩图信息获取失败"))
        return
    if len(str(jsonobj['error'])) != 0:
        await app.sendGroupMessage(group, MessageChain.create(f" 错误: 涩图信息获取失败, 错误信息: {jsonobj['error']}"))
        return
    if len(jsonobj['data']) == 0:
        tagslit = ', '.join(str(i[1]) for i in tags)
        await app.sendGroupMessage(group, MessageChain.create(f" 错误: tags: [{tagslit}] 没有找到任何图"))
        return
    
    # 群涩图历史记录
    group_history.put((group.id, sender.id), messages)
    
    await app.sendGroupMessage(group, MessageChain.create([At(sender), Plain(' 涩图下载中...')]))
    img_data, title, author, pid, url = await analysis(jsonobj['data'][0])
    
    outmsgs = MessageChain.create(At(sender)).append('\n')
    
    try:
        img = await app.uploadImage(img_data)
        outmsgs.append(img).append('\n')
    except RemoteException:
        # 上传失败, 说明被吞了
        outmsgs.append(' 「图被吞了」\n')
    
    await app.sendGroupMessage(group, outmsgs.append(f' 标题: {title}\n'
                                                     f' 作者: {author}\n'
                                                     f' pid: {pid} 「{url}」'))


@app.broadcast.receiver(GroupMessage, decorators=[MatchContent('再来一张')])
async def one_more(group: Group, sender: Member):
    # 如果这个群一个涩图都没有
    if (group.id, sender.id) not in group_history.container:
        return
    
    # 根据上一次请求的参数来获取涩图
    await send_to_group(group, sender, group_history.top((group.id, sender.id)))
