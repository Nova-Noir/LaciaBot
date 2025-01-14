import math
from typing import Any, Dict, List

from PicImageSearch import TraceMoe, Network

from .config import config
from .utils import handle_img


async def TraceMoeSearch(url: str, hide_img: bool) -> List[str]:
    tracemoe = TraceMoe(client=Network(proxies=config.proxy))
    res = await tracemoe.search(url=url)
    if res and res.raw:
        time = res.raw[0].From
        minutes = math.floor(time / 60)
        seconds = math.floor(time % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        if res.raw[0].isAdult:
            thumbnail = await handle_img(
                res.raw[0].cover_image,
                hide_img or config.hide_img_when_tracemoe_r18,
            )
        else:
            thumbnail = await handle_img(
                res.raw[0].cover_image,
                hide_img,
            )
        chinese_title = res.raw[0].title_chinese
        native_title = res.raw[0].title_native
        video = res.raw[0].video

        def date_to_str(date: Dict[str, Any]) -> str:
            return f"{date['year']}-{date['month']}-{date['day']}"

        start_date = date_to_str(res.raw[0].start_date)
        end_date = ""
        if (end_date_year := res.raw[0].end_date["year"]) and end_date_year > 0:
            end_date = date_to_str(res.raw[0].end_date)
        episode = res.raw[0].episode or 1
        res_list = [
            f"-- TraceMoe（{res.raw[0].similarity}%）--",
            f"截图出自第 {episode} 集的 {time_str}",
            thumbnail,
            chinese_title,
            native_title,
            f"类型：{res.raw[0].type}-{res.raw[0].format}",
            f"开播：{start_date}",
            f"完结：{end_date}" if end_date else "",
        ]
        return ["\n".join([i for i in res_list if i != ""]), f"[CQ:video,file={video}]"]
    return ["WhatAnime 暂时无法使用"]
