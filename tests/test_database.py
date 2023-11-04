import sys
sys.path.append("app")
import database as LIMS
from PyQt6.QtSql import QSqlDatabase

LIMS.connection_LIMS()

LIMS.close_connection()

LIMS.remove_connection()