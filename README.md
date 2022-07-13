# DOTA2的处刑BOT,hoshino插件版
魔改自： https://github.com/greenhaha/dota2_csgo_watcher_bot

## 介绍
在群友打完一把游戏后, bot会向群里更新这局比赛的数据

DOTA2的数据来自于V社的官方API, 每日请求数限制100,000次

YYGQ的文来自于[dota2_watcher](https://github.com/unilink233/dota2_watcher)

## 安装指南
1.clone本插件： 在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

`git clone https://github.com/joeyHXD/dota2_watcher_bot.git`

3.启用模块

在 HoshinoBot\hoshino\config\bot.py 文件的 MODULES_ON 加入 'Dota2_watcher_bot'

4.在(http://steamcommunity.com/dev/apikey)申请你的steam API key, 修改`DOTA2.py`中的`api_key`

然后重启 HoshinoBot

5.添加玩家： '添加刀塔玩家 [玩家昵称] [steam的id]'

如： 添加刀塔玩家 萧瑟先辈 898754153

- 走过路过点个star吧

## 运行效果
具体可以看 https://github.com/greenhaha/dota2_csgo_watcher_bot