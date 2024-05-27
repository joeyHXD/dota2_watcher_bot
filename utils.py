import json
from config import player_info_file_path
from player import Player


class DOTA2HTTPError(Exception):
    pass


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
    
    with open(player_info_file_path, encoding="utf-8") as file:
        tmp = json.load(file)

    # 从json文件中读取数据，转换成Player对象
    for gid, player_list in tmp.items():
        data[gid] = []
        for info in player_list:
            player = Player()
            player.load_dict(info)
            data[gid].append(player)


def save_to_json(data):
    tmp = {}

    # 将Player对象转换成字典，存入json文件
    for gid, player_list in data.items():
        tmp[gid] = []
        for player in player_list:
            tmp[gid].append(player.to_dict())

    with open(player_info_file_path, "w", encoding="utf-8") as file:
        json.dump(tmp, file, indent=4, ensure_ascii=False)