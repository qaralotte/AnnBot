# ff14 的别名黑话

# 根据区服定位所在的服务器
def location():
    return {
        **dict.fromkeys(['陆行鸟', '鸟', '鸟区', '陆行鸟区'], 'LaNuoXiYa'),
        **dict.fromkeys(['猫小胖', '猫', '猫区', '猫小胖区'], 'HaiMaoChaWu'),
        **dict.fromkeys(['莫古力', '猪', '猪区', '莫古力区'], 'FuXiaoZhiJian'),
        **dict.fromkeys(['豆豆柴', '狗', '狗区', '豆豆柴区'], 'ShuiJingTa'),
    }


# 职业别名
def job():
    return {
        **dict.fromkeys(['黑', '黑魔', '黑膜', '黑魔法', '黑魔法师'], '黑魔法师'),
        **dict.fromkeys(['侍', '盘', '武士', '盘子'], '武士'),
        **dict.fromkeys(['僧', '武僧'], '武僧'),
        **dict.fromkeys(['龙', '龙骑', '龙骑士'], '龙骑士'),
        **dict.fromkeys(['忍', 'ninja', '忍者'], '忍者'),
        **dict.fromkeys(['龙', '龙骑', '龙骑士'], '龙骑士'),
        **dict.fromkeys(['镰', '镰刀', '钐镰客'], '钐镰客'),
        **dict.fromkeys(['召', '召唤', '召唤师'], '召唤师'),
        **dict.fromkeys(['机', '机工', '手枪哥', '机工士'], '机工士'),
        **dict.fromkeys(['赤', '赤魔', '赤膜', '赤魔法师'], '赤魔法师'),
        **dict.fromkeys(['诗', '诗人', '吟游诗人'], '吟游诗人'),
        **dict.fromkeys(['舞', '舞娘', '舞者'], '舞者'),
        **dict.fromkeys(['暗', '暗骑', '黑骑', 'dk', 'DK', '暗黑骑士'], '暗黑骑士'),
        **dict.fromkeys(['枪', '绝枪', '枪刃', '绝枪战士'], '绝枪战士'),
        **dict.fromkeys(['战', '战士'], '战士'),
        **dict.fromkeys(['骑', '骑士'], '骑士'),
        **dict.fromkeys(['贤', '贤者'], '贤者'),
        **dict.fromkeys(['学', '学者'], '学者'),
        **dict.fromkeys(['白', '白魔', '白膜', '白魔法师'], '白魔法师'),
        **dict.fromkeys(['占', '占星', '占星术士'], '占星术士'),
    }


# 副本简写
def raid():
    return {
        **dict.fromkeys(['e1s', 'E1S'], '至尊伊甸'),
        **dict.fromkeys(['e2s', 'E2S'], '虚空行者'),
        **dict.fromkeys(['e3s', 'E3S'], '利维亚桑'),
        **dict.fromkeys(['e4s', 'E4S'], '泰坦'),
        **dict.fromkeys(['e5s', 'E5S'], '拉姆'),
        **dict.fromkeys(['e6s', 'E6S'], '伊弗利特与迦楼罗'),
        **dict.fromkeys(['e7s', 'E7S'], '暗黑心象'),
        **dict.fromkeys(['e8s', 'E8S'], '希瓦'),
        **dict.fromkeys(['e9s', 'E9S', '云妈', '暗黑之云'], '暗黑之云'),
        **dict.fromkeys(['e10s', 'E10S', '大狗', '臭狗', '影之王'], '影之王'),
        **dict.fromkeys(['e11s', 'E11S', '爹神', '塔其q', '绝命战士'], '绝命战士'),
        **dict.fromkeys(['e12s门神', 'E12S门神', '椰蛋树', '伊甸之约'], '伊甸之约'),
        **dict.fromkeys(['e12s本体', 'E12S本体', '盖娅', '暗之巫女'], '暗之巫女'),
        **dict.fromkeys(['p1s', 'P1S'], '埃里克特翁尼亚斯'),
        **dict.fromkeys(['p2s', 'P2S'], '鱼尾海马怪'),
        **dict.fromkeys(['p3s', 'P3S'], '菲尼克司'),
        **dict.fromkeys(['p4s门神', 'P4S门神'], '赫斯珀洛斯'),
        **dict.fromkeys(['p4s本体', 'P4S本体'], '赫斯珀洛斯II'),
    }


# dps 计算方式
def dpskind():
    return {
        **dict.fromkeys(['rd', 'rdps', 'RD', 'RDPS'], 'rdps'),
        **dict.fromkeys(['ad', 'adps', 'AD', 'ADPS'], 'adps'),
    }


# 副本对应版本
def raidversion():
    return {
        **dict.fromkeys(['至尊伊甸', '虚空行者', '利维亚桑', '泰坦'], ['5.0', '5.1']),
        **dict.fromkeys(['拉姆', '伊弗利特与迦楼罗', '暗黑心象', '希瓦'], ['5.2', '5.3']),
        **dict.fromkeys(['暗黑之云', '影之王', '绝命战士', '伊甸之约', '暗之巫女'], ['5.4', '5.5']),
        **dict.fromkeys(['埃里克特翁尼亚斯', '鱼尾海马怪', '菲尼克司', '赫斯珀洛斯', '赫斯珀洛斯II'], ['6.0', '6.1']),
    }


# 版本内部号
def versioncode():
    return {
        **dict.fromkeys(['6.0'], '1'),
        **dict.fromkeys(['5.0', '5.2', '5.4'], '3'),
        **dict.fromkeys(['5.1'], '5'),
        **dict.fromkeys(['6.1'], '7'),
        **dict.fromkeys(['5.3', '5.5'], '9'),
    }
