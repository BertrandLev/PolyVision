from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox

def connection_LIMS() -> bool:
    con = QSqlDatabase.addDatabase("QODBC","LIMS")
    con.setDatabaseName("ARAMIS7P64")
    con.setUserName("FELRRO")
    con.setPassword("am2468")
    if not con.open():
        QMessageBox.critical(
            None,
            "Polyvision - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True

def close_connection(connection_name : str = "LIMS") -> None:
    con = QSqlDatabase.database(connectionName=connection_name, open=False)
    if con.isOpen():
        con.close()

def remove_connection(connection_name: str = "LIMS") -> list:
    if connection_name in QSqlDatabase.connectionNames():
        QSqlDatabase.removeDatabase(connection_name)
    return QSqlDatabase.connectionNames()




# def get_LIMS_data(sql_query,**kwargs):
#     cnxn = connection_LIMS()
#     cursor = cnxn.cursor()
#     if 'parameters' in kwargs.keys():
#         cursor.execute(sql_query, kwargs['parameters'])
#     else:
#         cursor.execute(sql_query)
#     rows = cursor.fetchall()
#     columns = [column[0] for column in cursor.description]
#     cursor.close()
#     cnxn.close()
#     return pd.DataFrame.from_records(rows, columns=columns)

# def get_LIMS_column_name(table_name):
#     table_name = table_name.upper()
#     cnxn = connection_LIMS()
#     cursor = cnxn.cursor()
#     if not cursor.tables(table=table_name).fetchone():
#         return None
#     sql = "SELECT * FROM {}".format(table_name)
#     cursor.execute(sql)
#     return [column[0] for column in cursor.description]

# def get_LIMS_table_name():
#     cnxn = connection_LIMS()
#     cursor = cnxn.cursor()
#     return [row.table_name for row in cursor.tables(
#         schema = 'ARAMIS' , tableType = 'TABLE')]