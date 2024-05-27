# 这里替换成你自己的API
# http://steamcommunity.com/dev/apikey
api_key = "FF14D2C1C53E2C92ADA36FA1B75B2A1F"

# API被墙了，国内用户可能需要代理服务器
proxies = {"http": "", "https": ""}

# 超时时间，单位秒
timeout = 20

# 保存玩家信息的json文件路径
player_info_file_path = "./hoshino/modules/dota2_watcher_bot/playerInfo.json"

# 如何呼叫全体
all_nickname = "全体"

# 不播报的游戏模式，看DOTA2_dicts.py里的GAME_MODE
game_mode = [15, 19] # 15是自定义游戏，19是活动模式