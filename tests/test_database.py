import sys
sys.path.append("app")
import database as LIMS
from PyQt6.QtSql import QSqlDatabase
import pandas as pd



LIMS.connection_LIMS_MSQLServer()

LIMS.close_connection()

# LIMS.remove_connection()

