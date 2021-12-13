import pytest
from core import functionmod as fnm

def test_sep():
    h,w=fnm.Filesep("C:/Users/skuld/Documents/GitHub/Cordium-BatchRenamer/cdmrenamer.py")
    assert h == "C:/Users/skuld/Documents/GitHub/Cordium-BatchRenamer"
    assert w == "cdmrenamer.py"

def test_noext():
    assert fnm.noext("cdmrenamer.py") == "cdmrenamer"

def test_li2str():
    assert fnm.list2String(["cdmrenamer.py"]) == "cdmrenamer.py"

def test_filetable():
    file=[]
    sample=[["cdmrenamer.py", "cdmrenamer.py",
           "C:/Users/skuld/Documents/GitHub/Cordium-BatchRenamer/cdmrenamer.py"]]
    file = fnm.filetable(
        ["C:/Users/skuld/Documents/GitHub/Cordium-BatchRenamer/cdmrenamer.py"])
    assert file == sample
