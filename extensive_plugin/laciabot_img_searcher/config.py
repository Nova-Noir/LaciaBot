import typing
from typing import Optional

from configs.config import Config

plugin_name = "laciabot_img_searcher"

Config.add_plugin_config(
    plugin_name,
    "cache_expire",
    7,
    help_="缓存保存时间",
    default_value=7
)
Config.add_plugin_config(
    plugin_name,
    "proxy",
    None,
    help_="搜图代理",
    default_value=None
)
Config.add_plugin_config(
    plugin_name,
    "hide_img_when_tracemoe_r18",
    True,
    help_="TraceMoe R18 时自动隐藏图片",
    default_value=True
)
Config.add_plugin_config(
    plugin_name,
    "saucenao_api_key",
    None,
    help_="SauceNao API",
    default_value=None
)
Config.add_plugin_config(
    plugin_name,
    "saucenao_nsfw_hide_level",
    0,
    help_="SauceNao NSFW 隐藏等级",
    default_value=0
)


class PluginConfig:
    cache_expire: int
    proxy: Optional[str]
    hide_img_when_tracemoe_r18: bool
    saucenao_api_key: Optional[str]
    saucenao_nsfw_hide_level: int

    def __getattr__(self, item):
        return Config.get_config(plugin_name, item)


config = PluginConfig()