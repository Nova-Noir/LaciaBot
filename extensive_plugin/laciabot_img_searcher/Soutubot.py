from tenacity import AsyncRetrying, wait_fixed, stop_after_delay, stop_after_attempt
from typing import Optional, List
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from nonebot.log import logger
from playwright._impl._api_structures import FilePayload
from playwright.async_api import Page

from utils.browser import get_browser, get_playwright

from .model import SoutubotResult
from .utils import handle_img


class Soutubot:
    def __init__(self):
        self.page: Optional[Page] = None

    @staticmethod
    async def get_page() -> Page:
        # ToDo: Set `proxy` Option
        browser = await get_browser()
        playwright = await get_playwright()
        """ Remove webdriver flag and replace UA with Firefox one to bypass Cloudflare """
        device = playwright.devices['Desktop Firefox']
        js = "Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"

        logger.debug("Trying to bypass Cloudflare...")
        try:
            async for trys in AsyncRetrying(wait=wait_fixed(20), stop=stop_after_attempt(3), reraise=True):
                with trys:
                    context = await browser.new_context(**device)
                    await context.add_init_script(js)

                    new_page = await context.new_page()
                    await new_page.goto("https://soutubot.moe", wait_until="domcontentloaded")
                    try:
                        async for retry in AsyncRetrying(wait=wait_fixed(0.1), stop=stop_after_delay(10), reraise=True):
                            with retry:
                                """ `cf_clearance` is the sign that we bypassed Cloudflare """
                                next(filter(lambda x: x.get('name') == 'cf_clearance', await context.cookies()))
                    except RuntimeError:
                        await new_page.reload()
                    else:
                        break
        except Exception:
            raise ConnectionError("Failed to get the Page from `soutubot.moe`...")
        logger.debug("Bypass success...")
        return new_page

    async def __aenter__(self) -> Page:
        self.page = await self.get_page()
        return self.page

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.page.close()


async def soutubot_from_url(url: str) -> Optional[List[SoutubotResult]]:
    browser = await get_browser()
    img = await browser.new_page()
    resp = await img.goto(url, wait_until='networkidle')
    content = await resp.body()
    if content.startswith(b"\xff\xd8\xff"):
        file = FilePayload(name="img.jpg", mimeType="image/jpeg", buffer=content)
    elif content.startswith(b"\x89\x50\x4E\x47"):
        file = FilePayload(name="img.png", mimeType="image/png", buffer=content)
    else:
        raise ValueError("Invalid image type (only jpg and png support)!")
    await img.close()

    async with Soutubot() as page:
        async for retry in AsyncRetrying(stop=stop_after_attempt(3), reraise=True):
            with retry:
                await page.screenshot(path="test.png")
                await page.wait_for_selector("text=NH全部语言搜索", timeout=5000)
        async with page.expect_file_chooser() as fc:
            await page.click(".inputBox")
            file_chooser = await fc.value
            await file_chooser.set_files(file)
        await page.click("text=NH全部语言搜索")
        await page.wait_for_url(r"https://soutubot.moe/html/*")
        result_content = await page.content()
    return parse(result_content)


def parse(html: str) -> Optional[List[SoutubotResult]]:
    # Todo: Replace the parser with PyQuery
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("tr")
    results = []
    if len(tables) < 2:
        return None
    for i in tables[2:]:
        img = i.find_next("img")
        thumbnail = img.attrs.get('src')
        accuracy = float(str(img.find_next("td").string))
        names_tag = img.find_next("td").find_next("td")
        language = str(names_tag.next_element)[:2] if isinstance(names_tag.next_element, NavigableString) else 'Unknown'
        urls = list(map(lambda x: x.attrs.get('href'),
                        filter(lambda x: isinstance(x, Tag) and x.name == 'a',
                               names_tag.contents)))
        fullname = names_tag.text.replace("via soutubot.moe", " - via soutubot.moe")
        results.append(SoutubotResult(thumbnail=thumbnail,
                                      language=language,
                                      urls=urls,
                                      fullname=fullname,
                                      accuracy=accuracy))
    return results


async def SoutubotSearch(url: str, hide_img: bool = False) -> List[str]:
    try:
        results = await soutubot_from_url(url)
    except ValueError as e:
        message = f"-- Soutubot( VALUE ERROR ) --\n\n" \
                  f"{e}\n 请换个图片试试哦"
    except ConnectionError as e:
        message = f"-- Soutubot( CONNECTION ERROR ) --\n\n" \
                  f"{e}\n 请稍后再试试哦"
    except Exception as e:
        message = f"-- Soutubot( UNKNOWN ERROR {type(e)} ) --\n\n" \
                  f"{e}"
    else:
        message = f"-- Soutubot({results[0].accuracy}%) --\n"
        message += await handle_img(results[0].thumbnail, hide_img)
        message += f"{results[0].fullname}\n" \
                   f"url(s):\n\n" \
                   + "\n".join(results[0].urls)
    return [message]
