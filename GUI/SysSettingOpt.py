from PyQt5.QtWidgets import QWidget, QScrollArea, QTableWidgetItem, QAbstractItemView, QPushButton, \
            QTableWidget, \
            QLabel, QGridLayout, QMessageBox, QInputDialog, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtWidgets import QFormLayout, QDialog, QComboBox, QSpinBox, QDialogButtonBox
import logging


class SysSettingOpt:

    gggzBoxShow = ""
    pWind = ""

    def __init__(self):



        pass

    # 返回一个handle
    def createChart(self, parent):
        logging.info("创建个股跟踪成功")
        self.pWind = parent
        # 外层容器
        self.gggzBoxShow = QWidget()
        tLayout = QGridLayout()
        tLayout.setAlignment(Qt.AlignTop)

        # 内层容器
        tCtn = QWidget()
        self.qgLayout = QGridLayout()

        tCtn.setMinimumWidth(1100)
        tCtn.setMinimumHeight(1000)
        tCtn.setLayout(self.qgLayout)

        self.__showSetPanel()

        introQlt = QLabel("用户token")
        lineEdit = QLineEdit()
        lineEdit.setFixedWidth(300)




        trackScroll = QScrollArea(parent)  # 2
        trackScroll.setWidget(tCtn)
        trackScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        introQl = QLabel("请在如下文件中按要求完成配置，更新后需重启")
        winIntroQl = QLineEdit("windows：c:/portunid/task/config/config.ini")#QLabel("windows：c:/portunid/task/config/config.ini")
        macIntroQl = QLineEdit("macOS：/Users/admin/config/config.ini")
        tipIntroQl = QLabel("配置文件token是必须项，其它可以使用默认值")

        tLayout.addWidget(introQl, 0, 0, 1, 1)
        tLayout.addWidget(winIntroQl, 1, 0, 1, 1)
        tLayout.addWidget(macIntroQl, 2, 0, 1, 1)
        tLayout.addWidget(tipIntroQl, 3, 0, 1, 1)



        self.gggzBoxShow.setLayout(tLayout)

        return self.gggzBoxShow

    def __showSetPanel(self):
        None
