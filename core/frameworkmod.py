import sys

from PyQt5.QtGui import QTextBlock
from core import functionmod as fnm
from core import loggermod as lgm
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QToolButton,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy,
    QListWidget
 )


class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cdm Batch Renamer")
        self.setGeometry(300, 300, 900, 250)
        
        mlo1=QVBoxLayout() # for future update
        mlo2=QHBoxLayout()
        lo1=QHBoxLayout()
        lo2=QVBoxLayout()
        # Add widgets to the layout
        self.libox = QTableWidget()
        self.libox.setColumnCount(3)
        self.libox.setHorizontalHeaderLabels(["Name", "Changed Name","Path"])
        #self.libox.setSizeAdjustPolicy(
        #    QtWidgets.QAbstractScrollArea.AdjustToContents)
        
        lo1.addWidget(self.libox)


        btnsymbol = ['String Change', 'Front/Back Adding',
                     'EXT Change', 'Clear', 'Apply', 'File Select']
        self.funcbtn = [x for x in btnsymbol]
        for i, symbol in enumerate(btnsymbol):
            self.funcbtn[i] = Button(symbol, self.btnCli)
        
        for i in range(6):
            self.funcbtn[i].setMaximumWidth(130)
            lo2.addWidget(self.funcbtn[i])
        

        self.funcbtn[5].width()
        mlo2.addLayout(lo1)
        mlo2.addLayout(lo2)
        mlo1.addLayout(mlo2)
        #mlo1.addWidget(self.funcbtn[5])
        self.setLayout(mlo1)

    def btnCli(self):
        button = self.sender()
        key = button.text()
        lgm.logmsg('Button called', "debug")
        if key == 'File Select':
            files=[]
            files=fnm.FilesOpen(self)
            if(len(files)==0):
                return 
            for i in range(len(files)):
                cur = self.libox.rowCount()
                self.libox.insertRow(cur)
                for j in range(3):
                    self.libox.setItem(cur, j, QTableWidgetItem(files[i][j]))

            self.libox.resizeColumnsToContents()
            #self.libox.addItems(fileNames)
            #self.libox.sortItems()
        elif key == 'Clear':
            lgm.logmsg('Cleared list', "debug")
            self.libox.clear()
        elif key == 'String Change':
            sfw=schfndWindow(self)
            sfw.exec_()
            for i in range(self.libox.rowCount()):
                if sfw.fndstring in self.libox.item(i, 1).text():
                    self.libox.setItem(i, 1, QTableWidgetItem(self.libox.item(
                        i, 1).text().replace(sfw.fndstring, sfw.cngstring)))
            
        elif key == 'Apply':
            lgm.logmsg("Applying changes","debug")
            print(self.libox.item(0, 1).text())
            for i in range(self.libox.rowCount()):
                bef = self.libox.item(i, 0).text()
                aft = self.libox.item(i, 1).text()
                if bef != aft:
                    path,thr = fnm.Filesep(self.libox.item(i, 2).text())
                    fnm.rename(bef,aft,path)
                    self.libox.setItem(i, 0, QTableWidgetItem(aft))
                    self.libox.setItem(i, 2, QTableWidgetItem(path+aft))
                    
        #    self.display.setText('0')
        #else:
                

class schfndWindow(QDialog):
    def __init__(self,parent):
        super(schfndWindow,self).__init__(parent)
        self.setWindowTitle("Cdm Batch Renamer")
        # Create a QGridLayout instance
        mlo1= QVBoxLayout()
        lo1= QHBoxLayout()
        self.fndstr=QLineEdit()
        self.cngstr = QLineEdit()
        # Add widgets to the layout
        mlo1.addWidget(QLabel("String to find"))
        mlo1.addWidget(self.fndstr)
        mlo1.addWidget(QLabel("String to change"))
        mlo1.addWidget(self.cngstr)
        # Set the layout on the application's window
        btnsymbol = ['Apply', 'Cancel']
        self.funcbtn = [x for x in btnsymbol]
        for i, symbol in enumerate(btnsymbol):
            self.funcbtn[i] = Button(symbol, self.btnCli)

        for i in range(2):
            self.funcbtn[i].setMaximumWidth(130)
            lo1.addWidget(self.funcbtn[i])
        mlo1.addLayout(lo1)
        self.setLayout(mlo1)
        self.show()

    def btnCli(self):
        button = self.sender()
        key = button.text()
        lgm.logmsg('Button called', "debug")
        
        if key == 'Apply':
            self.cngstring=self.cngstr.text()
            self.fndstring=self.fndstr.text()
            self.close()
        elif key == 'Cancel':
            lgm.logmsg("Closing schfndWindow", "debug")
            self.close()


class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    #def sizeHint(self):
    #    size = super(Button, self).sizeHint()
    #    size.setHeight(size.height() + 10)
    #    size.setWidth(max(130, size.height()))
    #    return size
