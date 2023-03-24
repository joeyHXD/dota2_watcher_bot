from .DOTA2_dicts import *
import random
import time

# 根据slot判断队伍, 返回1为天辉, 2为夜魇
def get_team_by_slot(slot):
    if slot < 100:
        return 1
    else:
        return 2

# 接收某局比赛的玩家列表, 生成开黑战报
# 参数为玩家对象列表和比赛ID
def generate_message(match_info, player_list):
    # 比赛模式
    mode_id = match_info["game_mode"]
    if mode_id in (15, 19):  # 各种活动模式不通报
        return 0
    mode = GAME_MODE[mode_id] if mode_id in GAME_MODE else '未知'

    lobby_id = match_info['lobby_type']
    lobby = LOBBY[lobby_id] if lobby_id in LOBBY else '未知'

    # 更新玩家对象的比赛信息
    for player in player_list:
        for player_game_info in match_info['players']:
            if player.short_steamID == player_game_info['account_id']:
                player.load_player_info(player_game_info)
                break

    # 队伍信息
    team = player_list[0].stats["dota2_team"]
    teammates_info = list(filter(lambda x: get_team_by_slot(x['player_slot']) == team, match_info['players']))
    team_damage = sum([player["hero_damage"] for player in teammates_info])
    team_kills = sum([player["kills"] for player in teammates_info])
    team_deaths = sum([player["deaths"] for player in teammates_info])

    win = False
    if match_info['radiant_win'] and team == 1:
        win = True
    elif not match_info['radiant_win'] and team == 2:
        win = True
    if len(player_list) == 1:
        nicknames = player_list[0].nickname
    else:
        nicknames = ', '.join([player.nickname for player in player_list[:-1]])
        nicknames = '和'.join([nicknames, player_list[-1].nickname])

    top_kda = max(player.stats["kda"] for player in player_list)

    if (win and top_kda > 10) or (not win and top_kda > 6):
        postive = True
    elif (win and top_kda < 4) or (not win and top_kda < 1):
        postive = False
    else:
        postive = (random.randint(0, 1) == 1)

    print_str = ''
    if win and postive:
        print_str += random.choice(WIN_POSTIVE).format(nicknames) + '\n'
    elif win and not postive:
        print_str += random.choice(WIN_NEGATIVE).format(nicknames) + '\n'
    elif not win and postive:
        print_str += random.choice(LOSE_POSTIVE).format(nicknames) + '\n'
    else:
        print_str += random.choice(LOSE_NEGATIVE).format(nicknames) + '\n'

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(match_info['start_time']))
    duration = match_info['duration']
    print_str += f"开始时间: {start_time}\n"
    print_str += f"持续时间: {duration // 60}分{duration % 60}秒\n"
    print_str += f"游戏模式: [{mode}/{lobby}]\n"

    for player in player_list:
        nickname = player.nickname
        kill, death, assist, kda, dota2_team, hero, last_hit, damage, gpm, xpm = player.stats.values()
        #以后出新英雄就把编号名字加进dict里，这序号貌似有时还会变，如果出了变化麻烦提issue或者PR，毕竟本人玩的英雄很少
        hero = HEROES_LIST_CHINESE.get(hero, f"{hero}不知道什么鬼")
        damage_rate = 0 if team_damage == 0 else (100 * (float(damage) / team_damage))
        participation = 0 if team_kills == 0 else (100 * float(kill + assist) / team_kills)
        deaths_rate = 0 if team_deaths == 0 else (100 * float(death) / team_deaths)

        print_str += f"{nickname}使用{hero},\n"
        print_str += f"KDA: {kda:.2f}[{kill}/{death}/{assist}],\n"
        print_str += f"GPM/XPM: {gpm}/{xpm},\n"
        print_str += f"补刀数: {last_hit},\n"
        print_str += f"总伤害: {damage}({damage_rate:.2f}%),\n"
        print_str += f"参战率: {participation:.2f}%,\n"
        print_str += f"参葬率: {deaths_rate}%\n"
    # 我担心发网站bot容易寄
    # print_str += "战绩详情: https://cn.dotabuff.com/matches/{}".format(match_id)

    return(print_str)
