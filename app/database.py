import pyodbc
import pandas as pd

def connection_LIMS():
    conn_str = (
        "DSN=ARAMIS7P64;"
        "UID=FELRRO;"
        "PWD=am2468"
    )
    try :
        connection = pyodbc.connect(conn_str)
        print('Connection to LIMS successful')
    except Exception as e:
        print("Connection failed. Error message",e)
        raise e
    return connection

def get_LIMS_data(sql_query,**kwargs):
    cnxn = connection_LIMS()
    cursor = cnxn.cursor()
    if 'parameters' in kwargs.keys():
        cursor.execute(sql_query, kwargs['parameters'])
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    cnxn.close()
    return pd.DataFrame.from_records(rows, columns=columns)

def get_LIMS_column_name(table_name):
    table_name = table_name.upper()
    cnxn = connection_LIMS()
    cursor = cnxn.cursor()
    if not cursor.tables(table=table_name).fetchone():
        return None
    sql = "SELECT * FROM {}".format(table_name)
    cursor.execute(sql)
    return [column[0] for column in cursor.description]

def get_LIMS_table_name():
    cnxn = connection_LIMS()
    cursor = cnxn.cursor()
    return [row.table_name for row in cursor.tables(
        schema = 'ARAMIS' , tableType = 'TABLE')]