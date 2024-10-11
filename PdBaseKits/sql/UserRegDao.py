import logging
from typing import Union

from PdBaseKits.exceptions.exceptions import SqlConnectError
from PdBaseKits.sql.DbBase import DbBase
from entity.UserInfo import UserInfo


class UserRegDao(DbBase):
    def __init__(self):
        logging.info("UserRegDao")
        super().__init__()


    # 析构方法
    def __del__(self):
        super().__del__()

    def chkUserInfo(self, userName:str, pwd:str)->Union[UserInfo,bool]:
        sql = "select * from userinfo where username='"+userName+"' and password='"+pwd+"'"
        print(sql)
        data, c = self.exeStockSql(sql)
        if not data:
            return False

        for r in data:
            id=r[0]
            userName = r[1]

        userInfo = UserInfo(id, userName)
        return userInfo


