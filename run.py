import time
import json
from .common import get_message_DOTA2, steam_id_convert_32_to_64, update_group_DOTA2_match_ID
from .player import PLAYER_LIST, player
from .DBOper import is_player_stored, insert_info, update_DOTA2_match_ID
from . import DOTA2
from hoshino import Service, priv

sv = Service('dota-poller', use_priv=priv.SUPERUSER, 
            enable_on_default=False, manage_priv=priv.SUPERUSER, visible=True,
            help_='添加刀塔玩家 [玩家昵称] [steam的id]\n如：添加刀塔玩家 萧瑟先辈 898754153\n')
fn = "./hoshino/modules/dota2_watcher_bot/"
item_dict = json.load(open(fn + "list.json", "r",encoding='utf-8',errors='ignore'))
bot = sv.bot

if len(PLAYER_LIST) < len(item_dict):
    for short_steamID, info in item_dict.items():
        short_steamID = int(short_steamID)
        long_steamID = steam_id_convert_32_to_64(short_steamID)
        try:
            last_DOTA2_match_ID = DOTA2.get_last_match_id_by_short_steamID(short_steamID)
        except DOTA2.DOTA2HTTPError:
            last_DOTA2_match_ID = "-1"
        # 如果数据库中没有这个人的信息, 则进行数据库插入
        if not is_player_stored(short_steamID):
            # 插入数据库
            insert_info(short_steamID, long_steamID, last_DOTA2_match_ID)
        # 如果有这个人的信息则更新其最新的比赛信息
        else:
            update_DOTA2_match_ID(short_steamID, last_DOTA2_match_ID)
        # 新建一个玩家对象, 放入玩家列表
        temp_player = player(short_steamID=short_steamID,
                             long_steamID=long_steamID,
                             last_DOTA2_match_ID=last_DOTA2_match_ID)
        PLAYER_LIST.append(temp_player)
group_dict = {}
# format of group_dict
# {
    # gid: [
        # player1,
        # player2
    # ]
# }
print('dota_test')
for i in PLAYER_LIST:
    steam_id = str(i.short_steamID)
    #print(steam_id, item_dict.get(steam_id, None))
    if item_dict.get(steam_id, None):
        for group_nickname in item_dict[steam_id]:
            gid, nickname = group_nickname
            gid = str(gid)
            #print("gid", gid, nickname)
            temp_player = player(short_steamID = i.short_steamID,
                             long_steamID = i.long_steamID,
                             last_DOTA2_match_ID = i.last_DOTA2_match_ID)
            temp_player.nickname = nickname
            if group_dict.get(gid, None):
                group_dict[gid].append(temp_player)
            else:
                group_dict[gid] = [temp_player]

@sv.scheduled_job('interval', seconds=60)
async def update():
    print('updating dota2')
    update_list = []
    check_update = False
    for gid,players in group_dict.items():
        gid = int(gid)
        if not sv.check_enabled(gid):
            break
        msg,new_update = get_message_DOTA2(players)
        for match_id, new_players in new_update.items():
            for player in new_players:
                update_list.append([player, match_id])
        if (msg!= None):
            check_update = True
            if len(msg) == 1:
                a = 1
                print(msg[0])
                await bot.send_group_msg(group_id=gid, message=msg[0])
            else:
                for match_result in msg:
                    a = 1
                    print(match_result)
                    await bot.send_group_msg(group_id=gid, message=match_result)
    if check_update:
        update_group_DOTA2_match_ID(update_list)
        
@sv.on_prefix('添加刀塔玩家')
async def add_dota2_player(bot, ev):
    cmd = ev.raw_message
    content=cmd.split()
    if(len(content)!=3):
        reply="请输入：添加刀塔玩家 [玩家昵称] [steam的id]\n如：添加刀塔玩家 萧瑟先辈 898754153\n"
        await bot.finish(ev, reply)
    nickname = content[1]
    short_steamID = int(content[2])
    long_steamID = steam_id_convert_32_to_64(short_steamID)
    try:
        last_DOTA2_match_ID = DOTA2.get_last_match_id_by_short_steamID(short_steamID)
    except DOTA2.DOTA2HTTPError:
        last_DOTA2_match_ID = "-1"
    # 如果数据库中没有这个人的信息, 则进行数据库插入
    gid = str(ev['group_id'])
    # 新建一个玩家对象, 放入玩家列表
    temp_player = player(short_steamID=short_steamID,
                         long_steamID=long_steamID,
                         last_DOTA2_match_ID=last_DOTA2_match_ID)
    temp_player.nickname = nickname
    reply = '似乎出现了意想不到的事情'
    if not is_player_stored(short_steamID):
        # 插入数据库
        insert_info(short_steamID, long_steamID, last_DOTA2_match_ID)
        if group_dict.get(gid, None):
            group_dict[gid].append(temp_player)
        else:
            group_dict[gid] = [temp_player]
        item_dict[str(short_steamID)] = [[int(gid), nickname]]
        reply="添加成功-路线1"
    else:
        if group_dict.get(gid, None):
            for i in group_dict[gid]:
                if i.short_steamID == short_steamID:
                    for info in item_dict[str(short_steamID)]:
                        if info[0] == int(gid):
                            info[1] = nickname
                    reply = f"已将你的昵称从{i.nickname}更新为{nickname}"
                    i.nickname = nickname
                    break
            if not reply:
                group_dict[gid].append(temp_player)
                item_dict[str(short_steamID)].append([int(gid), nickname])
                reply="添加成功-路线2"
        else:
            reply="添加成功-路线3"
            group_dict[gid] = [temp_player]
            item_dict[str(short_steamID)].append([int(gid), nickname])
    temp_player = player(short_steamID=short_steamID,
                     long_steamID=long_steamID,
                     last_DOTA2_match_ID=last_DOTA2_match_ID)
    PLAYER_LIST.append(temp_player)
    with open(fn + "list.json", "w",encoding='utf-8') as config_file:
        json.dump(item_dict, config_file, ensure_ascii=False, indent=4)
    await bot.send(ev, reply)
    