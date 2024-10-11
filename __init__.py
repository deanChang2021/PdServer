import logging
from PdBaseKits.logger.logCfg import setupLogger
from PdBaseKits.tools.ini.Initial import initialSysConfig

setupLogger("kling")
logging.info("开始初始化系统配置文件……")

initialSysConfig()
