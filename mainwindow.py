#!/usr/bin/python
# encoding: utf8
import sys
import yaml
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_mainwindow import Ui_MainWindow
from ui_newdialog import Ui_Dialog

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.items = []
        self.dataModel = ItemModel(self.items)
        self.itemTable.setModel(self.dataModel)
        self.itemTable.verticalHeader().setVisible(False)
        hh = self.itemTable.horizontalHeader()
        hh.setVisible(True)
        hh.setStretchLastSection(True)
        self.itemTable.resizeColumnsToContents()
        self.itemTable.setColumnWidth(0, 180)
        self.connect(self.newButton, SIGNAL("clicked()"), self.openNewDialog)
        self.connect(self.startButton, SIGNAL("clicked()"), self.startTimer)
        self.connect(self.stopButton, SIGNAL("clicked()"), self.stopTimer)
        self.updateTimer = QTimer(self)
        self.connect(self.updateTimer, SIGNAL("timeout()"), self.timerTick)
        self.updateTimer.start(1000)
        self.connect(self.actionSave, SIGNAL("triggered()"), self.save)
        self.connect(self.actionLoad, SIGNAL("triggered()"), self.load)

    def openNewDialog(self):
        diag = NewDialog()
        #diag.setAttribute(Qt.WA_DeleteOnClose)
        rv = diag.exec_()
        if rv:
            self.dataModel.addItemHash(diag.getItemHash())

    def startTimer(self):
        selected_row = self.itemTable.currentIndex().row()
        for index in range(len(self.items)):
            if index == selected_row:
                self.items[index]["Inprogress"] = 1
            else:
                self.items[index]["Inprogress"] = 0

    def stopTimer(self):
        for index in range(len(self.items)):
            self.items[index]["Inprogress"] = 0

    def timerTick(self):
        for index in range(len(self.items)):
            if self.items[index]["Inprogress"] == 1:
                self.items[index]["Spent"] += 1
                i = self.dataModel.index(index, 4)
                self.itemTable.update(i)

    def save(self):
        diag = QFileDialog(self)
        diag.setFileMode(QFileDialog.AnyFile)
        rv = diag.exec_()
        if rv:
            fnames = diag.selectedFiles()
            out = file(fnames[0], "w")
            out.write(
                yaml.safe_dump(self.items,
                    encoding="utf8", allow_unicode=True))
            out.close()
            print self.items

    def load(self):
        diag = QFileDialog(self)
        diag.setFileMode(QFileDialog.AnyFile)
        rv = diag.exec_()
        if rv:
            fnames = diag.selectedFiles()
            infile = open(fnames[0], "r")
            lines = infile.read()
            print lines
            self.items = yaml.safe_load(lines)
            infile.close()
            print self.items
            self.dataModel = ItemModel(self.items)
            self.itemTable.setModel(self.dataModel)

class NewDialog(QDialog, Ui_Dialog):
    priorityLabels = ["High", "Medium", "Low"]
    statusLabels = ["New", "Deferred", "Done"]

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        for label in self.priorityLabels:
            self.priorityCBox.addItem(label)
        self.priorityCBox.setCurrentIndex(1)

        for label in self.statusLabels:
            self.statusCBox.addItem(label)
        self.statusCBox.setCurrentIndex(0)

        self.spent.setText("0")

    def qstr2unicode(self, qstr):
        return str(qstr.toUtf8()).decode("utf8")

    def getItemHash(self):
        itemHash = {"Title": self.qstr2unicode(self.title.text()),
            "Memo": self.qstr2unicode(self.memo.toPlainText()),
            "Priority": self.qstr2unicode(self.priorityCBox.itemText(
                                self.priorityCBox.currentIndex())),
            "Status": self.qstr2unicode(self.statusCBox.itemText(
                            self.statusCBox.currentIndex())),
            "Estimation": self.estimationSBox.value(),
            "Spent": float(self.spent.text()),
            "Inprogress": 0}
        return itemHash

class ItemModel(QAbstractTableModel):
    key_index = ["Title", "Priority", "Status", "Estimation", "Spent"]
    def __init__(self, data, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.modelData = data

    def rowCount(self, index=QModelIndex()):
        return len(self.modelData)

    def columnCount(self, index=QModelIndex()):
        return len(self.key_index)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            key = self.key_index[index.column()]
            val = self.modelData[index.row()][key]
            if isinstance(val, unicode):
                return QVariant(QString.fromUtf8(val.encode("utf8")))
            else:
                return QVariant(val)
        else:
            return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.key_index[col])
        return QVariant()

    def addItemHash(self, itemHash):
            dataLen = len(self.modelData)
            self.beginInsertRows(QModelIndex(), dataLen, dataLen)
            self.modelData.append(itemHash)
            self.endInsertRows()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.connect(w.actionQuit, SIGNAL("triggered()"), app, SLOT("quit()"))
    w.show()
    sys.exit(app.exec_())
