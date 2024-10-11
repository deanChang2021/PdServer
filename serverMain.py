import __init__
import logging
from GUI.loader import setupWindow
from PdBaseKits.RedisLoader import initRedis

# ========  Config   ========


version = "0.4"


# ========  End Config   ========




if __name__ == '__main__':
    """初始化redis"""
    initRedis()
    logging.info("完成Redis加载")

    """初始化窗口"""
    setupWindow()
    logging.info("完成界面加载")




