# DOTA2的处刑BOT,hoshino插件版
魔改自： https://github.com/greenhaha/dota2_csgo_watcher_bot

在此之上添加了直接从QQ群添加刀塔玩家的功能, 以及对每个QQ群分别播放各自的战绩

## 介绍
在群友打完一把游戏后, bot会向群里更新这局比赛的数据

DOTA2的数据来自于v社官方API(每日请求数限制100,000次)和openDota的API

openDota免费版每日请求数限制2,000次，不需要API key

这是一个hoshino机器人的插件，需要添加到hoshino本体里才能运行

搭建hoshino机器人请参考[Hoshino开源Project](https://github.com/Ice-Cirno/HoshinoBot)

添加玩家： `添加刀塔玩家 [玩家昵称] [steam的id]`

## 安装指南
1. clone本插件： 在 `HoshinoBot\hoshino\modules` 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/joeyHXD/dota2_watcher_bot.git
    ```
2. 在 `HoshinoBot\hoshino\config\bot.py` 文件的 `MODULES_ON` 加入 `dota2_watcher_bot,`
3. 将`default_config.py`复制并重命名为`config.py`
    - `cp default_config.py config.py`
4. 在 http://steamcommunity.com/dev/apikey 申请你的steam API key, 修改`config.py`中的`api_key`
5. 同样在`config.py`中修改`proxies`为你的代理地址
6. 然后重启 HoshinoBot，并在想要使用的QQ群里输入指令 `启用 dota-poller2` 或者 `enable dota-poller2`
7. 添加玩家： `添加刀塔玩家 [玩家昵称] [steam的id]
    - 如： `添加刀塔玩家 萧瑟 898754153`

然后就可以打一把快乐的刀塔试试效果啦！

## 使用指南
- 添加玩家： 
    - `添加刀塔玩家 [玩家昵称] [steam的id]`
    - 如： `添加刀塔玩家 萧瑟 898754153`
- 关闭XX的群播报: 
    - `关闭[玩家昵称]的群播报`
    - 如： `关闭萧瑟的群播报`
    - `关闭全体的群播报` 关闭本群所有玩家的播报~~我傻了，这个功能没啥用，直接禁用就行了~~
    - 该功能只对当前群有效，不会影响其他群
- 开启XX的群播报:
    - 同上 `开启[玩家昵称]的群播报`


## 运行效果
具体可以看 https://github.com/greenhaha/dota2_csgo_watcher_bot

## 后续计划
- ~~先咕一会，等7.33更新了再说~~(这一咕就是7.36了)
- 可选择是否播报加速/OMG/活动等模式(低优先级)
- ~~可选择开启/关闭某些玩家的战绩播放（高优先级~~(已完成)
- 加个玩家列表的指令
- 更多，更贴切战绩的怪话
- ~~通过图片展示战报的选项~~(摸了)
- ~~获取曾经的战绩~~(不做)