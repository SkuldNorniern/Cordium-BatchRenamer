import os
from core import loggermod as lgm
from PyQt5.QtWidgets import QFileDialog


def FilesOpen(instance):
    lgm.logmsg("Called File Dialog","debug")
    dialog = QFileDialog(instance)
    dialog.setFileMode(QFileDialog.ExistingFiles)
    dialog.setNameFilter(instance.tr("All Files(*.*)"))
    dialog.setViewMode(QFileDialog.Detail)
    if dialog.exec_():
        fileNames = dialog.selectedFiles()
    return fileNames

def Filesep(filepath):
    head, tail = os.path.split(filepath)
    return head, tail
