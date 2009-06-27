#!/usr/bin/python
# encoding: utf-8
import sys
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

    def openNewDialog(self):
        diag = NewDialog()
        #diag.setAttribute(Qt.WA_DeleteOnClose)
        rv = diag.exec_()
        if rv:
            import yaml
            itemHash = {"Title": str(diag.title.text().toUtf8()),
                "Memo": str(diag.memo.toPlainText().toUtf8()),
                "Priority": str(diag.priorityCBox.itemText(
                                    diag.priorityCBox.currentIndex())),
                "Status": str(diag.statusCBox.itemText(
                                diag.statusCBox.currentIndex())),
                "Estimation": diag.estimationSBox.value(),
                "Spent": str(diag.spent.text())}
            self.dataModel.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
            self.items.append(itemHash)
            self.dataModel.endInsertRows()
            print yaml.safe_dump(self.items, encoding="utf-8", allow_unicode=True)
        print rv

class NewDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.priorityCBox.addItem("High")
        self.priorityCBox.addItem("Medium")
        self.priorityCBox.addItem("Low")
        self.priorityCBox.setCurrentIndex(1)
        self.statusCBox.addItem("New")
        self.statusCBox.addItem("Deferred")
        self.statusCBox.addItem("Done")
        self.statusCBox.setCurrentIndex(0)
        self.spent.setText("0")

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
            return QVariant(QString.fromUtf8(str(self.modelData[index.row()][self.key_index[index.column()]])))
        else:
            return QVariant()
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.key_index[col])
        return QVariant()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
