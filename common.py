from . import DOTA2
from .DBOper import update_DOTA2_match_ID
from .player import PLAYER_LIST

def steam_id_convert_32_to_64(short_steamID):
    return short_steamID + 76561197960265728

def steam_id_convert_64_to_32(long_steamID):
    return long_steamID - 76561197960265728

def update_DOTA2(players):
    result = {}
    for player in players:
        try:
            match_id = DOTA2.get_last_match_id_by_short_steamID(player.short_steamID)
        except DOTA2.DOTA2HTTPError:
            continue
        #print(i.short_steamID, i.last_DOTA2_match_ID, match_id)
        if match_id != player.last_DOTA2_match_ID:
            print(match_id, 'and', player.last_DOTA2_match_ID)
            if result.get(match_id, 0) != 0:
                result[match_id].append(player)
            else:
                result.update({match_id: [player]})
            # 更新数据库的last_DOTA2_match_id字段
            #update_DOTA2_match_ID(i.short_steamID, match_id)
            # 更新列表
            player.last_DOTA2_match_ID = match_id
    return result

def get_message_DOTA2(players):
    #glist = [player1, player2]
    # 格式: { match_id1: [player1, player2, player3], match_id2: [player1, player2]}
    print("getting message")
    result = update_DOTA2(players)
    msg = []
    for match_id in result:
        if len(result[match_id]) > 1:
            txt = DOTA2.generate_party_message(match_id=match_id, player_list=result[match_id]);
            if (txt != 0):
                msg.append(txt)
        elif len(result[match_id]) == 1:
            txt = DOTA2.generate_solo_message(match_id=match_id, player_obj=result[match_id][0])
            if (txt != 0):
                msg.append(txt)
    return msg, result

def update_group_DOTA2_match_ID(update):
    for player in PLAYER_LIST:
        for updated_player, match_id in update:
            if player.short_steamID == updated_player.short_steamID:
                player.last_DOTA2_match_ID = match_id
                update_DOTA2_match_ID(player.short_steamID, match_id)
                break
