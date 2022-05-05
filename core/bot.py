from graia.ariadne import Ariadne
from graia.ariadne.model import MiraiSession

import core.config as config
from util import setting

app = Ariadne(MiraiSession(
    host=config.HOST,
    verify_key=config.VERIFY_KEY,
    account=config.QQ,
))


# 登录
def login():
    app.launch_blocking()


# 版本号
def version():
    return setting.read('bot')['version']
