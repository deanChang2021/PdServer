from PdBaseKits.redis.RedisUtil import redisUtil
from enum import Enum


"""定义了需要Redis统计的业务"""
class RedisCntType(str, Enum):
    POEM_PARSE_TOTALS = "ocrPoem:totals"


"""初始化需Redis统计的业务，在启动时调用"""
def initRedis():
    redisUtil.iniIncr(RedisCntType.POEM_PARSE_TOTALS, 0)