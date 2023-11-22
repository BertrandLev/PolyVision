from PyQt6 import QtCore
from PyQt6.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
import numpy as np
#CPO-CPR-23-0105
 
class QuickQuery(QtCore.QAbstractTableModel):
    """
    A class to manage the creation of SQL queries.
    
    Attributes:
        conditions (list): contain the field, operator and values to create the where part of the query
    """
    def __init__(self) -> None:
        super(QuickQuery, self).__init__()
        self._data = []
        

    def add_to_data(self, list_values:list):
        if len(list_values)==3:
            self._data.append(list_values)

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value,float):
                return "%.2f" % value
            return value
        
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

    def rowCount(self, index) -> int:
        return len(self._data)

    def columnCount(self, index):
        return 3

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        Titre_Col = ['Field','Operator','Value']
        column = Titre_Col[section]
        if orientation == QtCore.Qt.Orientation.Horizontal:
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return column
            
        return super().headerData(section, orientation, role)

    def model_to_dict(self) -> dict:
        dict_cond = dict()
        for condition in self._data:
            if not condition[0] in dict_cond.keys():
                dict_cond[condition[0]] = [condition[2]]
            else:
                dict_cond[condition[0]].append(condition[2])
        return dict_cond
    
    def createQuery(self) -> str:
    
        dict_conversion = {"Project Name" : "PROJECT.NAME",
                           "Sample Number" : "SAMPLE.SAMPLE_NUMBER",
                           "Product" : "SAMPLE.PRODUCT",
                           "Material" : "SAMPLE.MATERIAL_NAME"}
        sql_query = """
        select distinct 
            PROJECT.NAME as Project_Name , 
            CAST(SAMPLE.SAMPLE_NUMBER AS INT) as Sample_Number , 
            SAMPLE.PRODUCT as Product , 
            SAMPLE.MATERIAL_NAME as Material_Name , 
            TEST.ANALYSIS as Analysis , 
            TEST.REPLICATE_COUNT as Replicate , 
            RESULT.NAME as Result_Name , 
            RESULT.FORMATTED_ENTRY as Result
        from ((((((
            SAMPLE
            INNER JOIN PROJECT ON SAMPLE.PROJECT = PROJECT.NAME) 
            INNER JOIN TEST ON SAMPLE.SAMPLE_NUMBER = TEST.SAMPLE_NUMBER) 
            INNER JOIN RESULT ON TEST.TEST_NUMBER = RESULT.TEST_NUMBER) 
            LEFT JOIN UNITS ON RESULT.UNITS = UNITS.UNIT_CODE) 
            INNER JOIN PRODUCT ON SAMPLE.PRODUCT = PRODUCT.NAME and SAMPLE.PRODUCT_VERSION = PRODUCT.VERSION) 
            INNER JOIN X_MATERIAL ON SAMPLE.MATERIAL_NAME = X_MATERIAL.NAME) 
        where (
            SAMPLE.GROUP_NAME IN ( 'FELR' , 'CAR' , 'RHE' , 'SYSTEM_ANALYSIS' , 'CHEM_INV' , 'POLY' , 'DEFAULT' , 'MEC'))
            """
        for i, (key, value) in enumerate(self.model_to_dict().items()):
            my_string = ', '.join(f"'{item}'" for item in value)
            if i == 0:
                sql_query = sql_query + f"and {dict_conversion[key]} IN ({my_string})"
            else:
                sql_query = sql_query + f" or {dict_conversion[key]} IN ({my_string})"

        return sql_query

class PandasModel(QtCore.QAbstractItemModel):
    model_change = pyqtSignal(bool)

    def __init__(self, data:pd.DataFrame) -> None:
        super().__init__()
        self._root = QModelIndex()
        self.set_dataFrame(data)

    def set_dataFrame(self, data:pd.DataFrame):
        self._data = data
        # emit change
        self.model_change.emit(True)
        # emit change to views
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, 0)
        
    def data(self, index: QModelIndex, role: int) -> any:
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(),index.column()]
            if isinstance(value,np.int64):
                return int(value)
            if isinstance(value,np.float64):
                return float(value)
            return value

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
        return self._root
        
    def sort(self, column: int, order=Qt.SortOrder.AscendingOrder) -> None:
        if self.columnCount(self._root)>0:
            isAscending = True if order == Qt.SortOrder.AscendingOrder else False
            self.beginResetModel()
            # Sort the data using the sort_values method from dataframe
            self._data.sort_values(by= self._data.columns.values[column], ascending=isAscending, inplace=True)
            self.endResetModel()


class GroupPandasModel(QStandardItemModel):
    def __init__(self, columns:list[str]) -> None:
        super().__init__()
        self._groupColumns = columns

    @property
    def groupColumns(self):
        return self._groupColumns
    
    @groupColumns.setter
    def groupColumns(self, list_value:list[str]):
        self._groupColumns = list_value

    def create_model(self, data:pd.DataFrame) -> any:
        def is_key_exist(parent:QStandardItem, key:any) -> QStandardItem:
            # si la clef existe, on la renvoi, sinon on la créé et on la renvoi
            for row in range(parent.rowCount()):
                item = parent.child(row,0)
                item_value = item.data(Qt.ItemDataRole.DisplayRole)
                if item_value==key:
                    return item
            new_key = QStandardItem(str(key))
            new_key.setData(key,Qt.ItemDataRole.DisplayRole)
            parent.appendRow(new_key)
            return new_key
        
        def add_key(parent:QStandardItem,keys,values:pd.DataFrame) -> QStandardItem:
            print(keys)
            if len(keys) > 1:
                key = is_key_exist(parent,keys[0])
                add_key(key,keys[1:],values)
            else:
                key = is_key_exist(parent,keys[0])
                for _,cols in values.iterrows():
                    items = [QStandardItem("")]
                    for col in values.columns.values:
                        if col not in self._groupColumns:
                            item = QStandardItem()
                            item.setData(cols[col],Qt.ItemDataRole.DisplayRole)
                            items.append(item)
                    key.appendRow(items)
        
        if not all([column in data.columns.values for column in self._groupColumns]):
            print("columns must be a list of column from data")
            raise ValueError("columns must be a list of column from data")    

        self.clear()
        for keys, group in data.groupby(self._groupColumns):
            add_key(self.invisibleRootItem(),keys,group)

        header_values = [""] + [col for col in data.columns.values if col not in self._groupColumns]
        self.setHorizontalHeaderLabels(header_values)
        # emit change to views
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, 0)

    def data(self, index: QModelIndex, role: int) -> any:
        if not index.isValid():
            return None
        value = super().data(index,role)
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value,np.int64):
                return int(value)
            if isinstance(value,np.float64):
                return float(value)
        
        return value