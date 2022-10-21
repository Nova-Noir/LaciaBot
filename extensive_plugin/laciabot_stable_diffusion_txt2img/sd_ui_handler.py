from aiohttp import ClientSession, ClientTimeout
from asyncio.exceptions import TimeoutError as aTimeoutError
from typing import Literal, List, Tuple

from configs.config import Config

Config.add_plugin_config("laciabot_stable_diffusion_txt2img",
                         "API_URL",
                         "http://localhost:7860/sdapi/v1/txt2img",
                         help_="API 的完整路径",
                         default_value="http://localhost:7860/sdapi/v1/txt2img")

available_sampler_index = ["Euler", "DDIM", "Euler a"]


async def call_text2img(
        prompt: str,
        *,
        negative_prompt: str = "",
        sampler_index: Literal["Euler", "DDIM", "Euler a"] = "Euler",
        steps: int = 30,
        cfg_scale: float = 7.0,
        width: int = 512,
        height: int = 512,
        denoising: float = 0,
        seed: int = -1,
        **kwargs
) -> Tuple[List[str], str]:

    # Validation
    if sampler_index not in available_sampler_index:
        raise ValueError("%s is not a supported sampler method!(\"Euler\", \"Euler a\", \"DDIM\")" % sampler_index)
    if 0 > steps or steps > 150:
        raise ValueError("%d is not in the valid sampling steps range(0~150)" % steps)
    if 0 > cfg_scale or cfg_scale > 30.0:
        raise ValueError("%.1f is not in the valid cfg scale range(0.0~30.0)" % cfg_scale)
    if 0 >= width or width > 2048:
        raise ValueError("%d is not in the valid width range (0~2048)" % width)
    if 0 >= height or height > 2048:
        raise ValueError("%d is not in the valid height range (0~2048)" % height)
    if 0 > denoising or denoising > 1.0:
        raise ValueError("%.1f is not in the valid denosing range (0.0~1.0)" % denoising)

    json = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_index": sampler_index,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "denoising_strength": denoising,
        "seed": seed,
        **kwargs
    }
    try:
        async with ClientSession(timeout=ClientTimeout(total=60)) as session:
            async with session.post(Config.get_config("laciabot_stable_diffusion_txt2img", "API_URL"),
                                    json=json) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r['images'], r["info"]
                else:
                    raise ConnectionError("Error while fetching the pic. [Code] %d\n%s" %
                                          (resp.status, (await resp.read()).decode()))
    except aTimeoutError:
        raise TimeoutError("Picture is not generated, try to lower your input or retry it again.")
    except Exception as e:
        raise e
