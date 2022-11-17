from datetime import datetime
from typing import List, Optional
from urllib.parse import urlencode

from aiohttp import ClientSession
from pydantic import BaseModel, Extra

url = "https://youth.bupt.edu.cn/nuclear/api/get?"
getloc_url = "https://youth.bupt.edu.cn/nuclear/api/getloc"


class BUPT_Nuclear_Model(BaseModel, extra=Extra.ignore):
    time: datetime
    locate: str
    count: int


async def get_nuclear_people_number(loc: str = None) -> List[BUPT_Nuclear_Model]:
    loc_resp: List[Optional[BUPT_Nuclear_Model]] = []
    time_: datetime = None
    async with ClientSession() as session:
        async with session.get(getloc_url) as r:
            if r.status == 200:
                locales: dict = (await r.json())['loclist']
                if loc is None:
                    pass
                elif loc == 'SH':
                    locales = {x: locales[x]
                               for x in locales.keys() if x.startswith("沙河")}
                elif loc == 'main':
                    locales = {x: locales[x]
                               for x in locales.keys() if x.startswith("沙河")}
                elif loc in locales.keys():
                    locales = {loc: locales[loc]}
                else:
                    raise ValueError(
                        "Nuclear Locale %s is not on the supported list" % loc)
            else:
                raise ConnectionError(
                    "Could not fetch nuclear location, try again later!")
        for locale_name, locale in locales.items():
            async with session.get(url + urlencode({'locate': locale})) as r:
                if r.status == 200:
                    resp = await r.json()
                    resp['time'] = datetime.strptime(resp['time'], "%Y-%m-%d %H:%M:%S")
                    resp['locate'] = locale_name
                    loc_resp.append(BUPT_Nuclear_Model.parse_obj(resp))
    if len(loc_resp) == 0:
        raise ConnectionError(
            f"Could not fetch the number of people in locates {locales}")
    return loc_resp
