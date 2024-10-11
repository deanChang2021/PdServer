# 1、gui
import sys
from PyQt5.QtWidgets import QApplication
from GUI.mainWindow import KlingServerGUI

def setupWindow():
    app = QApplication(sys.argv)
    window = KlingServerGUI()
    window.show()

    sys.exit(app.exec())