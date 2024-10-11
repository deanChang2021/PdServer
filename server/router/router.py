import logging
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, File, UploadFile
import shutil

from PdBaseKits.llm.chat import PoemInfo
from PdBaseKits.logger.logQueue import logQueue
from PdBaseKits.logger.logType import LogType
from PdBaseKits.token.tokenUtil import createAccessToken, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate, decodeAccessToken
from server.service.klingService import klingService

from ..schema.TriggerType import TriggerType
from server.schema.schema import (
    TriggerImagineIn,
    TriggerUVIn,
    TriggerResponse,
    User, UserLoginResponse, TriggerOcrIn, TriggerOcrResponse,
)

router = APIRouter()


@router.post("/login", response_model=UserLoginResponse)
async def login(body: User):
    midService = klingService()

    logging.info("login [" + body.user + "],[" + body.pwd + "]]")

    userInfo = midService.login(body.user, body.pwd)
    if userInfo:
        accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        accessToken = createAccessToken(data={"userName": body.user, 'id': 12}, expires_delta=accessTokenExpires)
        return {"user": userInfo.user, "id": userInfo.id, 'token': accessToken, 'nickname': 'dean', 'headUrl': 'i.png'}
    else:
        return ""


@router.post("/imagine", response_model=TriggerResponse)
async def imagine(body: TriggerImagineIn, token: str = Depends(authenticate)):
    ##v2.0
    midService = klingService()
    code, msg, len = midService.imageingTask(body)
    if code != 200:
        return {"code": code, "message": msg}
    logQueue.push("完成了imagine任务!", LogType.info)
    return {"triggerId": msg, "triggerType": TriggerType.generate.value, "waitLen": len}



### Author : dean Date: 20240919
### 本接口实现文件上传
@router.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...), source: str = ""):
    logging.info("收到上传文件[" + file.filename + "]")


    fileName = klingService().uploadTask(file, file.filename)
    if fileName == None:
        return {"code":500,"msg":"上传文件失败"}
    return {"code":200, "filename": fileName}




@router.post("/ocrPoem", response_model=TriggerOcrResponse)
async def imagine(body: TriggerOcrIn, token: str = Depends(authenticate)):
    print(decodeAccessToken(token))

    ##v2.0
    midService = klingService()
    poem, poemParse = midService.parsePoemTask(body.fileName)
    logging.info(poem)
    logging.info(poemParse)
    if poemParse == None:
        return {"code": 500, "message": "解析失败"}

    logQueue.push("完成了["+str(poemParse.bookName)+"]解析!", LogType.info)
    return {"poem": poem, "parse": poemParse.parse, "prompt": poemParse.prompt}
