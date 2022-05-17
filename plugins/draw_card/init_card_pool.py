from typing import Any
from .config import DRAW_DATA_PATH
from .util import is_number
from nonebot.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json


def init_game_pool(game: str, data: dict, operator: Any):
    tmp_lst = []
    for key, value_ in data.items():
        if game == "genshin":
            if key.find("旅行者") != -1:
                continue
            limited = False
            if data[key]["常驻/限定"] == "限定UP":
                limited = True
            try:
                tmp_lst.append(
                    operator(name=key, star=int(data[key]["稀有度"][:1]), limited=limited)
                )
            except Exception as e:
                logger.warning(f"原神导入角色 {key} 数据错误：{type(e)}：{e}")
        elif game == "genshin_arms":
            if data[key]["获取途径"].find("祈愿") != -1:
                limited = False
                if data[key]["获取途径"].find("限定祈愿") != -1:
                    limited = True
                try:
                    tmp_lst.append(
                        operator(
                            name=key, star=int(data[key]["稀有度"][:1]), limited=limited
                        )
                    )
                except Exception as e:
                    logger.warning(f"原神导入武器 {key} 数据错误：{type(e)}：{e}")
        elif game == "pretty":
            try:
                tmp_lst.append(
                    operator(name=key, star=data[key]["初始星级"], limited=False)
                )
            except Exception as e:
                logger.warning(f"赛马娘导入角色 {key} 数据错误：{type(e)}：{e}")
        elif game == "pretty_card":
            limited = False
            if "卡池" not in value_["获取方式"]:
                limited = True
            if not data[key]["获取方式"]:
                limited = False
            try:
                tmp_lst.append(
                    operator(
                        name=data[key]["中文名"],
                        star=len(data[key]["稀有度"]),
                        limited=limited,
                    )
                )
            except Exception as e:
                logger.warning(f"赛马娘导入卡片 {key} 数据错误：{type(e)}：{e}")
        elif game == "prts":
            limited = False
            if "限定寻访" in data[key]["获取途径"]:
                limited = True
            recruit_only = False
            if "干员寻访" not in data[key]["获取途径"] and "公开招募" in data[key]["获取途径"]:
                recruit_only = True
            event_only = False
            if "活动获取" in data[key]["获取途径"]:
                event_only = True
            if "干员寻访" not in data[key]["获取途径"]:
                if data[key]["获取途径"][0] == "凭证交易所":
                    limited = True
                if data[key]["获取途径"][0] == "信用累计奖励":
                    limited = True
            if key.find("阿米娅") != -1:
                continue
            try:
                tmp_lst.append(
                    operator(
                        name=key,
                        star=int(data[key]["星级"]),
                        limited=limited,
                        recruit_only=recruit_only,
                        event_only=event_only,
                    )
                )
            except Exception as e:
                logger.warning(f"明日方舟导入角色 {key} 数据错误：{type(e)}：{e}")
    if game in {"guardian", "guardian_arms"}:
        tmp_lst.extend(
            operator(
                name=value____["名称"], star=int(data[key]["星级"]), limited=False
            )
            for key, value____ in data.items()
        )

    for key, value__ in data.items():
        if game == "azur":
            if is_number(data[key]["星级"]):
                limited = False
                if "可以建造" not in data[key]["获取途径"]:
                    limited = True
                try:
                    tmp_lst.append(
                        operator(
                            name=value__["名称"],
                            star=int(data[key]["星级"]),
                            limited=limited,
                            type_=data[key]["类型"],
                        )
                    )

                except Exception as e:
                    logger.warning(f"碧蓝航线导入角色 {key} 数据错误：{type(e)}：{e}")
        elif game == "pcr":
            limited = False
            if key.find("（") != -1:
                limited = True
            try:
                tmp_lst.append(
                    operator(
                        name=data[key]["名称"], star=int(data[key]["星级"]), limited=limited
                    )
                )
            except Exception as e:
                logger.warning(f"公主连接导入角色 {key} 数据错误：{type(e)}：{e}")
    if game in {"fgo", "fgo_card"}:
        for key, value in data.items():
            limited = False
            try:
                if (
                    "圣晶石召唤" not in value["入手方式"]
                    and "圣晶石召唤（Story卡池）" not in data[key]["入手方式"]
                ):
                    limited = True
            except KeyError:
                pass
            try:
                tmp_lst.append(
                    operator(
                        name=data[key]["名称"], star=int(data[key]["星级"]), limited=limited
                    )
                )
            except Exception as e:
                logger.warning(f"FGO导入角色 {key} 数据错误：{type(e)}：{e}")
    if game == "onmyoji":
        for key, value___ in data.items():
            limited = False
            if key in [
                "奴良陆生",
                "卖药郎",
                "鬼灯",
                "阿香",
                "蜜桃&芥子",
                "犬夜叉",
                "杀生丸",
                "桔梗",
                "朽木露琪亚",
                "黑崎一护",
                "灶门祢豆子",
                "灶门炭治郎",
            ]:
                limited = True
            try:
                tmp_lst.append(
                    operator(
                        name=value___["名称"],
                        star=data[key]["星级"],
                        limited=limited,
                    )
                )

            except Exception as e:
                logger.warning(f"阴阳师导入角色 {key} 数据错误：{type(e)}：{e}")
    # print(tmp_lst)
    char_name_lst = [x.name for x in tmp_lst]
    up_char_file = (
        (DRAW_DATA_PATH / "draw_card") / "draw_card_up"
    ) / f"{game.split('_')[0]}_up_char.json"

    if up_char_file.exists():
        data = json.load(open(up_char_file, "r", encoding="utf8"))
        key = "char" if len(game.split("_")) == 1 else list(data.keys())[1]
        for x in data[key]["up_char"]:
            for char in data[key]["up_char"][x]:
                if char not in char_name_lst:
                    if "prts" in game:
                        tmp_lst.append(
                            operator(
                                name=char,
                                star=int(x),
                                recruit_only=False,
                                event_only=False,
                                limited=False,
                            )
                        )
                    else:
                        tmp_lst.append(operator(name=char, star=int(x), limited=False))
    return tmp_lst
