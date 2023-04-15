import time
import json
from .player import Player
from . import DOTA2
from hoshino import Service, priv, aiorequests
from .text2img import image_draw

sv = Service(
            'dota-poller2',
            use_priv=priv.SUPERUSER,
            enable_on_default=False,
            manage_priv=priv.SUPERUSER,
            visible=True,
            help_='添加刀塔玩家 [玩家昵称] [steam的id]\n如：添加刀塔玩家 萧瑟先辈 898754153\n'
    )

# 这里替换成你自己的API
# http://steamcommunity.com/dev/apikey
api_key = ""
proxies = {"http": "", "https": ""}
class DOTA2HTTPError(Exception):
    pass

def steam_id_convert_32_to_64(short_steamID):
    return short_steamID + 76561197960265728
bot = sv.bot
data = {}
fn = "./hoshino/modules/dota2_watcher_bot/playerInfo.json"

with open(fn, encoding="utf-8") as file:
    tmp = json.load(file)

for gid, player_list in tmp.items():
    data[gid] = []
    for info in player_list:
        player = Player()
        player.load_dict(info)
        data[gid].append(player)

def save_to_json():
    tmp = {}
    for gid, player_list in data.items():
        tmp[gid] = []
        for player in player_list:
            tmp[gid].append(player.to_dict())
    with open(fn, "w", encoding="utf-8") as file:
        json.dump(tmp, file, indent=4, ensure_ascii=False)

@sv.scheduled_job('interval', seconds=60)
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
            short_steamID = player.short_steamID
            try:
                url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/?key={}' \
                  '&account_id={}&matches_requested=1'.format(api_key, short_steamID)
                try:
                    response = await aiorequests.get(url, timeout=20, proxies=proxies)
                except Exception as e:
                    sv.logger.exception("20秒内无法连接到网站，建议检查网络，或者尝试使用代理服务器")
                    raise e
                prompt_error(response, url)
                match = await response.json()
                if match["result"]["status"] == 15:
                    sv.logger.exception(f"{player.nickname}的战绩被隐藏了,无法获取")
                    continue
                try:
                    match_id = match["result"]["matches"][0]["match_id"]
                except Exception as e:
                    sv.logger.exception(e)
                if match_id != player.last_DOTA2_match_ID:
                    if match_id not in result:
                        result[match_id] = [player]
                    else:
                        result[match_id].append(player)
                    player.last_DOTA2_match_ID = match_id
            except DOTA2HTTPError as e:
                sv.logger.exception(e)
                continue
            except Exception as e:
                sv.logger.exception(e)
        messages = []
        for match_id, match_player_list in result.items():
            try:
                url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/' \
                  '?key={}&match_id={}'.format(api_key, match_id)
                try:
                    response = await aiorequests.get(url, timeout=20, proxies=proxies)
                except Exception as e:
                    sv.logger.exception("20秒内无法连接到网站，建议检查网络，或者尝试使用代理服务器")
                    raise e
                prompt_error(response, url)
                match = await response.json()
                try:
                    match_info = match["result"]
                except KeyError:
                    raise DOTA2HTTPError("Response Error: Key Error")
                except IndexError:
                    raise DOTA2HTTPError("Response Error: Index Error")
            except DOTA2HTTPError:
                raise DOTA2HTTPError("DOTA2开黑战报生成失败")
            txt = DOTA2.generate_message(match_info, match_player_list)
            if txt:
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
                    await bot.send_group_msg(group_id=gid, message="图片发送失败")
                    await bot.send_group_msg(group_id=gid, message=reply)
    save_to_json()
    sv.logger.info("done")

def prompt_error(response, url):
    if response.status_code >= 400:
        if response.status_code == 401:
            raise DOTA2HTTPError("Unauthorized request 401. Verify API key.")
        if response.status_code == 503:
            raise DOTA2HTTPError("The server is busy or you exceeded limits. Please wait 30s and try again.")
        raise DOTA2HTTPError("Failed to retrieve data: %s. URL: %s" % (response.status_code, url))

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
    gid = str(ev['group_id'])
    # 新建一个玩家对象, 放入玩家列表
    temp_player = Player(short_steamID=short_steamID,
                         nickname=nickname,
                         last_DOTA2_match_ID=0)
    temp_player.nickname = nickname
    if gid not in data:
        data[gid] = []
    for player in data[gid]:
        if player.short_steamID == short_steamID:
            player.nickname = nickname
            is_new_player = False
            reply = "玩家已存在，更新昵称"
            break
    else:
        reply = "玩家添加成功"
        data[gid].append(temp_player)
    save_to_json()
    await bot.send(ev, reply)
    