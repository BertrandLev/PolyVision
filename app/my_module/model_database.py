import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt6.QtWidgets import QTableView
from PyQt6.QtWidgets import QApplication

con = QSqlDatabase.addDatabase("QODBC","LIMS")
con.setDatabaseName("ARAMIS7P64")
con.setUserName("FELRRO")
con.setPassword("am2468")

if not con.open():
    print("Unable to connect to the database")
else:
    print("connection to LIMS")
    model = QSqlQueryModel()
    model.setQuery(
        """
        SELECT distinct
            ANALYSIS.LAB as "Lab",
            ANALYSIS.NAME as "Analysis"
        FROM
            ANALYSIS
        WHERE
            ANALYSIS.LAB in ('CAR','MEC','RHE')
            AND ANALYSIS.REMOVED = 'F'
            AND ANALYSIS.ACTIVE = 'T'
        """,con
    )

    app = QApplication(sys.argv)
    view = QTableView()
    view.setModel(model)
    view.show()
    sys.exit(app.exec())