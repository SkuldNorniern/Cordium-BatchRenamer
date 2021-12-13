from core import functionmod as fnm
from core import loggermod as lgm
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QToolButton,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy
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
        
        self.libox = QTableWidget()
        self.libox.setColumnCount(3)
        self.libox.setHorizontalHeaderLabels(["Name", "Changed Name","Path"])
        self.setAcceptDrops(True)

        lo1.addWidget(self.libox)


        btnsymbol = ['String Change', 'Front/Back Adding',
                     'Part Change', 'Clear', 'Apply', 'File Select']
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

        elif key == 'Clear':
            lgm.logmsg('Cleared list', "debug")
            for i in range(self.libox.rowCount()):
                self.libox.removeRow(i)
        
        elif key == 'String Change':
            sfw=schcngWindow(self)
            sfw.exec_()
            for i in range(self.libox.rowCount()):
                tocng = self.libox.item(i, 1).text()
                if sfw.fndstring in tocng:
                    self.libox.setItem(i, 1, QTableWidgetItem(tocng.replace(sfw.fndstring, sfw.cngstring)))
        
        elif key == "Front/Back Adding":
            fba= fbaddWindow(self)
            fba.exec_()
            if(fba.where=="N/A"):
                return
            
            
            for i in range(self.libox.rowCount()):
                tocng = self.libox.item(i, 1).text()
                cur = fnm.noext(tocng)
                if(fba.where=="Front"):
                    self.libox.setItem(i, 1, QTableWidgetItem(tocng.replace(cur,(fba.cngstring+cur))))
                elif(fba.where=="Back"):
                    self.libox.setItem(i, 1, QTableWidgetItem(tocng.replace(cur, (cur+fba.cngstring))))
        
        elif key == "Part Change":
            pgw = ptcngWindow(self)
            pgw.exec_()
            for i in range(self.libox.rowCount()):
                tocng = self.libox.item(i, 1).text()
                if len(tocng) < pgw.ednum:
                    continue
                self.libox.setItem(i, 1, QTableWidgetItem(tocng[:pgw.stnum-1]+pgw.cngstring+tocng[pgw.ednum-1:]))
        
        elif key == 'Apply':
            lgm.logmsg("Applying changes","debug")
            print(self.libox.item(0, 1).text())
            for i in range(self.libox.rowCount()):
                bef = self.libox.item(i, 0).text()
                aft = self.libox.item(i, 1).text()
                if bef != aft:
                    path=self.libox.item(i, 2).text()
                    fnm.rename(bef,aft,path)
                    self.libox.setItem(i, 0, QTableWidgetItem(aft))
                    self.libox.setItem(i, 2, QTableWidgetItem(path.replace(bef,aft)))
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        
        filess = fnm.filetable(files)
        
        for i in range(len(filess)):
            cur = self.libox.rowCount()
            self.libox.insertRow(cur)
            for j in range(3):
                self.libox.setItem(cur, j, QTableWidgetItem(filess[i][j]))

            self.libox.resizeColumnsToContents()            

class schcngWindow(QDialog):
    def __init__(self,parent):
        super(schcngWindow,self).__init__(parent)
        self.setWindowTitle("Find and Changer")
       
        mlo1= QVBoxLayout()
        lo1= QHBoxLayout()
        self.fndstr=QLineEdit()
        self.cngstr = QLineEdit()
        
        mlo1.addWidget(QLabel("String to find"))
        mlo1.addWidget(self.fndstr)
        mlo1.addWidget(QLabel("String to change"))
        mlo1.addWidget(self.cngstr)
         
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
            self.fndstring = self.fndstr.text()
            self.cngstring = self.cngstr.text()
            self.close()
        elif key == 'Cancel':
            lgm.logmsg("Closing schcngWindow", "debug")
            self.close()


class fbaddWindow(QDialog):
    def __init__(self, parent):
        super(fbaddWindow, self).__init__(parent)
        self.setWindowTitle("Front/Back Add")
        
        mlo1 = QVBoxLayout()
        lo1 = QHBoxLayout()
        self.wherebox = QComboBox()
        self.wherebox.addItem("Front")
        self.wherebox.addItem("Back")
        self.cngstr = QLineEdit()
        
        mlo1.addWidget(QLabel("Where to Add"))
        mlo1.addWidget(self.wherebox)
        mlo1.addWidget(QLabel("String to change"))
        mlo1.addWidget(self.cngstr)
        
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
            self.where = self.wherebox.currentText()
            self.cngstring = self.cngstr.text()
            self.close()
        elif key == 'Cancel':
            self.where = "N/A"
            lgm.logmsg("Closing fbaddWindow", "debug")
            self.close()


class ptcngWindow(QDialog):
    def __init__(self, parent):
        super(ptcngWindow, self).__init__(parent)
        self.setWindowTitle("Part Change")
        
        mlo1 = QVBoxLayout()
        lo1 = QHBoxLayout()
        lo2 = QHBoxLayout()
        lo3 = QHBoxLayout()
        
        self.stnumbx = QLineEdit()
        self.ednumbx = QLineEdit()
        self.cngstr = QLineEdit()
        
        lo1.addWidget(QLabel("Start index"))
        lo1.addWidget(QLabel("End index"))
        lo2.addWidget(self.stnumbx)
        lo2.addWidget(self.ednumbx)
        mlo1.addWidget(QLabel("String to change"))
        mlo1.addWidget(self.cngstr)
        
        btnsymbol = ['Apply', 'Cancel']
        self.funcbtn = [x for x in btnsymbol]
        for i, symbol in enumerate(btnsymbol):
            self.funcbtn[i] = Button(symbol, self.btnCli)

        for i in range(2):
            self.funcbtn[i].setMaximumWidth(130)
            lo3.addWidget(self.funcbtn[i])

        mlo1.addLayout(lo1)
        mlo1.addLayout(lo2)
        mlo1.addLayout(lo3)
        self.setLayout(mlo1)
        self.show()

    def btnCli(self):
        button = self.sender()
        key = button.text()
        lgm.logmsg('Button called', "debug")

        if key == 'Apply':
            self.stnum = int(self.stnumbx.text())
            self.ednum = int(self.ednumbx.text())
            self.cngstring = self.cngstr.text()
            self.close()
        elif key == 'Cancel':
            lgm.logmsg("Closing ptcngWindow", "debug")
            self.close()

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)
