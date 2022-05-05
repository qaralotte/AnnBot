# 搜图
import json
import urllib.parse

import requests
from graia.ariadne import get_running
from graia.ariadne.adapter import Adapter
from graia.ariadne.exception import RemoteException

import message.util as util

from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, At
from graia.ariadne.message.parser.base import MatchTemplate
from graia.ariadne.model import Group, Member

from core.bot import app

API_KEY = 'custom'

# 最大搜索数
SERACH_LIMIT = 5


# 获取所有结果 (json)
def getresults(img_url):
    api = f'https://saucenao.com/search.php?api_key={API_KEY}&db=999&output_type=2&testmode=1&numres=99&url={img_url}'
    r = requests.get(api)
    if r.status_code == 200:
        jsonobj = json.loads(r.content.decode('utf-8'))
        return jsonobj['results']
    else:
        raise BusyServerError()


# 处理 data 并以合适的格式输出到 MessageChain (see https://saucenao.com/tools/examples/api/index_details.txt)
# (*disabled) 不考虑
def analyse_data(data, index_id):
    
    messages = MessageChain.create()
    
    # h-mags
    if index_id == 0:
        kind = 'H-Magazines'
        title, part, date = data['title'], data['part'], data['date']
        
        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 章节: {part}\n'
                        f' 日期: {date}\n')
        
    # h-anime (disabled)
    if index_id == 1:
        pass
    
    # hcg
    if index_id == 2:
        kind = 'H-Game CG'
        title, company = data['title'], data['company']

        messages.append(f' 类型: {kind}\n'
                        f' 游戏名: {title}\n'
                        f' 制作公司: {company}\n')

    # ddb - objects (disabled)
    if index_id == 3:
        pass
    
    # ddb-samples (disabled)
    if index_id == 4:
        pass
    
    # pixiv (pixivhistorical)
    if index_id == 5 or index_id == 6:
        kind = 'Pixiv Images'
        title, author, pid = data['title'], data['member_name'], data['pixiv_id']
        url = f'https://www.pixiv.net/artworks/{pid}'

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' pid: {pid} 「{url}」\n')

    # anime (disabled)
    if index_id == 7:
        pass
    
    # seiga_illust - nico nico seiga
    if index_id == 8:
        kind = 'Nico Nico Seiga'
        url, title, seiga_id, author = data['ext_urls'][0], data['title'], data['seiga_id'], data['member_name']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' seiga id: {seiga_id} 「{url}」\n')
        
    # danbooru
    if index_id == 9:
        kind = 'Danbooru'
        url, danbooru_id, author, source = data['ext_urls'][0], data['danbooru_id'], data['creator'], data['source']

        messages.append(f' 类型: {kind}\n'
                        f' 源: {source}\n'
                        f' 作者: {author}\n'
                        f' danbooru_id: {danbooru_id} 「{url}」\n')
        
    # drawr
    if index_id == 10:
        kind = 'Drawr Images'
        url, drawr_id, title, author = data['ext_urls'][0], data['drawr_id'], data['title'], data['member_name']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' drawr_id: {drawr_id} 「{url}」\n')
    
    # nijie
    if index_id == 11:
        kind = 'Nijie Images'
        url, nijie_id, title, author = data['ext_urls'][0], data['nijie_id'], data['title'], data['member_name']
    
        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' nijie_id: {nijie_id} 「{url}」\n')
    
    # yande.re
    if index_id == 12:
        kind = 'Yande.re'
        url, yandere_id, author, source = data['ext_urls'][0], data['yandere_id'], data['creator'], data['source']

        messages.append(f' 类型: {kind}\n'
                        f' 源: {source}\n'
                        f' 作者: {author}\n'
                        f' yandere_id: {yandere_id} 「{url}」\n')
    
    # animeop (disabled)
    if index_id == 13:
        pass
    
    # IMDb (disabled)
    if index_id == 14:
        pass
    
    # Shutterstock (disabled)
    if index_id == 15:
        pass
    
    # FAKKU
    if index_id == 16:
        kind = 'FAKKU'
        url, source, author = data['ext_urls'][0], data['source'], data['creator']

        messages.append(f' 类型: {kind}\n'
                        f' 源: {source}\n'
                        f' 作者: {author}\n'
                        f' 链接: {url}\n')
        
    # (reserved)
    if index_id == 17:
        pass
    
    # H-MISC (nhentai / ehentai)
    if index_id == 18 or index_id == 38:
        kind = 'H-Misc (nhentai / ehentai)'
        source, authors, eng_name, jp_name = data['source'], data['creator'], data['eng_name'], data['jp_name']

        messages.append(f' 类型: {kind}\n'
                        f' 源: {source}\n'
                        f' 标题:\n'
                        f'  EN: {eng_name}\n'
                        f'  JP: {jp_name}\n'
                        f' 作者: {", ".join(str(i) for i in authors)}\n')
    
    # 2d_market
    if index_id == 19:
        kind = '2D Market'
        url, source, author = data['ext_urls'][0], data['source'], data['creator']
    
        messages.append(f' 类型: {kind}\n'
                        f' 源: {source}\n'
                        f' 作者: {author}\n')
    
    # medibang
    if index_id == 20:
        kind = 'MediBang'
        title, url, author = data['title'], data['url'], data['member_name']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' 链接: {url}\n')
        
    # Anime (H-Anime)
    if index_id == 21 or index_id == 22:
        kind = 'Anime'
        title, part, year, est_time = data['source'], data['part'], data['year'], data['est_time']

        messages.append(f' 类型: {kind}\n'
                        f' 名称: {title} ({year})\n'
                        f' 集: {part}\n'
                        f' 时间: {est_time}\n')
    
    # Movie
    if index_id == 23:
        kind = 'Movies'
        title, year, est_time = data['source'], data['year'], data['est_time']
    
        messages.append(f' 类型: {kind}\n'
                        f' 名称: {title} ({year})\n'
                        f' 时间: {est_time}\n')
    
    # Shows
    if index_id == 24:
        kind = 'Shows'
        title, part, year, est_time = data['source'], data['part'], data['year'], data['est_time']

        messages.append(f' 类型: {kind}\n'
                        f' 名称: {title} ({year})\n'
                        f' 场次: {part}\n'
                        f' 时间: {est_time}\n')
        
    # gelbooru
    if index_id == 25:
        kind = 'Gelbooru'
        url, gelbooru_id, author = data['ext_urls'][0], data['gelbooru_id'], data['creator']

        messages.append(f' 类型: {kind}\n'
                        f' 作者: {author}\n'
                        f' gelbooru_id: {gelbooru_id} 「{url}」\n')
    
    # konachan
    if index_id == 26:
        kind = 'Konachan'
        url, konachan_id, author, source = data['ext_urls'][0], data['konachan_id'], data['creator'], data['source']
    
        messages.append(f' 类型: {kind}\n'
                        f' 源: {source}\n'
                        f' 作者: {author}\n'
                        f' konachan_id: {konachan_id} 「{url}」\n')
    
    # sankaku
    if index_id == 27:
        kind = 'Sankaku Channel'
        url, sankaku_id, author = data['ext_urls'][0], data['sankaku_id'], data['creator']
    
        messages.append(f' 类型: {kind}\n'
                        f' 作者: {author}\n'
                        f' sankaku_id: {sankaku_id} 「{url}」\n')
    
    # anime-pictures
    if index_id == 28:
        kind = 'Anime-Pictures.net'
        url, anime_pictures_id = data['ext_urls'][0], data['anime-pictures_id']

        messages.append(f' 类型: {kind}\n'
                        f' anime-pictures_id: {anime_pictures_id} 「{url}」\n')
    
    # e621
    if index_id == 29:
        kind = 'e621.net'
        url, e621_id, author, source = data['ext_urls'][0], data['e621_id'], data['creator'], data['source']
    
        messages.append(f' 类型: {kind}\n'
                        f' 源: {source}\n'
                        f' 作者: {author}\n'
                        f' e621_id: {e621_id} 「{url}」\n')
        
    # idol complex
    if index_id == 30:
        kind = 'Idol Complex'
        url, idol_id = data['ext_urls'][0], data['idol_id']

        messages.append(f' 类型: {kind}\n'
                        f' idol_id: {idol_id} 「{url}」\n')
    
    # bcy (illust / cosplay)
    if index_id == 31 or index_id == 32:
        kind = 'bcy.net'
        url, title, bcy_id, author = data['ext_urls'][0], data['title'], data['bcy_id'], data['member_name']
        bcy_type = data['bcy_type']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' bcy 类型: {bcy_type}'
                        f' bcy_id: {bcy_id} 「{url}」\n')
    
    # portalgraphics
    if index_id == 33:
        kind = 'PortalGraphics.net (Hist)'
        url, title, pg_id, author = data['ext_urls'][0], data['title'], data['pg_id'], data['member_name']
    
        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' pg_id: {pg_id} 「{url}」\n')
    
    # dA
    if index_id == 34:
        kind = 'deviantArt'
        url, title, da_id, author = data['ext_urls'][0], data['title'], data['da_id'], data['author_name']
    
        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' da_id: {da_id} 「{url}」\n')
        
    # pawoo
    if index_id == 35:
        kind = 'Pawoo.net'
        url, title, pawoo_id = data['ext_urls'][0], data['pawoo_user_display_name'], data['pawoo_id']
        author = data['pawoo_user_username']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}'
                        f' 作者: {author}\n'
                        f' pawoo_id: {pawoo_id} 「{url}」\n')
    
    # madokami
    if index_id == 36:
        kind = 'Madokami (Manga)'
        url, title, part, mu_id = data['ext_urls'][0], data['source'], data['part'], data['mu_id']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 章节: {part}\n'
                        f' mu_id: {mu_id} 「{url}」\n')
    
    # mangadex
    if index_id == 37:
        kind = 'MangaDex2'
        md_url, mu_url, mal_url = data['ext_urls'][0], data['ext_urls'][1], data['ext_urls'][2]
        title, part = data['source'], data['part']
        md_id, mu_id, mal_id, author = data['md_id'], data['mu_id'], data['mal_id'], data['author']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' 章节: {part}\n'
                        f' md_id: {md_id} ({md_url})\n'
                        f' mu_id: {mu_id} ({mu_url})\n'
                        f' mal_id: {mal_id} ({mal_url})\n')
    
    # ArtStation
    if index_id == 39:
        kind = 'ArtStation'
        url, title, author = data['ext_urls'][0], data['title'], data['author_name']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' 链接: {url}\n')
    
    # FurAffinity
    if index_id == 40:
        kind = 'FurAffinity'
        url, title, fa_id, author = data['ext_urls'][0], data['title'], data['fa_id'], data['author_name']
    
        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' fa_id: {fa_id} 「{url}」\n')
    
    # Twitter
    if index_id == 41:
        kind = 'Twitter'
        url, username = data['ext_urls'][0], data['twitter_user_handle']

        messages.append(f' 类型: {kind}\n'
                        f' 用户: @{username}\n'
                        f' 推文: {url}\n')
    
    # Furry Network
    if index_id == 42:
        kind = 'Furry Network'
        url, title, fn_id, author = data['ext_urls'][0], data['title'], data['fn_id'], data['author_name']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' fn_id: {fn_id} 「{url}」\n')
    
    # Kemono
    if index_id == 43:
        kind = 'Kemono'
        url, title, _id, author = data['ext_urls'][0], data['title'], data['id'], data['user_name']

        messages.append(f' 类型: {kind}\n'
                        f' 标题: {title}\n'
                        f' 作者: {author}\n'
                        f' id: {_id} 「{url}」\n')
    
    return messages


