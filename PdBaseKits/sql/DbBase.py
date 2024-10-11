import logging

import pymysql

from PdBaseKits.exceptions.exceptions import SqlConnectError
from PdBaseKits.sql import DB_HOST, DB_NAME, DB_USER, DB_PWD

class DbBase:

    conn=""
    cursor=""

    def __init__(self):
        print(">>> DbBase init.")
        if not self.__createStockHandle():
            raise SqlConnectError("创建连接失败")


    # 析构方法
    def __del__(self):
        print(">>> DbBase del.")
        if self.conn:
            self.conn.close()


    # 提交数据
    def submitStockSql(self, sql):

        self.cursor.execute(sql)
        self.commitStock()


    # 查询数据
    def exeStockSql(self, sql):

        cursor = self.getStockHandle()

        cursor.execute(sql)

        data = cursor.fetchall()

        return data, cursor


    def getStockConn(self):
        return self.conn

    def getStockHandle(self):
        return self.cursor
        # 此句柄多线程不安全


    def commitStock(self):
        self.conn.commit()

    #
    def __createStockHandle(self):
        print("DB_HOST["+str(DB_HOST)+"],DB_USER["+str(DB_USER)+"], DB_PWD["+str(DB_PWD)+"],DB_NAME["+str(DB_NAME)+"]")
        try:
            self.conn = pymysql.connect(host=DB_HOST, port=3306, user=DB_USER,
                                            passwd=DB_PWD, db=DB_NAME, charset='utf8')

        except pymysql.connect.Error  as e:
            print(">>> __createStock2022Handle，连接数据库失败！")
            return False

        # 创建游标
        self.cursor = self.conn.cursor()
        return True


