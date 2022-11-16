from aiohttp import ClientSession
from typing import List, Optional
from urllib.parse import urlencode
from pydantic import BaseModel, Extra
from datetime import datetime

main_locale = ['ZIN', 'TygW', 'XHDT', 'Jiao4N', 'KHLT', 'KehuiOutside']
SH_locale = ['SH-TSG-Street', 'SH-XhS', 'SH-JxlW', 'SH-JZG']
all_locale = main_locale + SH_locale

locale_to_readable = {
    "ZIN": "本部-主楼北侧",
    "TygW": "本部-体育馆-室外",
    "XHDT": "本部-学活大厅",
    "Jiao4N": "本部-教四北侧",
    "KHLT": "本部-科学会堂-礼堂",
    "KehuiOutside": "本部-科学会堂-西北室外",
    "SH-TSG-Street": "沙河-图书馆内街",
    "SH-XhS": "沙河-学活南侧",
    "SH-JxlW": "沙河-教学楼西北角(待较正)",
    "SH-JZG": "沙河-甲子钟(待较正)"
}

url = "https://youth.bupt.edu.cn/nuclear/api/get?"

class BUPT_Nuclear_Model(BaseModel, extra=Extra.ignore):
    locate: str
    count: int

class BUPT_Nuclear_List_Model(BaseModel, extra=Extra.forbid):
    time: datetime
    nuclear_list: List[BUPT_Nuclear_Model]



async def get_nuclear_people_number(loc: str = None) -> BUPT_Nuclear_List_Model:
    if loc is None:
        locales = all_locale
    elif loc == 'SH':
        locales = SH_locale
    elif loc == 'main':
        locales = main_locale
    elif loc in all_locale:
        locales= [loc]
    else:
        raise ValueError("Nuclear Locale %s is not on the supported list" % loc)
    
    loc_resp: List[Optional[BUPT_Nuclear_Model]] = []
    time_: datetime = None
    async with ClientSession() as session:
        for locale in locales:
            async with session.get(url + urlencode({'locate': locale})) as r:
                if r.status == 200:
                    resp = await r.json()
                    time_ = resp['time']
                    resp['locate'] = locale_to_readable[locale]
                    loc_resp.append(BUPT_Nuclear_Model.parse_obj(resp))
    if len(loc_resp) == 0:
        raise ConnectionError(f"Could not fetch the number of people in locates {locales}")
    time_ = datetime.strptime(time_, "%Y-%m-%d %H:%M:%S")
    return BUPT_Nuclear_List_Model(time=time_, nuclear_list=loc_resp)
    