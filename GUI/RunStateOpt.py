import logging
import time

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QTextBrowser
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from GUI import SERVER_PORT
from PdBaseKits.RedisLoader import RedisCntType
from PdBaseKits.logger.logType import LogType
from PdBaseKits.logger.logQueue import logQueue, Source
from PdBaseKits.redis.RedisUtil import redisUtil

from server.APP import server

class workData:
    def __init__(self, log:str, poemCnt:int):
        self.log:str = log
        self.poemCnt = poemCnt

class WorkerThread(QThread):
    trigger = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            time.sleep(0.1)
            try:
                self.trigger.emit("")

            except Exception as e:
                print(e)
        self.finished.emit()


class ServerThread(QThread):
    trigger = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        api_app = server.init_app()
        server.run("0.0.0.0", int(SERVER_PORT))


class RunStateOpt:

    def __init__(self):
        self.gggzBoxShow = None
        self.dpfxBoxShow = None
        self.qgLayout: QGridLayout = None
        self.pWind = ""

    # 返回一个handle
    def createChart(self, parent):
        print("run state create chart")

        logging.info("创建个股跟踪成功")
        self.pWind = parent
        # 外层容器
        self.gggzBoxShow = QWidget()
        tLayout = QGridLayout()
        tLayout.setAlignment(Qt.AlignTop)

        # 内层容器
        tCtn = QWidget()
        self.qgLayout = QGridLayout()

        tCtn.setMinimumWidth(400)
        tCtn.setMinimumHeight(400)
        tCtn.setLayout(self.qgLayout)

        # 1
        self.__showTextArea()

        # trackScroll = QScrollArea(parent)  # 2
        # trackScroll.setWidget(tCtn)
        # trackScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        introQl = QLabel(
            "请首先完成配置，然后启动服务")
        refreshBtn = QPushButton("启动服务")
        refreshBtn.clicked.connect(lambda: self.__startServerFunc(parent))
        refreshBtn.setMaximumWidth(100)

        self.countQl = QLabel(
            "业务完成数量：")
        self.countQl.setFixedHeight(50)
        self.countQl.setStyleSheet("background: #333333; color:#fff")
        self.poemCntQl = QLabel("有效数量：1")
        self.poemCntQl.setStyleSheet("background: #333333; color:#fff")
        self.errorCntQl = QLabel("异常数量：0")
        self.errorCntQl.setStyleSheet("background: #333333; color:#fff")
        tLayout.addWidget(refreshBtn, 0, 0, 1, 1)
        tLayout.addWidget(introQl, 0, 1, 1, 2)

        tLayout.addWidget(self.countQl, 1, 0, 1, 1)
        tLayout.addWidget(self.poemCntQl, 1, 1, 1, 1)
        tLayout.addWidget(self.errorCntQl, 1, 2, 1, 1)

        tLayout.addWidget(tCtn, 2, 0, 1, 3)

        self.gggzBoxShow.setLayout(tLayout)

        self.__startShowThread()
        return self.gggzBoxShow

    def updatePoemCount(self, val:str):
        self.poemCntQl.setText(val)

    def __showTextArea(self):


        self.textBrowser = QTextBrowser()
        self.qgLayout.addWidget(self.textBrowser)


    def __startShowThread(self):
        self.work = WorkerThread()
        self.work.start()

        self.work.trigger.connect(self.__writeLog2Ui)
        self.work.finished.connect(self.__threadFinished)
        return


    def __threadFinished(self):
        print("thread finish")

    def __writeLog2Ui(self, t):
        #print("__writeLog2Ui")
        poemCnt = redisUtil.getStr(RedisCntType.POEM_PARSE_TOTALS)
        """ 处理日志 """
        log: Source = logQueue.pop()

        if log is None:
            self.countQl.setText("业务完成数量：" + str(poemCnt))
            #print("||" + str(poemCnt))
        else:

            self.textBrowser.append(log.content)
            self.countQl.setText("业务完成数量：" + str(poemCnt))
            #print(log.content + "||" + str(poemCnt))









    def __startServerFunc(self, parent):
        print("__dpfxFunc")



        logQueue.push("yes this is saluton mode!", LogType.info)


        self.serverThr = ServerThread()
        self.serverThr.start()

