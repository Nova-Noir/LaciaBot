from nonebot.adapters.onebot.v11 import Event
from utils.manager import group_manager, plugins2settings_manager
from utils.utils import get_message_text
from services.log import logger
import time

cmd = []

v = time.time()


def switch_rule(event: Event) -> bool:
    """
    说明:
        检测文本是否是关闭功能命令
    参数:
        :param event: pass
    """
    global cmd, v
    try:
        if not cmd or time.time() - v > 60 * 60:
            cmd = ["关闭全部被动", "开启全部被动", "开启全部功能", "关闭全部功能"]
            _data = group_manager.get_task_data()
            for key in _data:
                cmd.extend(
                    (
                        f"开启{_data[key]}",
                        f"关闭{_data[key]}",
                        f"开启 {_data[key]}",
                        f"关闭 {_data[key]}",
                    )
                )

            _data = plugins2settings_manager.get_data()
            for key in _data.keys():
                try:
                    if isinstance(_data[key].cmd, list):
                        for x in _data[key].cmd:
                            cmd.extend((f"开启{x}", f"关闭{x}", f"开启 {x}", f"关闭 {x}"))
                    else:
                        cmd.extend((f"开启{key}", f"关闭{key}", f"开启 {key}", f"关闭 {key}"))
                except KeyError:
                    pass
            v = time.time()
        msg = get_message_text(event.json()).split()
        msg = msg[0] if msg else ""
        return msg in cmd
    except Exception as e:
        logger.error(f"检测是否为功能开关命令发生错误 {type(e)}: {e}")
    return False
