import logging
import shutil
from typing import Union
from fastapi import UploadFile

from PdBaseKits.AES import aesECBDecrypt
from PdBaseKits.OCR.ocr import OCR
from PdBaseKits.RedisLoader import RedisCntType
from PdBaseKits.llm.chat import LLM, PoemInfo
from PdBaseKits.logger.logQueue import logQueue
from PdBaseKits.redis.RedisUtil import redisUtil
from PdBaseKits.tools.CommonTools import getSaveUploadFilePath, getFileName
from business.demoService import demo

from entity.UserInfo import UserInfo
from server import WAIT_SIZE
from server.handler.handler import unique_id
from server.schema.schema import TriggerImagineIn
from server.schema.TriggerType import TriggerType
from server.queue.TaskQueue import taskqueue


class klingService:

    def login(self, userId, pwd) -> Union[UserInfo, bool]:
        try:
            pwdDecrypt = aesECBDecrypt(pwd)
            #user = UserRegDao()
        except Exception as e:
            return False
        print("pwdDecrypt:" + pwdDecrypt)

        return UserInfo(1, "zyy")  #user.chkUserInfo(userId, pwdDecrypt)

    def __chkWaitQueue(self, userId: int):
        if taskqueue.findWaitTask(userId):
            return 600
        return 200

    def __chkConsurQueue(self, userId: int):
        if taskqueue.findConsurTask(userId):
            return 601
        return 200

    def imageingTask(self, body: TriggerImagineIn):

        redisUtil.incrKey(RedisCntType.POEM_PARSE_TOTALS)
        print("POEM_PARSE_TOTALS:"+str(redisUtil.getStr(RedisCntType.POEM_PARSE_TOTALS)))
        return 200, "1231232", "2"

        # if (taskqueue.currentWaitQueueLen() >= int(WAIT_SIZE)):
        #     return 603, " task queue is full", WAIT_SIZE
        #
        # ret = self.__chkWaitQueue(body.userId)
        # if ret != 200:
        #     return ret, "user task is waitting", 0
        # print("wait queue pass")
        #
        # ret = self.__chkConsurQueue(body.userId)
        # if ret != 200:
        #     return ret, "user task is executing", 0
        # logging.info("consur queue pass")
        # triggerId = str(unique_id())
        #
        # taskqueue.put(str(body.userId), demo, triggerId, TriggerType.generate.value)
        #
        # logQueue.info("recive imagine task")
        #
        # return 200, "1231232", "2"


    def uploadTask(self, file: UploadFile, fileName: str) -> Union[str,None]:


        tmpArr = fileName.split(".")
        sysFileName = getFileName(tmpArr[-1])

        try:
            filePath = getSaveUploadFilePath() + sysFileName
            logging.info("filePath ["+filePath+"]")
            with open(filePath, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        except Exception as e:
            logging.error(str(e))
            return None

        return sysFileName


    def parsePoemTask(self, fileName) -> tuple[str, PoemInfo]:
        filePath = getSaveUploadFilePath() + fileName
        logging.info("filePath:" + filePath)


        poem:str = OCR().ocr(filePath, "chi_sim")
        ret = LLM().chatPoem(poem)

        redisUtil.incrKey(RedisCntType.POEM_PARSE_TOTALS)

        logging.info("--- after chat ----")
        logging.info(ret)
        return poem, ret
