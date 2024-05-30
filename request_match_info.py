from .utils import (
    config,
    DOTA2HTTPError,
    prompt_error
)
from hoshino import aiorequests

# 报错请检查是否配置了config.py
api_key = config.api_key
proxies = config.proxies
timeout = config.timeout


async def request_match_history(player, api_key):
    url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/?key={}' \
        '&account_id={}&matches_requested=1'.format(api_key, player.short_steamID)
    try:
        response = await aiorequests.get(url, timeout=timeout, proxies=proxies)
    except:
        raise DOTA2HTTPError(f"{timeout}秒内无法连接到网站，建议检查网络，或者尝试使用代理服务器")
    prompt_error(response, url)
    match = response.json()
    if match["result"]["status"] == 15:
        raise DOTA2HTTPError(f"{player.nickname}的战绩被隐藏了,无法获取")
    try:
        match_id = match["result"]["matches"][0]["match_id"]
    except:
        raise DOTA2HTTPError(f"无法获取{player.nickname}的最近比赛ID, 请检查{url}")
    return match_id


async def request_match_info_steam(match_id, api_key):
    # API文档: https://wiki.teamfortress.com/wiki/WebAPI#Dota_2
    url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/' \
        '?key={}&match_id={}'.format(api_key, match_id)

    try:
        response = await aiorequests.get(url, timeout=timeout, proxies=proxies)
    except:
        raise DOTA2HTTPError(f"{timeout}秒内无法连接到网站，建议检查网络，或者尝试使用代理服务器")

    # 根据status code报错
    prompt_error(response, url)
    # 7.36 版本后，此API无法获取到比赛结果，需要使用openDota的API
    try:
        match = response.json()
        match_info = match.get("result", None)
    except:
        raise DOTA2HTTPError("DOTA2开黑战报生成失败")
    return match_info


async def request_match_info_opendota(match_id, api_key=None):
    # 无API的免费版每天仅2000次访问，如果需要更多请自行申请API
    # 详情请访问：https://www.opendota.com/api-keys
    url = f"https://api.opendota.com/api/matches/{match_id}"

    try:
        response = await aiorequests.get(url, timeout=timeout, proxies=proxies)
    except:
        raise DOTA2HTTPError(f"{timeout}秒内无法连接到网站，建议检查网络，或者尝试使用代理服务器")

    try:
        match_info = await response.json()
    except:
        raise DOTA2HTTPError("DOTA2开黑战报生成失败")
    return match_info