from .player import Player
from . import DOTA2
from hoshino import Service, priv
from .text2img import image_draw
from .utils import (
    config,
    load_from_json,
    save_to_json
)
from .request_match_info import request_match_info_opendota, request_match_history

# 报错请检查是否配置了config.py
api_key = config.api_key
proxies = config.proxies
timeout = config.timeout
all_nickname = config.all_nickname

sv = Service(
            'dota-poller2',
            use_priv=priv.SUPERUSER,
            enable_on_default=False,
            manage_priv=priv.SUPERUSER,
            visible=True,
            help_='添加刀塔玩家 [玩家昵称] [steam的id]\n如：添加刀塔玩家 萧瑟先辈 898754153\n'
    )
bot = sv.bot
data = load_from_json()


@sv.scheduled_job('interval', seconds=120)
async def update():
    sv.logger.info("updating")
    for gid, player_list in data.items():
        if not sv.check_enabled(int(gid)):
            continue
        result = {}
        """
        result = {
            match_id_1 : [Player1, Player2]
            match_id_2 : [Player3]
        }
        """
        for player in player_list:
            if not player.display_recent_match:
                # 不显示比赛
                continue
            try:
                # 获取最近一场比赛的ID
                match_id = await request_match_history(player, api_key)
            except Exception as e:
                sv.logger.exception(e)
                continue
            if match_id != player.last_DOTA2_match_ID:
                # 如果有新比赛，加入到result
                if match_id not in result:
                    result[match_id] = [player]
                else:
                    result[match_id].append(player)
                # player.last_DOTA2_match_ID = match_id
        messages = []
        for match_id, match_player_list in result.items():
            try:
                # 获取比赛信息
                match_info = await request_match_info_opendota(match_id)
                # match_info = await DOTA2.request_match_info_steam(match_id, api_key)
            except Exception as e:
                sv.logger.exception(e)
                continue
            if match_info:
                for player in match_player_list:
                    # 更新last_DOTA2_match_ID
                    player.last_DOTA2_match_ID = match_id
                txt = DOTA2.generate_message(match_info, match_player_list)
                messages.append(txt)
        if messages:
            data[gid] = player_list
            for msg in messages:
                sv.logger.info(msg)
                pic = image_draw(msg)
                try:
                    await bot.send_group_msg(group_id=gid, message=f'[CQ:image,file={pic}]')
                except:
                    sv.logger.info(f"临时会话图片发送失败")
                    # await bot.send_group_msg(group_id=gid, message="图片发送失败")
                    await bot.send_group_msg(group_id=gid, message=msg)
    save_to_json(data)
    sv.logger.info("done")


@sv.on_prefix('添加刀塔玩家')
async def add_dota2_player(bot, ev):
    cmd = ev.raw_message
    content=cmd.split()
    if(len(content)!=3):
        reply="请输入：添加刀塔玩家 [玩家昵称] [steam的id]\n如：添加刀塔玩家 萧瑟先辈 898754153\n"
        await bot.finish(ev, reply)
    nickname = content[1]
    short_steamID = int(content[2])
    gid = str(ev['group_id'])
    # 新建一个玩家对象, 放入玩家列表
    if nickname == all_nickname:
        await bot.finish(ev, f"{all_nickname}不是一个合法的昵称")
    temp_player = Player(short_steamID=short_steamID,
                         nickname=nickname,
                         last_DOTA2_match_ID=0)
    temp_player.nickname = nickname
    if gid not in data:
        data[gid] = []
    for player in data[gid]:
        if player.short_steamID == short_steamID:
            player.nickname = nickname
            reply = "玩家已存在，更新昵称"
            break
    else:
        reply = "玩家添加成功"
        data[gid].append(temp_player)
    save_to_json(data)
    await bot.send(ev, reply)


@sv.on_rex(r'关闭(\S+)的群播报')
async def close_broadcast(bot, ev):
    gid = str(ev['group_id'])
    if gid not in data:
        await bot.finish(ev, "当前群组没有添加任何玩家")
    player_name = ev['match'].group(1)
    if player_name == all_nickname:
        # 全体关闭
        for player in data[gid]:
            player.display_recent_match = False
    else:
        # 单个关闭
        for player in data[gid]:
            if player.nickname == player_name:
                player.display_recent_match = False
                await bot.finish(ev, f"已关闭{player_name}的播报")
        await bot.finish(ev, "未找到该玩家")


@sv.on_rex(r'开启(\S+)的群播报')
async def open_broadcast(bot, ev):
    gid = str(ev['group_id'])
    if gid not in data:
        await bot.finish(ev, "当前群组没有添加任何玩家")
    player_name = ev['match'].group(1)
    if player_name == all_nickname:
        # 全体开启
        for player in data[gid]:
            player.display_recent_match = True
    else:
        # 单个开启
        for player in data[gid]:
            if player.nickname == player_name:
                player.display_recent_match = True
                await bot.finish(ev, f"已开启{player_name}的播报")
        await bot.finish(ev, "未找到该玩家")