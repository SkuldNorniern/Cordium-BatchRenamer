import os
from pathlib import Path
from core import loggermod as lgm
from PyQt5.QtWidgets import QFileDialog


def FilesOpen(instance):
    lgm.logmsg("Called File Dialog","debug")
    dialog = QFileDialog(instance)
    dialog.setFileMode(QFileDialog.ExistingFiles)
    dialog.setNameFilter(instance.tr("All Files(*.*)"))
    dialog.setViewMode(QFileDialog.Detail)
    files = []
    if dialog.exec_():
        fileNames = dialog.selectedFiles()
        for i in fileNames:
            h, w = Filesep(i)
            file = [w, w, list2String(i)]
            files.append(file)
    return files


def list2String(s):
    str1 = ""

    for ele in s:
        str1 += ele

    return str1

def Filesep(filepath):
    head, tail = os.path.split(filepath)
    return head, tail

def rename(before, after, path):
    print(path)
    os.rename(path, path.replace(before, after))

def noext(file):
    return Path(file).stem