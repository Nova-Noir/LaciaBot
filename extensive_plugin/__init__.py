import nonebot
import pathlib


plugin_list: list[str] = [
    'nonebot-plugin-chatgpt'
]

prefix = pathlib.Path(__file__).parent.absolute()

for plugin in plugin_list:
    nonebot.load_plugins(str(prefix / plugin))