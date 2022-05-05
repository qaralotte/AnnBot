# 非 pycharm 环境需要手动导入项目文件夹
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import core.bot as bot
import function

if __name__ == '__main__':
    bot.login()
