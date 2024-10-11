from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QAction
from PyQt5.QtWidgets import QApplication, QMainWindow

from GUI.SysSettingOpt import SysSettingOpt
from PdBaseKits.logger.logCfg import setupLogger
from GUI.RunStateOpt import RunStateOpt

from PdBaseKits.tools.ini.Initial import initialSysConfig

# ========  Config   ========


version = "0.4"


# ========  End Config   ========


class KlingServerGUI(QMainWindow):
    newStockHqData = ""
    newStateData = ""
    existTabName = []
    MENU_RUN_STATE = "RUNSTATE"
    MENU_SYS_SETTING = "HYFX"

    exeTimeArr = ["09"]

    # 初始化各个句柄
    def __init__(self, parent=None):
        super(KlingServerGUI, self).__init__(parent)

        self.showTabWidget = None
        self.runStateBoxShow = None
        self.SysSettingBoxShow = None

        self.existTabName = []
        # 设置窗口标题
        self.setWindowTitle('KlingApiServer(' + version + ')，请匆关闭！！')
        # 设置窗口大小
        self.resize(400, 600)
        self.setWindowIcon(QIcon(":/logo.png"))
        self.createMenu()
        self.iniWelcomeTab()

    def createMenu(self):
        print(">>> createMenu")
        menuBar = self.menuBar()
        # menuBar.setNativeMenuBar(False)
        # dataMenu = menuBar.addMenu("数据处理")
        indusryMenu = menuBar.addMenu("系统")
        stockMenu = menuBar.addMenu("设置")

        # 给menu创建一个Action
        getDataAct = QAction(QIcon(':/spider.png'), '运行日志', self)
        getDataAct.setShortcut('Ctr+Q')
        getDataAct.setStatusTip('Exit Application')
        getDataAct.triggered.connect(lambda: self.createRunStatePanel())
        indusryMenu.addAction(getDataAct)

        alyStockAct = QAction(QIcon(':/alystock.png'), '系统设置', self)
        alyStockAct.setShortcut('Ctr+Q')
        alyStockAct.setStatusTip('Exit Application')
        alyStockAct.triggered.connect(lambda: self.createSettingPanel())
        stockMenu.addAction(alyStockAct)

        self.setMenuWidget(menuBar)

    def createRunStatePanel(self):
        print(">>> createRunStatePanel exist tab： ", self.existTabName)
        # 如果已经存在不作任何动作
        if self.MENU_RUN_STATE in self.existTabName:
            self.showTabWidget.setCurrentWidget(self.runStateBoxShow)
            return

        print("create obj")
        # 不存在则新建
        self.existTabName.append(self.MENU_RUN_STATE)
        runState = RunStateOpt()
        self.runStateBoxShow = runState.createChart(self)
        if not self.runStateBoxShow is None:
            self.showTabWidget.addTab(self.runStateBoxShow, "系统运行状态")
            self.showTabWidget.setCurrentWidget(self.runStateBoxShow)
        else:
            print("createRunStatePanel pdfx is 0")

    def createSettingPanel(self):
        print(">>> createSettingPanel exist panel： ", self.existTabName)
        # 如果已经存在不作任何动作
        if self.MENU_SYS_SETTING in self.existTabName:
            self.showTabWidget.setCurrentWidget(self.SysSettingBoxShow)
            return

        # 不存在则新建
        self.existTabName.append(self.MENU_SYS_SETTING)
        sysSetting = SysSettingOpt()
        self.SysSettingBoxShow = sysSetting.createChart(self)
        if not self.SysSettingBoxShow is None:
            self.showTabWidget.addTab(self.SysSettingBoxShow, "系统设置")
            self.showTabWidget.setCurrentWidget(self.SysSettingBoxShow)
        else:
            print("createSettingPanel pdfx is 0")

    def iniWelcomeTab(self):
        self.showTabWidget = QTabWidget()
        self.setCentralWidget(self.showTabWidget)

        status = self.statusBar()
        status.showMessage("portunid team是一个专注于数据分析的团队，欢迎关注公众号：AIGC中文站")

        self.createRunStatePanel()



