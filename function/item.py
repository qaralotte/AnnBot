# 市价查询

import json
import time
import requests

import util.ff14.alias as alias
import message.util as util

from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import MatchRegex
from graia.ariadne.model import Group
from lxml import etree

from util import setting
from core.bot import app


class Universail:
    # Wiki 链接
    WIKI_URL = "https://ff14.huijiwiki.com/wiki"
    
    # Universail 链接
    UNIVERSAIL_URL = 'https://universalis.app/market'
    
    # 最低价格表最大查询数量
    QUERY_MAX = 8
    
    def __init__(self, name, server):
        
        locations = alias.location()
        
        # 如果区服名称错误则抛出 ServerNotFoundError
        if server not in locations:
            raise ServerNotFoundError()
        
        # 设置 cookies
        self.cookies = {
            'mogboard_homeworld': 'no',
            'mogboard_language': 'chs',
            'mogboard_leftnav': 'off',
            'mogboard_server': locations[server],
            'mogboard_timezone': 'Asia/Chongqing',
        }
        
        # 物品 id
        self.name = name
        
        # 查找物品 id, 如果未找到则抛出 ItemNotFoundError
        self.id = self.find_id()
        
        # universale 的 dom (避免多次加载)
        self.dom = None
        
        # 查询物品是否可出售, 如果不可出售则抛出 UnsalableError
        if self.is_salable():
            self.url = f'{self.UNIVERSAIL_URL}/{self.id}'
            self.has_hq, self.has_nq, self.hq_items, self.nq_items = self.serach_lowest()
    
    # 查询物品 id
    def find_id(self):
        url = f'{self.WIKI_URL}/物品:{self.name}'
        r = requests.get(url)
        
        if r.status_code == 200:
            dom = etree.HTML(r.content.decode('utf-8'))
            
            # .external text 第 ② 个标签的 href
            garland = dom.xpath('//a[contains(text(), "Garland Data")]/@href')[0]
            
            # "http://www.garlandtools.org/db/#item/xxxxx" -> xxxxx
            return garland[garland.rindex('/') + 1:]
        else:
            # 没有找到物品
            raise ItemNotFoundError()
    
    # 查询物品是否可出售
    def is_salable(self):
        url = f'{self.UNIVERSAIL_URL}/{self.id}'
        r = requests.get(url=url, cookies=self.cookies)
        self.dom = etree.HTML(r.content.decode('utf-8'))
        error = self.dom.xpath('//*[@class="error-page"]')
        if len(error) != 0:
            raise UnsalableError()
        return True
    
    # 搜索物品最低价格
    def serach_lowest(self):
        has_hq = self.has_quality('HQ 最低价')
        has_nq = self.has_quality('NQ 最低价')
        
        hq_items = self.query_items('HQ 价格') if has_hq else None
        nq_items = self.query_items('NQ 价格') if has_nq else None
        
        return has_hq, has_nq, hq_items, nq_items
    
    # 是否有 HQ / NQ 品质
    def has_quality(self, quality):
        x = self.dom.xpath(f'//h2[contains(text(), "{quality}")]/following-sibling::*[1]/*[@class="xiv-Gil"]')
        return len(x) != 0
    
    # 查询市价
    def query_items(self, quality):
        table = self.dom.xpath(f'//h6[contains(text(), "{quality}")]/following-sibling::*[1]//tbody/tr')
        items = []
        for i, item in enumerate(table):
            if i == self.QUERY_MAX:
                break
            server = item.xpath('./*[@class="price-server"]/strong/text()')[0]
            price = item.xpath('./*[@class="price-current"]/text()')[0]
            count = item.xpath('./*[@class="price-qty"]/text()')[0]
            total = item.xpath('./*[@class="price-total"]/text()')[0]
            items.append((server, price, count, total))
        
        return items
    
    # 查询更新日期
    def query_time(self, server):
        universail_api = f'https://universalis.app/api/v2/history/{server}/{self.id}'
        r = requests.get(universail_api)
        jsonobj = json.loads(r.content.decode('utf-8'))
        secs = int(jsonobj['lastUploadTime']) / 1000
        
        time_array = time.localtime(secs)
        style_time = time.strftime('%Y.%m.%d %H:%M:%S', time_array)
        
        return style_time


# 模糊查找最大查询数
FUZZY_MAX_SEARCH = 20


# 模糊查找物品名称
def fuzzy_search(name):
    item_search_api = ('https://cdn.huijiwiki.com/ff14/api.php?'
                       'format=json&action=parse&disablelimitreport=true&prop=text&title=ItemSearch&'
                       f'ver={setting.read("ff14")["version"]}&smaxage=86400&maxage=86400&text='
                       '{{ItemSearch|name=' + name + '|job=0|kind=0|category=0|rarity=0|version=0}}')
    
    headers = {
        'referer': 'https://ff14.huijiwiki.com/wiki/'
    }
    
    r = requests.get(url=item_search_api, headers=headers)
    
    jsonobj = json.loads(r.content.decode('utf-8'))
    html = str(jsonobj['parse']['text']['*'])
    
    names = etree.HTML(html).xpath('//div[contains(@class, "item-name")]/a/text()')
    return names[:FUZZY_MAX_SEARCH]


@app.broadcast.receiver(GroupMessage, decorators=[MatchRegex(r'^/item \S+ \S+')])
async def send_to_group(group: Group, messages: MessageChain):
    messages = messages.asSendable()
    
    args = util.getargs(messages)
    
    # 物品名称, 区服名称
    name, server = str(args[0]), str(args[1])
    try:
        universale = Universail(name, server)
        
        outmsgs = MessageChain.create()
        if universale.has_hq:
            outmsgs.append(f'「{name}」HQ 市价表: \n')
            for server, price, count, total in universale.hq_items:
                outmsgs.append(f'\t服务器: {server}, 价格: {price}, 数量: {count}, 总计: {total}\n')
        else:
            outmsgs.append(f'「{name}」无 HQ 品质在售: \n')
        
        outmsgs.append('----------\n')
        
        if universale.has_nq:
            outmsgs.append(f'「{name}」NQ 市价表: \n')
            for server, price, count, total in universale.nq_items:
                outmsgs.append(f'\t服务器: {server}, 价格: {price}, 数量: {count}, 总计: {total}\n')
        else:
            outmsgs.append(f'「{name}」无 NQ 品质在售: \n')

        outmsgs.append(f'数据来源: {universale.url}\n')
        outmsgs.append(f'更新日期: {universale.query_time(universale.nq_items[0][0])}') if universale.has_nq else None
        
        await app.sendGroupMessage(group, outmsgs)
    
    except ServerNotFoundError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: {server} 不是一个正确的区服名称\n区服可选: (鸟/猫/猪/狗) or 全称'))
        return
    except ItemNotFoundError:
        outmsgs = MessageChain.create(f'错误: 没有找到该物品「{name}」, 请检查是否拼写正确')
        
        # 开始模糊查找
        may_items = fuzzy_search(name)
        if len(may_items) != 0:
            outmsgs.append(f'\n关于可能是「{name}」的检索结果如下: \n')
            for may_item in may_items:
                outmsgs.append(f'\t{may_item}\n')
        
        await app.sendGroupMessage(group, outmsgs)
        return
    except UnsalableError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: 「{name}」不可在市场出售'))
        return


# 区服名称错误
class ServerNotFoundError(BaseException):
    pass


# 物品未找到
class ItemNotFoundError(BaseException):
    pass


# 物品不可出售
class UnsalableError(BaseException):
    pass
