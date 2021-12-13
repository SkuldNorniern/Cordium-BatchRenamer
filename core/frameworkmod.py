import sys
from core import functionmod as fnm
from core import loggermod as lgm
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QListView,
    QListWidget,
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

        mlo1=QVBoxLayout()
        mlo2=QHBoxLayout()
        lo1=QHBoxLayout()
        lo2=QVBoxLayout()
        # Add widgets to the layout
        self.libox = QTableWidget()
        self.libox.setColumnCount(3)
        self.libox.setHorizontalHeaderLabels(["Name", "Changed Name","Path"])
        
        
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
        lgm.logmsg('Button Called', "debug")
        if key == 'File Select':
            fileNames=fnm.FilesOpen(self)
            files=[]
            for i in fileNames:
                h,w = fnm.Filesep(i)
                file=[w,w,h+w]
                files.append(file)
                
            for i in range(len(files)):
                cur = self.libox.rowCount()
                self.libox.insertRow(cur)
                for j in range(3):
                    print(files[i][j])
                    self.libox.setItem(cur, j, QTableWidgetItem(files[i][j]))
            #self.libox.addItems(fileNames)
            #self.libox.sortItems()
        if key == 'Clear':
            lgm.logmsg('Cleared list', "debug")
            self.libox.clear()
        #    result = str(eval(self.display.text()))
        #    self.display.setText(result)
        #elif key == 'C':
        #    self.display.setText('0')
        #else:
                
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            super(mainWindow, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(mainWindow, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(Qt.SIGNAL("dropped"), links)
            event.acceptProposedAction()
        else:
            super(mainWindow, self).dropEvent(event)

class schfndWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cdm Batch Renamer")
        # Create a QGridLayout instance
        layout = QGridLayout()
        # Add widgets to the layout
        layout.addWidget(QPushButton("Button at (0, 0)"), 0, 0)
        layout.addWidget(QPushButton("Button at (0, 1)"), 0, 1)
        layout.addWidget(QPushButton("Button Spans two Cols"), 1, 0, 1, 2)
        # Set the layout on the application's window
        self.setLayout(layout)


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
