import random
from typing import List
from PIL import Image
from pathlib import Path
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH

from .data_source import BUPT_Nuclear_Model

font = "SmileySans-Oblique.otf" # Download this font in 'https://github.com/atelier-anchor/smiley-sans/releases'
                                # or replace it with an existing one.

async def generate_card(nuclear_list: List[BUPT_Nuclear_Model]) -> str:
    bk = BuildImage(
        676,
        115 + len(nuclear_list)*155,
        color=(210, 210, 210, 200),
        font_size=25
    )

    nuclear_img = Image.open(Path(__file__).parent / 'bupt_nuclear.png').resize((620,80))
    await bk.apaste(nuclear_img, (30,20), True)

    data_back_mask = BuildImage(
        666,
        140,
        color=(233, 233, 233, 220)
    )
    await data_back_mask.acircle_corner(10)
    for i in range(len(nuclear_list)):
        data = nuclear_list[i]
        if data.count in range(0, 40):
                rt = "稳"
                rt_color = (34, 166, 105)
        elif data.count in range(40, 100):
                rt = "危"
                rt_color = (209, 164, 31)
        else:
                rt = "寄"
                rt_color = (231, 97, 35)
        data_back = BuildImage(
            676,
            150,
            color=(*rt_color, 220)
        )
        await data_back.acircle_corner(10)
        await data_back.apaste(data_back_mask, (5, 5), True)
        status_text = BuildImage(
            120,
            120,
            color=(255, 255, 255, 0),
            font_size=80,
            font=font
        )
        await status_text.atext((0, 0), rt, rt_color, center_type="center")
        await data_back.apaste(status_text, (20, 10), True)

        locate_text = BuildImage(
            496,
            80,
            color=(255, 255, 255, 0),
            font_size=25,
            font=font
        )
        await locate_text.atext((0, 0), data.locate, fill=(123, 123, 123), center_type='by_width')
        await data_back.apaste(locate_text, (125, 15), True)

        waiting_people_text = BuildImage(
            496,
            80,
            color=(255, 255, 255, 0),
            font_size=25,
            font=font
        )
        await waiting_people_text.atext((0, 0), "当前预估人数：", fill=rt_color, center_type='by_width')
        await data_back.apaste(waiting_people_text, (180, 90), True)

        number_text = BuildImage(
            120,
            120,
            color=(255, 255, 255, 0),
            font_size=80,
            font=font
        )
        await number_text.atext((0, 0), str(data.count), rt_color, center_type='center')
        await data_back.apaste(number_text, (520, 10), True)

        time_text = BuildImage(
            496,
            80,
            color=(233, 233, 233, 0),
            font_size=18,
            font=font
        )
        await time_text.atext((0, 0), f"更新时间：{data.time.strftime('%Y-%m-%d %H:%M:%S')}", fill=(123, 123, 123), center_type="by_width")
        await data_back.apaste(time_text, (125, 120), True)

        await bk.apaste(data_back, (0, 120 + 155*i), True)
    return bk.pic2bs4()
    