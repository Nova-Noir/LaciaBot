import re

from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from utils.utils import get_message_img_file
from nonebot.typing import T_State
from .model import WordBank


async def check(bot: Bot, event: Event, state: T_State) -> bool:
    if isinstance(event, GroupMessageEvent):
        msg = event.raw_message
        if list_img := get_message_img_file(event.json()):
            for img_file in list_img:
                strinfo = re.compile(f"{img_file},subType=\d*]")
                msg = strinfo.sub(f'{img_file}]', msg)
        print(msg)
        return bool(
            await WordBank.check(event.group_id, msg, event.is_tome())
        )
    return False
