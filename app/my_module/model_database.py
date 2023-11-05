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
        select distinct PROJECT.NAME as Project_Name , SAMPLE.SAMPLE_NUMBER as Sample_Number , SAMPLE.TEXT_ID as Sample_ID , SAMPLE.STATUS as Sample_Status , SAMPLE.PRODUCT as Product , SAMPLE.MATERIAL_NAME as Material_Name , TEST.ANALYSIS as Analysis , TEST.REPLICATE_COUNT as Replicate , RESULT.NAME as Result_Name , RESULT.FORMATTED_ENTRY as Result , 'J0401466' as CurrentUser,  'PROJECT_RESULTS' as SearchConfigKey, 'SAMPLE' as SearchTableName, SAMPLE.SAMPLE_NUMBER  from ((((((SAMPLE INNER JOIN PROJECT ON SAMPLE.PROJECT = PROJECT.NAME) INNER JOIN TEST ON SAMPLE.SAMPLE_NUMBER = TEST.SAMPLE_NUMBER) INNER JOIN RESULT ON TEST.TEST_NUMBER = RESULT.TEST_NUMBER) LEFT JOIN UNITS ON RESULT.UNITS = UNITS.UNIT_CODE) INNER JOIN PRODUCT ON SAMPLE.PRODUCT = PRODUCT.NAME and SAMPLE.PRODUCT_VERSION = PRODUCT.VERSION) INNER JOIN X_MATERIAL ON SAMPLE.MATERIAL_NAME = X_MATERIAL.NAME) where  (SAMPLE.GROUP_NAME IN ( 'FELR' , 'CAR' , 'RHE' , 'SYSTEM_ANALYSIS' , 'CHEM_INV' , 'POLY' , 'DEFAULT' , 'MEC'))  and PROJECT.NAME in ('CPO-CPR-23-0100')
        """,con
    )

    app = QApplication(sys.argv)
    view = QTableView()
    view.setModel(model)
    view.show()
    sys.exit(app.exec())