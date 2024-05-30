import json
import os
from .player import Player

class DOTA2HTTPError(Exception):
    pass

# 加载配置文件
config_path = "./hoshino/modules/dota2_watcher_bot/config.py"

class Config:
    def __init__(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                "DOTA2_WATCHER_BOT: config.py not found. Please create config.py based on README and default_config.py."
            )
        else:
            from .config import (
                api_key,
                proxies,
                timeout,
                player_info_file_path,
                all_nickname,
                game_mode,
                benchmark_threshold
            )
            self._api_key = api_key
            self._proxies = proxies
            self._timeout = timeout
            self._player_info_file_path = player_info_file_path
            self._all_nickname = all_nickname
            self._game_mode = game_mode
            self._benchmark_threshold = benchmark_threshold

    @property
    def api_key(self):
        return self._api_key

    @property
    def proxies(self):
        return self._proxies

    @property
    def timeout(self):
        return self._timeout

    @property
    def player_info_file_path(self):
        return self._player_info_file_path

    @property
    def all_nickname(self):
        return self._all_nickname

    @property
    def game_mode(self):
        return self._game_mode

    @property
    def benchmark_threshold(self):
        return self._benchmark_threshold

config = Config(config_path)

def prompt_error(response, url):
    if response.status_code >= 400:
        if response.status_code == 401:
            raise DOTA2HTTPError("未经授权的请求 401。请验证 API 密钥。")
        if response.status_code == 503:
            raise DOTA2HTTPError("服务器繁忙或您超出了限制。请等待 30 秒后重试。")
        raise DOTA2HTTPError("无法获取数据：%s。URL：%s" % (response.status_code, url))


def load_from_json():
    """
    data = {
        group_id: [Player1, Player2]
    }
    """
    data = {}

    if not os.path.exists(config.player_info_file_path):
        # Create an empty playerInfo.json if it doesn't exist
        with open(config.player_info_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    # Open and read the file
    with open(config.player_info_file_path, 'r', encoding='utf-8') as file:
        tmp = json.load(file)

    # 从json文件中读取数据，转换成Player对象
    for gid, player_list in tmp.items():
        data[gid] = []
        for info in player_list:
            player = Player()
            player.load_dict(info)
            data[gid].append(player)
    return data


def save_to_json(data):
    tmp = {}

    # 将Player对象转换成字典，存入json文件
    for gid, player_list in data.items():
        tmp[gid] = []
        for player in player_list:
            tmp[gid].append(player.to_dict())

    with open(config.player_info_file_path, "w", encoding="utf-8") as file:
        json.dump(tmp, file, indent=4, ensure_ascii=False)