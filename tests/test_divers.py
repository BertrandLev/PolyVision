import typing
 Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, QWidget,
                            QVBoxLayout, QHBoxLayout, QPushButton, QTableView,
                            QTreeView)
from PyQt6 import QtCore
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
import numpy as np

import sys
sys.path.append("app")
from my_module import model




class MultiLevelHeaderExample(QWidget):
    def __init__(self):
        super().__init__()

        data = [[865123,1,"DSC","pic_fusion",115],
                [865123,1,"DSC","pic_crist",100],
                [865123,1,"DSC","enthalpie",250],
                [865124,1,"DSC","pic_crist",134],
                [865124,1,"DSC","pic_fusion",110],
                [865124,1,"DSC","enthalpie",300],]
        
        # model pandas
        data_df = pd.DataFrame(data, columns=["Sample","Replicat","Analysis","Result_name","Value"])
        model_pandas = pandasModel(data_df)
        
        pivot_data = data_df.pivot(index=["Sample","Replicat","Analysis"],
                                   columns="Result_name",values="Value").reset_index()

        pivot_model_pandas = pandasModel(pivot_data)
        group_model_pandas = groupPandasModel(data_df,["Sample","Replicat"])

        # Creation du model table
        table_model = QStandardItemModel(4,4)
        for row in range(table_model.rowCount()):
            for col in range(table_model.columnCount()):
                idx = table_model.index(row,col)
                table_model.setData(idx,data[row][col],Qt.ItemDataRole.DisplayRole)

        #Creation du model arbre
        tree_model = QStandardItemModel()
        for row, columns in enumerate(data):
            root = QStandardItem()
            root.setData(data[row][0],Qt.ItemDataRole.DisplayRole)
            tree_model.appendRow(root)
            values = []
            for col in columns[1:]:
                item = QStandardItem()
                item.setData(col,Qt.ItemDataRole.DisplayRole)
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
        self.table_pivot = QTableView()
        self.table_pivot.setModel(pivot_model_pandas)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.table_pivot)
        self.setLayout(self.layout)

app = QApplication([])
window = MultiLevelHeaderExample()
window.show()
app.exec()