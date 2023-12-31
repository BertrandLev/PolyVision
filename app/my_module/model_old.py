import typing
from PyQt6 import QtCore
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem

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


class GroupbyColumnTableModel(QStandardItemModel):
    """
    A completer
    """
    def __init__(self, groupColumns:list = [0], parent = None) -> None:
        super(QStandardItemModel,self).__init__(parent)
        self._groupColumns = groupColumns

    @property
    def groupColumns(self):
        return self._groupColumns
    
    @groupColumns.setter
    def groupColumns(self, list_value:list[int]):
        if any(value < 0 for value in list_value):
            raise ValueError("Value must be positive")
        self._groupColumns = list_value            

    def setSourceModel(self, sourceModel: QtCore.QAbstractTableModel) -> None:
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
        
        if max(self.groupColumns)>sourceModel.columnCount(): # test if groupColumn match with the new model
            raise ValueError("Groupby column value is higher than the number of column in the model")

        self.clear()
        group_values = {}
        #Extract unique value from groupbycolumn and all row that belong to this value
        for row in range(sourceModel.rowCount()):
            keys = []
            for col in self._groupColumns:
                keys.append(sourceModel.data(sourceModel.index(row,col)))
            add_to_dict(group_values, keys, row)
        
        #Add item in model
        def add_to_model(parent:QStandardItem,my_dict:dict):
            for key, items in my_dict.items():
                child = QStandardItem()
                child.setData(key,QtCore.Qt.ItemDataRole.DisplayRole)
                parent.appendRow(child)
                if isinstance(items,dict):
                    add_to_model(child,items)
                else:
                    for row in items:
                        values = [QStandardItem("")]
                        for col in range(sourceModel.columnCount()):
                            if col not in self._groupColumns:
                                item = QStandardItem()
                                item.setData(sourceModel.data(sourceModel.index(row,col)),QtCore.Qt.ItemDataRole.DisplayRole)
                                values.append(item)
                        parent.appendRow(values)

        add_to_model(self,group_values)

        header_values = [""] + [str(sourceModel.headerData(col,QtCore.Qt.Orientation.Horizontal,QtCore.Qt.ItemDataRole.DisplayRole))
                        for col in range(sourceModel.columnCount()) if col not in self._groupColumns]
        self.setHorizontalHeaderLabels(header_values)


class PivotResultTableModel(QStandardItemModel):
    """
    Pivote les colonnes Result_Name et Result
    A completer
    """
    def __init__(self,parent = None) -> None:
        super(QStandardItemModel,self).__init__(parent)

    def setSourceModel(self, sourceModel: QtCore.QAbstractTableModel) -> None:
        """
        A completer
        """       
        def add_to_dict(my_dict, keys, value):
            key = keys[0] + "_" + keys[1]
            if key not in my_dict:
                my_dict[key] = set()
            my_dict[key].add(value)
            
        self.clear()
        header_values = []
        pivot_index = {}
        group_index = {}
        for col in range(sourceModel.columnCount()):
            column_name = sourceModel.headerData(col,QtCore.Qt.Orientation.Horizontal,QtCore.Qt.ItemDataRole.DisplayRole)
            if column_name in ('Analysis','Result_name','Result'):
                pivot_index[column_name] = col
            else:
                group_index[column_name] = col
                header_values.append(column_name)
  
        new_headers = []
        groups_row = {}
        for row in range(sourceModel.rowCount()):
            # Trouve les lignes correspondant aux couples unique des colonnes non pivotées
            keys = []
            for col in group_index:
                keys.append(sourceModel.data(sourceModel.index(row,col)))
            add_to_dict(groups_row,keys,row)
            # Récupère les couples (analyses,result_name)
            header = sourceModel.data(sourceModel.index(row,pivot_index['Analysis'])) + "_" + sourceModel.data(sourceModel.index(row,pivot_index['Result_name']))
            new_headers.append(header)

        header_values = header_values + new_headers # ajoute les colonnes aux headers
        
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

    
        




        # header_values = [""] + [sourceModel.headerData(col,QtCore.Qt.Orientation.Horizontal,QtCore.Qt.ItemDataRole.DisplayRole)
        #                 for col in range(sourceModel.columnCount()) if col not in self._groupColumns]
        # self.setHorizontalHeaderLabels(header_values)
