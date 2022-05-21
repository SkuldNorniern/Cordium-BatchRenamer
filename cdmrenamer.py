import sys
from core import frameworkmod as fwm
from core import loggermod as lgm
from PyQt5.QtWidgets import QApplication

app= QApplication(sys.argv)
lgm.init()
mainwindow = fwm.mainWindow()
mainwindow.setStyleSheet(open("theme/theme.qss", "r").read())
mainwindow.setAutoFillBackground(True)
mainwindow.show()

sys.exit(app.exec_())



