from nonebot.rule import ArgumentParser

ai_drawing_parser = ArgumentParser("AI画图", conflict_handler="resolve")
ai_drawing_parser.add_argument("prompt", type=str, action='store', help="词条（需要用双引号包裹）")
ai_drawing_parser.add_argument("-w", "--width", type=int, action='store',
                               help="图片宽度，默认为 `512`，最大为 `2048`，（提高这项的值会急剧消耗金币且存在爆显存的风险）",
                               default=512)
ai_drawing_parser.add_argument("-h", "--height", type=int, action='store',
                               help="图片高度，默认为 `512`，最大为 `2048`，（提高这项的值会急剧消耗金币且存在爆显存的风险）",
                               default=512)
ai_drawing_parser.add_argument("-n", "--negative",
                               type=str, action='store', help="否定词条,默认为设定好的初始咒语（需要用双引号包裹）",
                               default="longbody, lowres,bad anatomy, bad hands, missing fingers, pubic hair,"
                                       "extra digit, fewer digits, cropped, worst quality, low quality")
ai_drawing_parser.add_argument("-s", "--steps", type=int, action='store',
                               help="采样次数，默认为 `30`，最高为 `150`（更高的采样次数会消耗更多金币）",
                               default=30)
ai_drawing_parser.add_argument("-m", "--method", type=str, action='store',
                               help="模型采样方法，默认为 `Euler`，可选项：`Euler`, `Euler a`, `DDIM`",
                               default="Euler")
ai_drawing_parser.add_argument("-d", "--denoising", type=float, action='store',
                               help="降噪程度，默认为 `0.0`，最高为 `1.0`（开启这项将会消耗更多金币）",
                               default=0.0)
ai_drawing_parser.add_argument("-c", "--cfg-scale", type=float, action='store',
                               help="词条倾向程度，默认为 `7.0`，最高为 `30.0`",
                               default=7.0)
ai_drawing_parser.add_argument("--seed", type=int, action='store',
                               help="设置图片种子，默认为 `-1`",
                               default=-1)
ai_drawing_parser.add_argument("-y", "--yes", action='store_true',
                               help="不再次确认直接画图")
