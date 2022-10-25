import asyncio
from typing import Optional
from nonebot.log import logger
from playwright.async_api import Browser, async_playwright
from playwright.async_api._generated import Playwright
from services.log import logger


_browser: Optional[Browser] = None
_playwright: Optional[Playwright] = None


async def init(**kwargs):
    global _browser
    global _playwright
    _playwright = await async_playwright().start()
    try:
        _browser = await _playwright.chromium.launch(**kwargs)
    except Exception:
        # Basically exception raises because Chromium is not installed, so we try to install it and then rerun again
        await asyncio.get_event_loop().run_in_executor(None, install)
        _browser = await _playwright.chromium.launch(**kwargs)


async def get_browser(**kwargs) -> Browser:
    if _browser is None:
        await init(**kwargs)
    return _browser


async def get_playwright(**kwargs) -> Playwright:
    if _playwright is None:
        await init(**kwargs)
    return _playwright


def install():
    """自动安装、更新 Chromium"""
    logger.info("正在检查 Chromium 更新")
    import sys
    from playwright.__main__ import main

    sys.argv = ["", "install", "chromium"]
    try:
        main()
    except SystemExit:
        pass
