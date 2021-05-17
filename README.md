<div align=center><img width="320" height="320" src="https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/zhenxun.jpg"/></div>
![maven](https://img.shields.io/badge/Redis-5.0+-yellow.svg)(https://redis.io/)
# 绪山真寻Bot
****
此项目基于 Nonebot2 和 go-cqhttp 开发的QQ群娱乐机器人
## 关于
用爱发电的项目，某些功能借鉴了大佬们的代码，因为绪山真寻实在太可爱了因此开发了 
绪山真寻bot，实现了一些对群友的娱乐功能和实用功能（大概）。

## 声明
此项目仅用于学习交流，请勿用于非法用途

## 真寻的帮助
请对真寻说: '真寻帮助' or '管理员帮助' or '超级用户帮助' or '对应指令 帮助'


## 功能列表
<details>
<summary>展开查看已实现的功能</summary>

## 已实现的常用功能
- [x] 昵称系统（群与群与私聊分开.）
- [x] 图灵AI（会把'你'等关键字替换为你的昵称）  
- [x] 签到/我的签到/好感度排行（影响色图概率和开箱次数，支持配置）
- [x] 发送某文件夹下的随机图片（支持自定义，默认：美图，萝莉，壁纸）
- [x] 色图（可配置是否存储到本地，并会判断该色图是否已在本地，存在则跳过）
- [x] coser
- [x] 黑白草图生成器
- [x] 鸡汤/语录
- [x] 骂我（钉宫语音）
- [x] 戳一戳（概率发送美图，钉宫语音或者戳回去）
- [x] 模拟开箱/我的开箱/群开箱统计/我的金色/设置cookie（csgo，内置爬虫脚本，需要提前抓取数据和图片，需要session，可能需要代理，阿里云服务器等ip也许已经被ban了（我无代理访问失败），如果访问太多账号可能被封掉！）
- [x] 鲁迅说过
- [x] 构造假消息（自定义的分享链接）
- [x] 商店/我的金币/购买道具/使用道具
- [x] 原神/明日方舟/赛马娘的抽卡【原神抽卡设置小保底与大保底/重置原神抽卡次数】（根据bwiki自动更新）
- [x] 骰子娘（nb2商店插件）
- [x] 我有一个朋友想问问..（pcrbot插件..重构）
- [x] 原神黄历
- [x] 原神今日素材/天赋材料
- [x] 原神资源查询

- [x] pil对图片的一些操作
- [x] BUFF饰品底价查询（需要session）
- [x] 天气查询  
- [x] 疫情查询
- [x] bt搜索
- [x] reimu搜索（上车）
- [x] 靠图识番
- [x] 以图搜图
- [x] 搜番
- [x] 点歌
- [x] epic免费游戏
- [x] p站排行榜（可含参数）
- [x] p站搜图（可含参数）
- [x] 翻译（日英韩）

- [x] 群内csgo服务器（如果没有csgo服务器请删除）
- [x] 查看当前群欢迎消息
- [x] 查看该群自己的权限
- [x] 我的信息（只是为了看看什么时候入群）
- [x] 更新信息（如果继续更新的话）
- [x] go-cqhttp最新版下载和上传（不需要请删除）
- [x] 滴滴滴-（用户对超级用户发送消息）

## 已实现的管理员功能
- [x] 更新群组成员信息
- [x] 95%的功能开关
- [x] 查看群内被动技能状态
- [x] 自定义群欢迎消息（是真寻的不是管家的！）
- [x] .ban/.unban（支持设置ban时长）
- [x] 刷屏禁言相关：刷屏检测设置/设置禁言时长/设置检测次数
- [x] 上传图片 （上传图片至指定图库）
- [x] 移动图片  （同上）
- [x] 删除图片  （同上）

## 已实现的超级用户功能
- [x] 添加/删除管理
- [x] 开启/关闭指定群的广播通知
- [x] 广播
- [x] 自检（检查系统状态）  
- [x] 所有群组/所有好友
- [x] 退出指定群
- [x] 更新好友信息/更新群信息
- [x] /t（对用户进行回复或发送消息）

## 已实现的被动技能
- [x] 开启/关闭进群欢迎
- [x] 开启/关闭早晚安  
- [x] 开启/关闭每日开箱重置提醒
- [x] 开启/关闭b站转发解析
- [x] 开启/关闭丢人爬（爬表情包）
- [x] 开启/关闭epic通知（每日发送epic免费游戏链接）
- [x] 开启/关闭原神黄历提醒

## 已实现的看不见的技能！
- [x] 复读
- [x] 刷屏禁言检测
- [x] 功能调用统计
- [x] 检测恶意触发命令（将被最高权限ban掉30分钟，只有最高权限(9级)可以进行unban）
- [x] 自动同意好友请求，加群请求将会提醒管理员等等
- [x] 群聊时间检测（当群聊最后一人发言时间大于当前36小时后将关闭该群所有通知（即被动技能））
- [x] 支持对各个管理员功能的权限配置
</details>

## Todo
- [ ] 提供更多对插件的控制
- [ ] 明日方舟卡片式的签到..(大概)

## 感谢
[Onebot]("https://github.com/howmanybots/onebot")
[go-cqhttp]("https://github.com/Mrs4s/go-cqhttp")
[nonebot2]("https://github.com/nonebot/nonebot2")