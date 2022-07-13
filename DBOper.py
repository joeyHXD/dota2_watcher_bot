import sqlite3
from .player import player, PLAYER_LIST

conn = sqlite3.connect('./hoshino/modules/dota2_watcher_bot/playerInfo.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS playerInfos(
            short_steamID           INT,
            long_steamID            INT,
            last_DOTA2_match_ID     INT,
            DOTA2_score             TEXT)""")
conn.commit()

cursor = c.execute("SELECT * from playerInfos")
for row in cursor:
    player_obj = player(short_steamID=row[0],
                        long_steamID=row[1],
                        last_DOTA2_match_ID=row[2])
    player_obj.DOTA2_score = row[3]
    PLAYER_LIST.append(player_obj)

def update_DOTA2_match_ID(short_steamID, last_DOTA2_match_ID):
    conn.execute("UPDATE playerInfos SET last_DOTA2_match_ID='{}' "
              "WHERE short_steamID={}".format(last_DOTA2_match_ID, short_steamID))
    conn.commit()

def insert_info(short_steamID, long_steamID, last_DOTA2_match_ID):
    c.execute("INSERT INTO playerInfos (short_steamID, long_steamID, last_DOTA2_match_ID) "
              "VALUES ({}, {}, {})"
              .format(short_steamID, long_steamID, last_DOTA2_match_ID))
    conn.commit()

def is_player_stored(short_steamID):
    c.execute("SELECT * FROM playerInfos WHERE short_steamID=={}".format(short_steamID))
    if len(c.fetchall()) == 0:
        return False
    return True

