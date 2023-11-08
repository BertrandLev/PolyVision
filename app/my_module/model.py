import typing
from PyQt6 import QtCore
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, QObject
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem


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
    
class GroupbyColumnTableModel(QStandardItemModel):
    """
    A completer
    """
    def __init__(self, groupColumn:int = 0, parent = None) -> None:
        super(QStandardItemModel,self).__init__(parent)
        self._groupColumn = groupColumn
        self.setHorizontalHeaderLabels()

    def setSourceModel(self, sourceModel: QSqlQueryModel) -> None:
        self.clear()
        group_values = {}

        #Extract unique value from groupbycolumn and all row that belong to this value
        for row in range(sourceModel.rowCount()):
            index = sourceModel.index(row,self._groupColumn)
            group_name = sourceModel.data(index)
            if not group_name in group_values.keys():
                group_values[group_name] = set()
            group_values[group_name].add(row)
        
        #Add item in model
        for key,rows in group_values.items():
            group_item = QStandardItem(str(key))
            self.appendRow(group_item)
            for row in rows:
                first_value = QStandardItem(str(sourceModel.data(sourceModel.index(row,1))))
                second_value = QStandardItem(str(sourceModel.data(sourceModel.index(row,2))))
                group_item.appendRow([QStandardItem(""),first_value, second_value])
                # first_value.appendColumn(
                #     [QStandardItem(str(sourceModel.data(sourceModel.index(row,col)))) for col in range(1,sourceModel.columnCount())])
                # group_item.appendRow(
                #     [QStandardItem(str(sourceModel.data(sourceModel.index(row,col)))) for col in range(1,sourceModel.columnCount())])
        self.setHorizontalHeaderLabels()
        
    def setHorizontalHeaderLabels(self, labels=None) -> None:
        super().setHorizontalHeaderLabels(['DDT','Sample_number','Sample_ID'])