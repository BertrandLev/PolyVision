import sys
from PyQt6.QtCore import Qt, QModelIndex, QAbstractProxyModel
from PyQt6.QtWidgets import QApplication, QTableView, QTreeView, QSplitter, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class CustomProxyModel(QAbstractProxyModel):
    def __init__(self):
        super().__init__()
        self.sourceModel = None

    def setSourceModel(self, sourceModel):
        self.sourceModel = sourceModel

    def mapToSource(self, proxyIndex):
        if not proxyIndex.isValid():
            return QModelIndex()
        sourceParent = self.sourceModel.index(0, 0)
        sourceIndex = self.sourceModel.index(proxyIndex.row(), proxyIndex.column() - 2, sourceParent)
        return sourceIndex

    def mapFromSource(self, sourceIndex):
        if not sourceIndex.isValid():
            return QModelIndex()
        row = sourceIndex.row()
        column = sourceIndex.column() + 2
        return self.createIndex(row, column)

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            sourceParent = self.sourceModel.index(row, 0)
        else:
            sourceParent = self.mapToSource(parent)

        sourceIndex = self.sourceModel.index(row, column - 2, sourceParent)
        return self.mapFromSource(sourceIndex)

    def parent(self, proxyIndex):
        sourceIndex = self.mapToSource(proxyIndex)
        sourceParent = sourceIndex.parent()
        return self.mapFromSource(sourceParent)

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return self.sourceModel.rowCount()
        else:
            return 0

    def columnCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return self.sourceModel.columnCount() + 2
        else:
            return 0


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        sourceModel = QStandardItemModel(4, 3)
        for row in range(4):
            for column in range(3):
                item = QStandardItem(f"Item {row}-{column}")
                sourceModel.setItem(row, column, item)

        proxyModel = CustomProxyModel()
        proxyModel.setSourceModel(sourceModel)

        splitter = QSplitter()
        tableView = QTableView()
        tableView.setModel(sourceModel)

        treeView = QTreeView()
        treeView.setModel(proxyModel)

        splitter.addWidget(tableView)
        splitter.addWidget(treeView)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setWindowTitle('Proxy Model Example')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
