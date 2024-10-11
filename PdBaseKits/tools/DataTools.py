import time
import datetime

class DateTools():


    def __init__(self):
        super().__init__()


    def getNow(self):
        return datetime.datetime.now()


    # 返回整点 24小时制
    def getCurClock(self):

        return datetime.datetime.now().strftime('%H')


    def getCurrTimeHM(self):
        return datetime.datetime.now().strftime('%H:%M')

    def getCurrTimeHMS(self):
        return datetime.datetime.now().strftime('%H:%M:%S')

    # 当前日期 %Y%m%d
    def getCurrDate(self):

        return  datetime.datetime.now().strftime('%Y%m%d')


    # 适合windows和mac、linux，因为windows中不能有":"
    def getTimeForName(self, type):

         return datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')



    # 当前时间 % Y - % m - % d % H: % M: % S
    def getCurrTime(self, type):
        if 1 == type:
            return datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        elif 2 == type:
            return datetime.datetime.now().strftime('%H:%M:%S')
        elif 3 == type:
            return datetime.datetime.now().strftime('%Y-%m-%d')
        elif 4 == type:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    # 格式："2022-01-01 12:00:00"
    # 2: t1>t2  0: t2>t1
    def cmpTime(self, t1, t2):

        # 将字符串转换为时间元组

        t1_tuple = time.strptime(t1, "%Y-%m-%d %H:%M:%S")
        t2_tuple = time.strptime(t2, "%Y-%m-%d %H:%M:%S")

        # 将时间元组转换为时间戳
        timestamp1 = time.mktime(t1_tuple)
        timestamp2 = time.mktime(t2_tuple)

        if timestamp1 > timestamp2:
            return 2
        elif timestamp1 == timestamp2:
            return 1
        elif timestamp1 < timestamp2:
            return 0



    # time2与time1的时间差，单位S
    def timeDiff(self, time1, time2):
        s = (time2-time1).seconds()
        print(">>> timeDiff s:",s)
        return s


dateTools = DateTools()
