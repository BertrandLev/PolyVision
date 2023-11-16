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
        def is_key_exist(parent:QStandardItem, key:str) -> QStandardItem:
            # si la clef existe, on la renvoi, sinon on la créé et on la renvoi
            for row in range(parent.rowCount()):
                item = parent.child(row,0)
                if item.text()==key:
                    return item
            new_key = QStandardItem(str(key))
            new_key.setData(key,Qt.ItemDataRole.DisplayRole)
            parent.appendRow(new_key)
            return new_key
        
        def add_key(parent:QStandardItem,keys,values:pd.DataFrame) -> QStandardItem:
            if len(keys) > 1:
                key = is_key_exist(parent,keys[0])
                add_key(key,keys[1:],values)
            else:
                key = is_key_exist(parent,keys[0])
                for _,cols in values.iterrows():
                    items = [QStandardItem("")]
                    for col in values.columns.values:
                        if col not in columns:
                            item = QStandardItem()
                            item.setData(cols[col],Qt.ItemDataRole.DisplayRole)
                            items.append(item)
                    key.appendRow(items)
            

        for keys, group in data.groupby(columns):
            print(keys)
            print(group)
            add_key(self.invisibleRootItem(),keys,group)

        header_values = [""] + [col for col in data.columns.values if col not in columns]
        self.setHorizontalHeaderLabels(header_values)

class MultiLevelHeaderExample(QWidget):
    def __init__(self):
        super().__init__()

        data = [["sample",4,5,6],
                ["model",9,67,90],
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

        # Creation des vues
        self.layout = QVBoxLayout()
        self.table = QTableView()
        self.table.setModel(model_pandas)
        self.tree = QTreeView()
        self.tree.setModel(group_model_pandas)
        self.tree.expandAll()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

        #Test
        idx = group_model_pandas.index(1,0,group_model_pandas.index(0,0))
        print(group_model_pandas.data(idx,Qt.ItemDataRole.DisplayRole))

    
app = QApplication([])
window = MultiLevelHeaderExample()
window.show()
app.exec()