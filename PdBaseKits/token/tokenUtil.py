from fastapi import HTTPException, Header
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

#Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyTmFtZSI6Inp6eiIsImlkIjoxMiwiZXhwIjoxNzI0NzI5ODM5fQ.yyfzrDRp7u5cE8ua1dIW0h0ad4CYwilW_2CraUWlVc4

# 加密算法
SECRET_KEY = "zyysqlrxm"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 525600  #一年

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 生成JWT令牌
def createAccessToken(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证JWT令牌
def decodeAccessToken(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail=e.args)


def checkToken(token: str):
    payload = decodeAccessToken(token)
    ##{'userName': 'zzz', 'id': 12, 'exp': 1724729839}


# 鉴权依赖项
async def authenticate(token: str = Header(..., alias="Authorization")):
    checkToken(token)
    return token
