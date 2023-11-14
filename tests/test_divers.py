import typing
from PyQt6.QtCore import QModelIndex, QObject, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, QWidget,
                            QVBoxLayout, QHBoxLayout, QPushButton, QTableView,
                            QTreeView)
from PyQt6 import QtCore
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd

import sys
sys.path.append("app")
from my_module import model

class pandasModel(QtCore.QAbstractItemModel):
    def __init__(self, data:pd.DataFrame) -> None:
        super().__init__()
        self._data = data
        self._root = QModelIndex()

    def data(self, index: QModelIndex, role: int) -> any:
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(),index.column()]
            return str(value)

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._data.index)
    
    def columnCount(self, parent: QModelIndex) -> int:
        return len(self._data.columns)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        if not parent:
            return super().index(row,column,self._root)
        else:
            return self.createIndex(row,column,parent)
        
    def parent(self, child:QModelIndex) -> QModelIndex:
        
        if not child.isValid():
            return QModelIndex()        
        else:
            return self._root
        
class groupPandasModel(QStandardItemModel):
    def __init__(self, data:pd.DataFrame, columns:list[str]) -> None:
        super().__init__()
        if not all([column in data.columns.values for column in columns]):
            raise ValueError("columns must be a list of column from data")
        self.create_model(data,columns)

    def create_model(self, data:pd.DataFrame, columns:list[str]) -> any:
        # def add_key(parent:QStandardItem,keys,values:pd.DataFrame) -> QStandardItem:
        #     if len(keys) > 1:
        #         key = QStandardItem()
        #         key.setData(keys[0],Qt.ItemDataRole.DisplayRole)
        #         parent.appendRow(key)
        #         add_key(key,keys[1:],values)
        #     else:
        #         key = QStandardItem()
        #         key.setData(keys[0],Qt.ItemDataRole.DisplayRole)
        #         parent.appendRow(key)
        #         for row,cols in values.iterrows():
        #             items = [QStandardItem("")]
        #             for col in values.columns.values:
        #                 if col not in columns:
        #                     item = QStandardItem()
        #                     item.setData(cols[col],Qt.ItemDataRole.DisplayRole)
        #                     items.append(item)
        #             key.appendRow(items)

        def is_key_exist(parent,value) -> QStandardItem:
            

        for keys, group in data.groupby(columns):
            add_key(self,keys,group)

        header_values = [""] + [col for col in data.columns.values if col not in columns]
        self.setHorizontalHeaderLabels(header_values)

class MultiLevelHeaderExample(QWidget):
    def __init__(self):
        super().__init__()

        data = [["sample",4,5,6],
                ["model",45,67,90],
                ["sample",4,45,9],
                ["model",3,5,7],
                ["sample",5,34,5]]
        
        # model pandas
        data_df = pd.DataFrame(data, columns=["colA","colB","colC","colD"])
        model_pandas = pandasModel(data_df)
        
        group_model_pandas = groupPandasModel(data_df,["colA","colB"])

        # Creation du model table
        table_model = QStandardItemModel(4,4)
        for row in range(table_model.rowCount()):
            for col in range(table_model.columnCount()):
                idx = table_model.index(row,col)
                table_model.setData(idx,data[row][col],QtCore.Qt.ItemDataRole.DisplayRole)

        #Creation du model arbre
        tree_model = QStandardItemModel()
        for row, columns in enumerate(data):
            root = QStandardItem()
            root.setData(data[row][0],QtCore.Qt.ItemDataRole.DisplayRole)
            tree_model.appendRow(root)
            values = []
            for col in columns[1:]:
                item = QStandardItem()
                item.setData(col,QtCore.Qt.ItemDataRole.DisplayRole)
                values.append(item)
            root.appendRow(values)
        tree_model.setHorizontalHeaderLabels(["1","2","3"])

        group_model = model.GroupbyColumnTableModel()
        group_model.setSourceModel(table_model)

        data = [["sample",4,5,6],
                ["model",45,67,90],
                ["sample",4,45,9],
                ["model",3,5,7],
                ["sample",5,34,5]]
        
        # model pandas
        data_df = pd.DataFrame(data, columns=["colA","colB","colC","colD"])
        model_pandas = pandasModel(data_df)
        
        group_model_pandas = groupPandasModel(data_df,["colA","colB"])

        # Creation du model table
        table_model = QStandardItemModel(4,4)
        for row in range(table_model.rowCount()):
            for col in range(table_model.columnCount()):
                idx = table_model.index(row,col)
                table_model.setData(idx,data[row][col],QtCore.Qt.ItemDataRole.DisplayRole)

        #Creation du model arbre
        tree_model = QStandardItemModel()
        for row, columns in enumerate(data):
            root = QStandardItem()
            root.setData(data[row][0],QtCore.Qt.ItemDataRole.DisplayRole)
            tree_model.appendRow(root)
            values = []
            for col in columns[1:]:
                item = QStandardItem()
                item.setData(col,QtCore.Qt.ItemDataRole.DisplayRole)
                values.append(item)
            root.appendRow(values)
        tree_model.setHorizontalHeaderLabels(["1","2","3"])

        group_model = model.GroupbyColumnTableModel()
        group_model.setSourceModel(table_model)

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Multi-Level Header Example')

        data = [
            ["Row 1", "Data 1-1", "Data 1-2", "Data 1-3", "Data 1-4", "Data 1-5"],
            ["Row 2", "Data 2-1", "Data 2-2", "Data 2-3", "Data 2-4", "Data 2-5"],
            ["Row 3", "Data 3-1", "Data 3-2", "Data 3-3", "Data 3-4", "Data 3-5"]
        ]

        table = QTableWidget(self)
        table.setRowCount(len(data))
        table.setColumnCount(len(data[0]))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        # Create a left panel widget
        left_panel = QWidget(splitter)
        left_table_view = QTableView()
        left_table_view.setModel(model_pandas)
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.addWidget(left_table_view)

        # Create a right panel widget
        right_panel = QWidget(splitter)
        right_tree_view = QTreeView()
        right_tree_view.setModel(group_model_pandas)
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.addWidget(right_tree_view)

        # Set up multi-level header model
        header_model = MultiLevelHeaderModel(1, 15, self)
        table.setHorizontalHeaderModel(header_model)

        # Allow selecting entire rows
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()