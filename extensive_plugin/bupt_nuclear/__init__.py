from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment

from configs.config import NICKNAME

from .data_source import get_nuclear_people_number

__zx_plugin_name__ = "核酸点位查询"
__plugin_usage__ = """
usage:
    指令：
        @bot 核酸
"""
__plugin_des__ = "BUPT 核酸点位查询"
__plugin_cmd__ = [
    "搜图",
]
__plugin_type__ = ("BUPT-Tools",)
__plugin_version__ = 0.1
__plugin_author__ = "Nova-No1r"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["核酸"],
}
__plugin_cd_limit__ = {
    "cd": 10,  # 限制 cd 时长
    "check_type": "all",  # 'private'/'group'/'all'，限制私聊/群聊/全部
    "limit_type": "user",  # 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
    "rst": f"{NICKNAME} 也需要休息呢，等等再来吧",  # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
    "status": False  # 此限制的开关状态
}

__plugin_block_limit__ = {"rst": f"{NICKNAME} 正在实地考察核酸人数，再等等..."}

bupt_nuclear = on_command("nuclear", aliases={"核酸", "核"}, rule=to_me, priority=2, block=True)


@bupt_nuclear.handle()
async def _():
    result = await get_nuclear_people_number()
    msg = MessageSegment.text(f"更新时间：{result.time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    for resp in result.nuclear_list:
        if resp.count in range(0, 50):
            rt = "稳"
        elif resp.count in range(50, 100):
            rt = "急"
        else:
            rt = "寄"
        msg += f"{resp.locate}: {rt} | 预估人数: {resp.count}\n"
    await bupt_nuclear.finish(msg)