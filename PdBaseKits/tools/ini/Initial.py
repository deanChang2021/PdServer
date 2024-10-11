import logging
import os
import sys

from PdBaseKits.tools.CommonTools import getSys
from PdBaseKits.tools.ini.IniConfig import IniConfig


def getIniFilePath():

    logPath = ""
    if "win" == getSys():
        logPath = "c:/portunid/task/config"
    else:
        logPath = "/Users/admin/config"

    configpath = logPath + "/config.ini"

    return configpath

def getIni(section, key) -> int:
    logPath = ""
    if "win" == getSys():
        logPath = "c:/portunid/task/config"
    else:
        logPath = "/Users/admin/config"

    configpath = logPath + "/config.ini"

    # 检查文件是否存在
    if not os.path.exists(configpath):
        # 文件不存在，创建文件
        raise FileNotFoundError
    else:
        logging.info("find ini file")

    conf = IniConfig(configpath)
    val = conf.get_value(section, key)

    return val


def initialSysConfig():
    print("----- loading ini -----------")
    logPath = ""
    if "win" == getSys():
        logPath = "c:/portunid/task/config"
    else:
        logPath = "/Users/admin/config"

    configpath = logPath + "/config.ini"

    # 检查文件是否存在
    if not os.path.exists(configpath):
        # 文件不存在，创建文件
        with open(configpath, 'w') as file:
            file.write('')
        print(f'文件 {configpath} 已创建。')
    else:
        print(f'文件 {configpath} 已存在。')
        return

    conf = IniConfig(configpath)

    sys = {
        'kling_token':'_did=web_295137192E9A9212; did=web_0328a539ae2236049a118f81397c58660522; monetization-ads-shown-count-xx=T; user-message-duration-extend-two-years=true; userId=1139668240; kuaishou.ai.portal_st=ChVrdWFpc2hvdS5haS5wb3J0YWwuc3QSsAEZB7Amx4hRovpuMK71gbhE1r2mwDPtOBkYHGvfYuj480eh-uNpxA7jz8TbHqQUQIdeqOsgoGaBuV1mMcHKj-XlsismCqsD9qyOgscWQjw_M5aoUiVfUif0hY_tW5KZ5b_1t6UO0KCuOx1OyfFluSHBK71sBW5a9V_604RPFc-sv98YeZazAYzoBokfDUY0rrutfNOcf-_EVeIv_eiGJKZu-s76RsawtXRXZYdYzvY_tRoSbNPczmNJ_1sJ8Hk4ukmqCW4IIiC1_zgVPWZ3Ue8iAvCaTtIzbD4afUUON6g2OLAbV630XygFMAE; kuaishou.ai.portal_ph=912f12da2e1901d930500acbdd44bb332319',
        'maxTaskQueueLen':3,
        'maxWaitQueueLen': 99,
        'taskTimeOut':180,
    }
    server = {
        'port' : 8062,
    }

    log = {
        'maxLogLen': 999,
    }

    db = {
        'host':'localhost',
        'name':'woowo',
        'user':'root',
        'pwd':'zyy191712',
    }

    thirdApi = {'token' :'testtoken'}

    ai = {'chatModel': 'qwen2.5', 'mathModel': 'qwen2-math'}

    conf.add_section("sys", sys)
    conf.add_section("server", server)
    conf.add_section("log", log)
    conf.add_section("db", db)
    conf.add_section("thirdApi", thirdApi)
    conf.add_section("ai", ai)