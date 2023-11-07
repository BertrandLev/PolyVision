import typing
from PyQt6 import QtCore
from PyQt6.QtCore import QModelIndex, QObject
from PyQt6.QtSql import QSqlQueryModel

class QuickQuery(QtCore.QAbstractTableModel):
    """
    A class to manage the creation of SQL queries.
    
    Attributes:
        conditions (list): contain the field, operator and values to create the where part of the query
    """
    def __init__(self) -> None:
        super(QuickQuery, self).__init__()
        self.conditions = []

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.conditions[index.row()][index.column()]
        
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

    def rowCount(self, index) -> int:
        return len(self.conditions)

    def columnCount(self, index):
        return 3

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        Titre_Col = ['Field','Operator','Value']
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return str(Titre_Col[section])

    def conditions_to_dict(self) -> dict:
        dict_cond = dict()
        for condition in self.conditions:
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
            SAMPLE.SAMPLE_NUMBER as Sample_Number , 
            SAMPLE.TEXT_ID as Sample_ID , 
            SAMPLE.STATUS as Sample_Status , 
            SAMPLE.PRODUCT as Product , 
            SAMPLE.MATERIAL_NAME as Material_Name , 
            TEST.ANALYSIS as Analysis , 
            TEST.REPLICATE_COUNT as Replicate , 
            RESULT.NAME as Result_Name , 
            RESULT.FORMATTED_ENTRY as Result , 
            SAMPLE.SAMPLE_NUMBER  
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
        for i, (key, value) in enumerate(self.conditions_to_dict().items()):
            my_string = ', '.join(f"'{item}'" for item in value)
            if i == 0:
                sql_query = sql_query + f"and {dict_conversion[key]} IN ({my_string})"
            else:
                sql_query = sql_query + f" or {dict_conversion[key]} IN ({my_string})"

        return sql_query
    
class TableToTreeProxyModel(QtCore.QAbstractProxyModel):
    """
    A completer
    """
    def __init__(self, sourceModel: QSqlQueryModel, parent = None) -> None:
        super(TableToTreeProxyModel,self).__init__(parent)
        self.setSourceModel(sourceModel)

    def mapFromSource(self, sourceIndex: QModelIndex) -> QModelIndex:
        if sourceIndex.isValid():
            return self.createIndex(sourceIndex.row(), sourceIndex.column())
        return QModelIndex()
    
    def mapToSource(self, proxyIndex: QModelIndex) -> QModelIndex:
        if proxyIndex.isValid():
            return self.sourceModel().index(proxyIndex.row(), proxyIndex.column())
        return QModelIndex()
    
    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        
        if not parent.isValid():  # top level
            parentItem = QModelIndex()
        elif parent.column() == 0:  # second level
            parentItem = self.sourceModel().index(row, 0, QModelIndex())
        else:  # third level
            parentItem = self.sourceModel().index(row, 1, QModelIndex())

        childItem = self.sourceModel().index(row, column, parentItem)

        if childItem.isValid():
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
    
    def parent(self, proxyIndex: QModelIndex = ...) -> QModelIndex:
        if not proxyIndex.isValid():
            return QModelIndex()
        childIndex = self.mapToSource(proxyIndex)
        if childIndex.column() == 0:  # top level
            return QModelIndex()
        elif childIndex.column() == 1:  # second level
            return self.mapFromSource(self.sourceModel().index(childIndex.row(), 0))
        else:  # third level
            return self.mapFromSource(self.sourceModel().index(childIndex.row(), 1))

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():  # top level
            return self.sourceModel().rowCount()
        elif parent.column() == 0:  # second level
            return self.sourceModel().columnCount() - 1
        else:  # third level
            return 0

    def columnCount(self, parent=QModelIndex()):
        return 3  # tree model has only one column

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.sourceModel().data(self.mapToSource(index), role)
        return None