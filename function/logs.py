# 查询 logs 排名

import json

import requests
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import MatchRegex
from graia.ariadne.model import Group
from lxml import etree

import util.ff14.alias as alias
import message.util as util

from core.bot import app

API_KEY = 'custom'


# 根据名称 (黑话别名) 来寻找对应的职业名称
# todo 暂时用不到
def find_job(jobname):
    jobs = alias.job()
    if jobname not in jobs:
        raise JobNotFoundError()
    return jobs[jobname]


# 根据名称来寻找对应战斗的基本信息
def find_raid(raidname):
    if raidname not in alias.raid():
        raise RaidNotFoundError()
    raidname = alias.raid()[raidname]
    
    api = f'https://cn.fflogs.com:443/v1/zones?api_key={API_KEY}'
    zones = json.loads(requests.get(api).content)
    for zone in zones:
        raid_id = zone['id']
        for encounter in zone['encounters']:
            if encounter['name'] == raidname:
                boss_id = encounter['id']
                return raidname, raid_id, boss_id
    
    raise RaidNotFoundError()


# dps 种类 (rdps or adps)
def find_dpskind(dpskind):
    dpskinds = alias.dpskind()
    if dpskind not in dpskinds:
        raise DpsKindError()
    return dpskinds[dpskind]


# 版本内部号
def find_versioncode(boss_name, version):
    if version not in alias.versioncode():
        raise VersionError()
    
    raidversions = alias.raidversion()[boss_name]
    if version not in raidversions:
        raise VersionError()
    
    return alias.versioncode()[version]
    

# 统计副本里所有职业的 dps
def stat_logs(raid_id, boss_id, rank, dpskind, region, versioncode):
    
    server = 'www' if region == '国际服' else 'cn'
    url = (f'https://{server}.fflogs.com/zone/statistics/table/'
           f'{raid_id}/dps/{boss_id}/101/8/{versioncode}/{rank}'
           '/1000/14/0/Any/Any/All/0/normalized/single'
           f'/0/-1/?keystone=15&dpstype={dpskind}')
    
    headers = {'referer': f'https://{server}.fflogs.com'}
    r = requests.get(url=url, headers=headers)
    
    dom = etree.HTML(r.content.decode('utf-8'))
    
    trs = dom.xpath('//tbody[1]/tr')
    
    logs = []
    for tr in trs:
        job = str(tr.xpath('./td[1]/text()')[0]).strip()
        dps = str(tr.xpath('./td[2]/text()')[0]).strip()
        logs.append((job, dps))
    
    return logs


@app.broadcast.receiver(GroupMessage, decorators=[MatchRegex(r'^/logs \S+ \S+ \S+ \S+ \S+')])
async def send_to_group(group: Group, messages: MessageChain):
    messages = messages.asSendable()
    
    args = util.getargs(messages)
    
    # 副本名 版本号 排名 dps计算方式 地区
    raid, rank, dpskind, region, version = (str(args[0]), str(args[1]), str(args[2]), str(args[3]), str(args[4]))
    try:
        
        if region != '国服' and region != '国际服':
            raise InvalidRegionError()
        
        if not rank.isdigit() or int(rank) < 0 or int(rank) > 100:
            raise InvalidRankError()
        
        name, raid_id, boss_id = find_raid(raid)
        dpskind = find_dpskind(dpskind)
        versioncode = find_versioncode(name, version)
        
        outmsgs = MessageChain.create(f'「{name}」 {dpskind} {rank} 排名线: \n')
        
        logs = stat_logs(raid_id, boss_id, rank, dpskind, region, versioncode)
        logs.sort(key=lambda x: (len(x[1]), x[1]), reverse=True)  # 倒序排序
        for log in logs:
            outmsgs.append(f'\t{log[0]}: {log[1]}\n')
        
        await app.sendGroupMessage(group, outmsgs)
    
    except RaidNotFoundError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: 未找到副本「{raid}」\n目前仅支持e1s-e12s、p1s-p4s'))
        return
    except DpsKindError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: 仅支持查询 rd(rdps) 或 ad(adps)'))
        return
    except InvalidRankError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: 排名必须为数字 (0 - 100)'))
        return
    except InvalidRegionError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: 地区必须是「国服」或「国际服」'))
        return
    except VersionError:
        await app.sendGroupMessage(group, MessageChain.create(f'错误: 非法版本号「{version}」, 仅支持 x.y 格式'))
        return


# 职业名称错误
class JobNotFoundError(BaseException):
    pass


# 副本名称错误
class RaidNotFoundError(BaseException):
    pass


# DPS 种类错误
class DpsKindError(BaseException):
    pass


# 不合法的排名
class InvalidRankError(BaseException):
    pass


# 不合法的地区 (only 国服 or 国际服)
class InvalidRegionError(BaseException):
    pass


# 版本号错误
class VersionError(BaseException):
    pass
