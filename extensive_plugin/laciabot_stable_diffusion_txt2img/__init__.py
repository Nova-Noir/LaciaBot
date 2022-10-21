import asyncio.exceptions
from typing import Union

from nonebot import on_shell_command
from nonebot.params import ShellCommandArgs, T_State
from nonebot.rule import Namespace, ParserExit
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, MessageEvent, Message

from configs.config import NICKNAME, Config
from models.bag_user import BagUser

from .parser import ai_drawing_parser
from .sd_ui_handler import call_text2img

__zx_plugin_name__ = "AI画图"
__plugin_usage__ = """
usage：
    指令：
        AI画图 <Prompt> [选项]
    
    选项:
        -w, --width     图片宽度，默认为 `512`，最大为 `2048`，（提高这项的值会急剧消耗金币且存在爆显存的风险）
        -h, --height    图片高度，默认为 `512`，最大为 `2048`，（提高这项的值会急剧消耗金币且存在爆显存的风险）
        -n, --negative  设置否定词条，否则默认为设定好的初始咒语。
        -s, --steps     采样次数，默认为 `30`，最高为 `150`（更高的采样次数会消耗更多金币）
        -c, --cfg-scale 词条倾向程度，默认为 `7.0`，最高为 `30.0`
        -d, --denoising 降噪程度，默认为 `0.0`，最高为 `1.0`（开启这项将会消耗更多金币）
        -m, --method    模型采样方法，默认为 `Euler`，可选项：`Euler`, `Euler a`, `DDIM`
            --seed      设置图片种子，默认为 `-1`
        -y, --yes       不再次确认金币消耗数，直接画图
""".strip()
__plugin_des__ = "基于 Stable Diffusion 以及 NovelAI 泄露模型的绘画插件"
__plugin_cmd__ = [
    "AI画图",
]
__plugin_type__ = ("AI",)
__plugin_version__ = 0.1
__plugin_author__ = "Nova-No1r"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["AI画图"],
}

__plugin_cd_limit__ = {
    "cd": 30,  # 限制 cd 时长
    "check_type": "all",  # 'private'/'group'/'all'，限制私聊/群聊/全部
    "limit_type": "user",  # 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
    "rst": f"{NICKNAME} 也需要休息呢，等等再来吧",  # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
    "status": True  # 此限制的开关状态
}

__plugin_block_limit__ = {"rst": f"{NICKNAME} 正在处理图片，别急..."}

__plugin_configs__ = {
    "BasicCost": {
        "value": 100,
        "help": "每一张图片的基本花费",
        "name": None,
        "default_value": 100
    },
    "StepCost": {
        "value": 2,
        "help": "每增加一次采样步数的花费",
        "name": None,
        "default_value": 2
    },
    "DenoisingCost": {
        "value": 80,
        "help": "开启降噪的花费",
        "name": None,
        "default_value": 80
    },
    "ScaleCost": {
        "value": 0.9,
        "help": "总像素除以(512*512)后的指数，在其他花销上做乘算",
        "name": None,
        "default_value": 0.9
    },
}

ai_drawing = on_shell_command("AI画图", parser=ai_drawing_parser)

draw_prompt = Message.template("准备画图啦！\n本次作图花费 {cost}\n余额: {balance}\n\n确认要作图吗 (Y/n)")


@ai_drawing.handle()
async def _(event: MessageEvent,
            state: T_State,
            args: Union[Namespace, ParserExit] = ShellCommandArgs()):
    if isinstance(args, ParserExit):
        await ai_drawing.finish(args.message)
        return

    state['args'] = args
    if isinstance(event, GroupMessageEvent):
        cost = Config.get_config("laciabot_stable_diffusion_txt2img", "BasicCost")
        cost += Config.get_config("laciabot_stable_diffusion_txt2img", "StepCost") * args.steps \
            if args.steps > 30 else 0
        cost += Config.get_config("laciabot_stable_diffusion_txt2img", "DenoisingCost") if args.denoising != 0.0 else 0
        cost *= ((args.width * args.height / 262144) **
                 Config.get_config("laciabot_stable_diffusion_txt2img", "ScaleCost")) \
            if args.width * args.height > 262144 else 1
        state['cost'] = int(cost)
        state['balance'] = await BagUser.get_gold(event.user_id, event.group_id)
    else:
        state['is_sure'] = Message('y')
    if args.yes:
        state['is_sure'] = Message('y')
    return


@ai_drawing.got("is_sure", prompt=draw_prompt)
async def _(event: MessageEvent, state: T_State):
    if state['is_sure'].extract_plain_text() in ['yes', 'Y', 'y', 'Yes']:
        if isinstance(event, GroupMessageEvent) and state['balance'] < state['cost']:
            await ai_drawing.finish(f"你没有这么多钱来画画哦！\n余额:{state['balance']}\n花费:{state['cost']}")
        await ai_drawing.send(f"收到，{NICKNAME} 马上去画 qwq")
        try:
            result, info = await call_text2img(**state['args'].__dict__)
        except ValueError as e:
            await ai_drawing.finish(MessageSegment.reply(event.user_id) + f"[参数错误]\n{e}")
        except asyncio.exceptions.TimeoutError:
            await ai_drawing.finish(MessageSegment.reply(
                event.user_id) + f"{NICKNAME} 没有把图画出来呢...可能是线程堵塞了。\n可以尝试重新生成或者减小参数再试试哦")
        except Exception as e:
            await ai_drawing.finish(MessageSegment.reply(event.user_id) + f"{type(e)} {e}")
        else:
            for img in result:
                await ai_drawing.send(
                    MessageSegment.reply(event.user_id) + MessageSegment.image("base64://" + img) + info)
            if isinstance(event, GroupMessageEvent):
                await BagUser.spend_gold(event.user_id, event.group_id, state['cost'])
