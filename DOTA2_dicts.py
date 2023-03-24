# 可以在这里添加新的阴阳怪气, {}为昵称位置

# 单排的阴阳怪气
WIN_NEGATIVE = [
    '{}侥幸赢得了比赛',
    '{}走狗屎运赢得了比赛',
    '{}躺赢了比赛',
    '{}打团都没来, 队友4V5赢得了比赛.'
]

WIN_POSTIVE = [
    '{}带领团队走向了胜利',
    '{}暴打对面后赢得了胜利',
    '{} CARRY全场赢得了胜利',
    '{}把对面当猪宰了, 赢得了胜利.',
    '{}又赢了, 这游戏就是这么枯燥, 且乏味.',
]

LOSE_NEGATIVE = [
    '{}被人按在地上摩擦, 输掉了这场比赛',
    '{}悲惨地输掉了比赛',
    '{}头都被打歪了, 心态爆炸地输掉了比赛.',
    '{}捕鱼被鱼吃了, 输掉了比赛.',
    '{}打的是个几把.'
]

LOSE_POSTIVE = [
    '{}无力回天输掉了比赛.',
    '{}尽力了, 但还是输了比赛.',
    '{}背靠世界树, 虽败犹荣.',
    '{}带不动队友, 输了比赛',
    '{}又输了, 很难受, 宁愿输的是我.',
]

GAME_MODE = {
    0: "No Game Mode",
    1: "全英雄选择",
    2: "队长模式",
    3: "随机征召",
    4: "小黑屋",
    5: "全部随机",
    7: "万圣节活动",
    8: "反队长模式",
    9: "贪魔活动",
    10: "教程",
    11: "中路模式",
    12: "生疏模式",
    13: "新手模式",
    14: "Compendium Matchmaking",
    15: "自定义游戏",
    16: "队长征召",
    17: "平衡征召",
    18: "OMG",
    19: "活动模式",
    20: "全英雄死亡随机",
    21: "中路SOLO",
    22: "全英雄选择",
    23: "加速模式"}


LOBBY = {
    -1: "非法ID",
    0: "普通匹配",
    1: "练习",
    2: "锦标赛",
    3: "教程",
    4: "合作对抗电脑",
    5: "组排模式",
    6: "单排模式",
    7: "天梯匹配",
    8: "中路SOLO"
}


# 服务器ID列表
AREA_CODE = {
    111: "美国西部",
    112: "美国西部",
    114: "美国西部",
    121: "美国东部",
    122: "美国东部",
    123: "美国东部",
    124: "美国东部",
    131: "欧洲西部",
    132: "欧洲西部",
    133: "欧洲西部",
    134: "欧洲西部",
    135: "欧洲西部",
    136: "欧洲西部",
    142: "南韩",
    143: "南韩",
    151: "东南亚",
    152: "东南亚",
    153: "东南亚",
    161: "中国",
    163: "中国",
    171: "澳大利亚",
    181: "俄罗斯",
    182: "俄罗斯",
    183: "俄罗斯",
    184: "俄罗斯",
    185: "俄罗斯",
    186: "俄罗斯",
    191: "欧洲东部",
    192: "欧洲东部",
    200: "南美洲",
    202: "南美洲",
    203: "南美洲",
    204: "南美洲",
    211: "非洲南部",
    212: "非洲南部",
    213: "非洲南部",
    221: "中国",
    222: "中国",
    223: "中国",
    224: "中国",
    225: "中国",
    231: "中国",
    236: "中国",
    242: "智利",
    251: "秘鲁",
    261: "印度"}


# 英雄昵称
HEROES_LIST_CHINESE = {
    1: '敌法师',
    2: '斧王',
    3: '痛苦之源',
    4: '血魔',
    5: '冰女',
    6: '小黑',
    7: '撼地神牛',
    8: '奶棒人',
    9: '白虎',
    10: '水人',
    11: '影魔王',
    12: '幻影长矛手',
    13: '帕克',
    14: '屠夫',
    15: '电魂',
    16: '沙王',
    17: '蓝猫',
    18: '斯温',
    19: '小小',
    20: '复仇之魂',
    21: '风行',
    22: '宙斯',
    23: '船长',
    25: '火女',
    26: '莱恩',
    27: '小歪',
    28: '大鱼',
    29: '潮汐',
    30: '巫医',
    31: '巫妖',
    32: '力丸',
    33: '谜团',
    34: '修补匠',
    35: '火枪',
    36: 'NEC',
    37: '术士',
    38: '兽王',
    39: '女王',
    40: '剧毒',
    41: '虚空',
    42: '骷髅王',
    43: '死亡先知',
    44: '幻影刺客',
    45: '帕格纳',
    46: '圣堂刺客',
    47: '毒龙',
    48: 'Luna',
    49: '龙骑士',
    50: '戴泽',
    51: '发条',
    52: '拉席克',
    53: "先知",
    54: '小狗',
    55: '黑暗贤者',
    56: '克林克兹',
    57: '全能',
    58: '小鹿',
    59: '哈斯卡',
    60: '夜魔',
    61: '蜘蛛',
    62: '赏金',
    63: '蚂蚁',
    64: '双头龙',
    65: '蝙蝠',
    66: '陈',
    67: '幽鬼',
    68: '冰魂',
    69: 'Doom',
    70: '拍拍熊',
    71: '白牛',
    72: '飞机',
    73: '炼金',
    74: '卡尔',
    75: '沉默',
    76: '黑鸟',
    77: '狼人',
    78: '兽王',
    79: '毒狗',
    80: '德鲁伊',
    81: '混沌骑士',
    82: '米波',
    83: '大树',
    84: '蓝胖',
    85: '尸王',
    86: '拉比克',
    87: '萨尔',
    88: '小强',
    89: '小娜迦',
    90: '光法',
    91: '小精灵',
    92: '死灵龙',
    93: '小鱼',
    94: '美杜莎',
    95: '巨馍蘸酱',
    96: '人马',
    97: '猛犸',
    98: '伐木机',
    99: '钢背兽',
    100: '海民',
    101: '天怒',
    102: '亚巴顿',
    103: '大牛',
    104: '军团',
    105: '炸弹人',
    106: '火猫',
    107: '土猫',
    108: '大屁股',
    109: '恐怖利刃',
    110: '凤凰',
    111: '神谕者',
    112: '冰龙',
    113: '电狗',
    114: '大圣',
    119: '小仙女',
    120: '滚滚',
    121: '墨客',
    123: '小松鼠',
    126: '紫猫',
    128: '老奶奶',
    129: '马尔斯',
    135: '破晓晨星',
    136: '玛西',
    137: '兽'
}