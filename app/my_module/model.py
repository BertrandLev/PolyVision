from PyQt6 import QtCore
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
    def __init__(self, groupColumns:list = [0], parent = None) -> None:
        super(QStandardItemModel,self).__init__(parent)
        self._groupColumns = groupColumns

    def setSourceModel(self, sourceModel: QSqlQueryModel) -> None:
        def add_to_dict(my_dict, keys, value):
            key = keys[0]
            if len(keys) == 1:
                if key not in my_dict:
                    my_dict[key] = set()
                my_dict[key].add(value)
            else:
                if key not in my_dict:
                    my_dict[key] = {}
                add_to_dict(my_dict[key], keys[1:], value)
        
        self.clear()
        group_values = {}
        #Extract unique value from groupbycolumn and all row that belong to this value
        for row in range(sourceModel.rowCount()):
            keys = []
            for col in self._groupColumns:
                keys.append(sourceModel.data(sourceModel.index(row,col)))
            add_to_dict(group_values, keys, row)
        
        #Add item in model
        def add_to_model(parent,my_dict:dict):
            for key, items in my_dict.items():
                child = QStandardItem(str(key))
                parent.appendRow(child)
                if isinstance(items,dict):
                    add_to_model(child,items)
                else:
                    for row in items:
                        parent.appendRow([QStandardItem("")] +
                            [QStandardItem(str(sourceModel.data(sourceModel.index(row,col)))) 
                            for col in range(sourceModel.columnCount()) if col not in self._groupColumns])

        add_to_model(self,group_values)
        
        header_values = [""] + [sourceModel.headerData(col,QtCore.Qt.Orientation.Horizontal,QtCore.Qt.ItemDataRole.DisplayRole)
                        for col in range(sourceModel.columnCount()) if col not in self._groupColumns]
        self.setHorizontalHeaderLabels(header_values)
        
    
#CPO-CPR-23-0105