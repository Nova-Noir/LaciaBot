import re
from typing import Tuple, List
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
    MessageSegment,
    Bot,
    PrivateMessageEvent,
    GroupMessageEvent
)
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot import on_message, on_command
from configs.config import NICKNAME

from .ASCII2D import ASCII2DSearch
from .SauceNAO import SauceNAOSearch
from .Soutubot import SoutubotSearch
from .TraceMoe import TraceMoeSearch
from .config import config
from .cache import Cache, exist_in_cache, upsert_cache
from .iqdb import iqdbSearch
from .utils import REPLY_SEARCH_RULE, extract_first_img_url

__zx_plugin_name__ = "搜图"
__plugin_usage__ = """
usage:
    指令：
        搜图 <图片> [选项]
        %回复图片% @bot [选项]
    默认使用 SauceNao -> a2d -> Tracemoe -> Soutubot 次序查找，在上一个m，可通过指定模式指定搜图方法。
    选项:
        -p, --purge     不使用缓存（默认优先从缓存中查找）
        -h, --hide      隐藏搜寻结果缩略图
            --pixiv     使用 pixiv    搜图 (SauceNao 衍生方法)
            --danbooru  使用 danbooru 搜图 (SauceNao 衍生方法)
            --doujin    使用 Soutubot 本子搜图
            --anime     使用 Tracemoe 番剧搜图
            --a2d       使用 ascii2d  搜图
            --iqdb      使用 iqdb     搜图
"""
__plugin_des__ = "使用多个搜图引擎聚合的搜图插件"
__plugin_cmd__ = [
    "搜图",
]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "Nova-No1r"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["搜图"],
}
__plugin_cd_limit__ = {
    "cd": 10,  # 限制 cd 时长
    "check_type": "all",  # 'private'/'group'/'all'，限制私聊/群聊/全部
    "limit_type": "user",  # 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
    "rst": f"{NICKNAME} 也需要休息呢，等等再来吧",  # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
    "status": False  # 此限制的开关状态
}
__plugin_block_limit__ = {"rst": f"{NICKNAME} 正在搜索图片，再等等..."}

reply_img_searcher = on_message(rule=REPLY_SEARCH_RULE, priority=3)
img_searcher = on_command("搜图", aliases={("识图", "查图", "图片搜索")}, priority=2)


def arg_parser(args: str) -> Tuple[str, bool, bool]:
    mode_args = ["pixiv", "danbooru", "doujin", "anime", "a2d", "iqdb"]
    mode = next((i for i in mode_args if f'--{i}' in args), 'all')
    purge = '--purge' in args or '-p' in args
    hide_img = '--hide' in args or '-h' in args
    return mode, purge, hide_img


@img_searcher.handle()
async def _(state: T_State, event: MessageEvent, args: Message = CommandArg()):
    state['args'] = arg_parser(args.extract_plain_text())
    if img := extract_first_img_url(event):
        state['img'] = img


@reply_img_searcher.handle()
@img_searcher.got("img", prompt="你想要查找哪张图片呢?")
async def _(state: T_State, event: MessageEvent, bot: Bot):
    if 'args' not in state:
        state['args'] = arg_parser(event.message.extract_plain_text())
    img = extract_first_img_url(event)
    if not img:
        await bot.send(event, "这不是图片!")
        return
    await img_searcher.send("好的！马上去搜 qwq")
    results = await img_search(img, *state['args'])
    if not results:
        await img_searcher.finish("阿巴阿巴啥也搜不到啊待会再试试吧阿巴阿巴")
        return

    results[0] = f"{MessageSegment.reply(id_=event.message_id)}{results[0]}"
    await bot.send_forward_msg(
        user_id=event.user_id if isinstance(event, PrivateMessageEvent) else 0,
        group_id=event.group_id if isinstance(event, GroupMessageEvent) else 0,
        messages=[
            {
                "type": "node",
                "data": {
                    "name": list(config.nickname)[0] if config.nickname else "\u200b",
                    "uin": bot.self_id,
                    "content": msg,
                },
            }
            for msg in results
        ],
    )


async def img_search(
        url: str,
        mode: str = 'all',
        purge: bool = False,
        hide_img: bool = False
) -> List[str]:
    md5 = re.search(r'[A-F\d]{32}', url)
    if not md5:
        raise ValueError("URL is not a valid link from `qpic.cn` !")
    _cache = Cache("data/laciabot_img_searcher")
    if not purge and (result := exist_in_cache(_cache, f"{md5[0]}_{mode}")):
        return [f"** [Cache] **\n{i}" for i in result]

    if mode == 'a2d':
        results = await ASCII2DSearch(url, hide_img)
    elif mode == 'anime':
        results = await TraceMoeSearch(url, hide_img)
    elif mode == 'doujin':
        results = await SoutubotSearch(url, hide_img)
    elif mode == 'iqdb':
        results = await iqdbSearch(url, hide_img)
    else:
        results = await SauceNAOSearch(url, mode, hide_img)
    upsert_cache(_cache, f"{md5[0]}_{mode}", results)
    return results
