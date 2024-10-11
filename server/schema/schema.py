from typing import Optional, List
from pydantic import BaseModel

class TriggerOcrIn(BaseModel):

    fileName : str
    taskType : Optional[str]
    model : Optional[int] # 1 normal/ 2 fast

class TriggerOcrResponse(BaseModel):
    message: str = "success"
    code: int = 200

    poem: str = ""
    parse : str = ""
    prompt: List[str] = []


class User(BaseModel):
    user: str
    pwd: str

class UserLoginResponse(BaseModel):
    user: str
    id: int
    token: str
    nickname: str
    headUrl: str

class TriggerImagineIn(BaseModel):

    prompt: str
    picurl: Optional[str]
    userId: str


class TriggerUVIn(BaseModel):
    index: int
    msg_id: str
    msg_hash: str
    userId: str



class TriggerResetIn(BaseModel):
    msg_id: str
    msg_hash: str

    trigger_id: str  # 供业务定位触发ID，/trigger/imagine 接口返回的 trigger_id


class TriggerExpandIn(BaseModel):
    msg_id: str
    msg_hash: str
    direction: str  # right/left/up/down
    trigger_id: str  # 供业务定位触发ID，/trigger/imagine 接口返回的 trigger_id

class TriggerZoomOutIn(BaseModel):
    msg_id: str
    msg_hash: str
    zoomout: int    # 2x: 50; 1.5x: 75
    userId: str


class TriggerDescribeIn(BaseModel):
    userId: str
    upload_filename: str
    trigger_id: str


class TriggerUploadIn(BaseModel):
    userId: str
    uploadFilename: str
    uploadUrl: str


class QueueReleaseIn(BaseModel):
    channelId: str


class TriggerResponse(BaseModel):
    message: str = "success"
    code: int = 200
    triggerId: str = ""
    triggerType: str = ""
    waitLen: int = 0

class ReleaseResponse(BaseModel):
    message: str = "success"
    code: int = 200
    userId : str = ""
    triggerId: str = ""
    channelId: str=""
    type:str=""


class UploadResponse(BaseModel):
    message: str = "success"
    upload_filename: str = ""
    upload_url: str = ""
    trigger_id: str


class SendMessageIn(BaseModel):
    upload_filename: str


class SendMessageResponse(BaseModel):
    message: str = "success"
    picurl: str

class TriggerUploadResponse(BaseModel):
    message: str = "success"
    code: int = 200
    picUrl: str = ""


class CallbackErrorRequest(BaseModel):
    businessId: str=""
    type: str=""
    state: str = ""

class CallbackDescriptionRequest(BaseModel):
    channelId: str=""
    businessId: str=""
    first: str=""
    second: str = ""
    third: str = ""
    fourth: str = ""

class CallbackImageRequest(BaseModel):
    businessid:str=""
    msgid:str="" #此msgid是discord生成的msgid
    hashmsg:str=""
    filesize:float=0
    width:int=0
    height:int=0
    type:str=""
    smallpicurl:str=""
    smallfilename:str=""
    picurl:str=""
    filename:str=""