async def download(url):
    session = get_running(Adapter).session
    
    async with session.get(url) as r:
        data = await r.read()
        return data


@app.broadcast.receiver(GroupMessage, decorators=[MatchTemplate([Plain('/image'), Plain, Image])])
async def send_to_group(group: Group, sender: Member, messages: MessageChain):
    messages = messages.asSendable()
    args = util.getargs(messages)
    
    img_url = urllib.parse.quote(args[0].url, '')
    
    try:
        await app.sendGroupMessage(group, MessageChain.create([At(sender), ' 正在搜图中...']))
        
        results = getresults(img_url)

        outmsgs = MessageChain.create()
        for i, result in enumerate(results):
            if i == SERACH_LIMIT:
                break

            if i != 0:
                outmsgs.append('----------\n')
                
            header, data = result['header'], result['data']
            similarity = float(header['similarity'])
            thumbnail = str(header['thumbnail'])
            index_id = int(header['index_id'])
            
            try:
                img_bytes = await download(thumbnail)
                img = await app.uploadImage(img_bytes)
                outmsgs.append(img).append('\n')
            except RemoteException:
                # 上传失败, 说明被吞了
                outmsgs.append(' 「图被吞了」\n')
                
            outmsgs.append(f'相似度: {similarity}%\n')
            outmsgs = MessageChain.create().join([outmsgs, analyse_data(data, index_id)])

        await app.sendGroupMessage(group, outmsgs)
    
    except BusyServerError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: 服务器繁忙, 请稍后再试'))
        return


# 服务器繁忙
class BusyServerError(BaseException):
    pass
