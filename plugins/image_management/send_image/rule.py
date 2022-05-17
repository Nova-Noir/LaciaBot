from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State
from utils.utils import get_message_text
from configs.config import Config


def rule(bot: Bot, event: Event, state: T_State) -> bool:
    """
    检测文本是否是关闭功能命令
    :param bot: pass
    :param event: pass
    :param state: pass
    """
    msg = get_message_text(event.json())
    return any(
        msg.startswith(x)
        for x in Config.get_config("image_management", "IMAGE_DIR_LIST")
    )
