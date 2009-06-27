#!/usr/bin/python
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_mainwindow import Ui_MainWindow
from ui_newdialog import Ui_Dialog

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.newButton, SIGNAL("clicked()"), self.openNewDialog)

    def openNewDialog(self):
        diag = NewDialog()
        help(diag)
        diag.setAttribute(Qt.WA_DeleteOnClose)
        rv = diag.exec_()
        print rv

class NewDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
