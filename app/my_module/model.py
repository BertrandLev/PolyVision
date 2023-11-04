from PyQt6 import QtCore
from PyQt6.QtSql import QSqlQuery

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

    # def preview_query(self) -> str:
    #     join_condition = ["/ ".join(condition) for condition in self.conditions]
    #     return "\n".join(join_condition)