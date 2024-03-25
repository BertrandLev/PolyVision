from PyQt6 import QtCore
from PyQt6.QtWidgets import (QTableView, QTreeView, QWidget, QVBoxLayout, QComboBox,
                             QGroupBox, QPushButton, QGridLayout, QLabel,
                             QLineEdit, QMenu, QSplitter, QHeaderView, QAbstractItemView,
                             QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QAction
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from my_module.model import MyQuery, QuickQuery, PandasModel, GroupPandasModel
import database as LIMS
import pandas as pd

class QuickSearch(QGroupBox):
    # def __init__(self, query:QuickQuery ) -> None:
    def __init__(self, query:MyQuery ) -> None:
        super().__init__(title = "Search Criteria")

        layout = QGridLayout()
        
        # First Line: Search by Label and Dropdown List
        search_by_label = QLabel("Search by:")
        search_by_dropdown = QComboBox()
        search_by_dropdown.addItems(["Project Name", "Sample Number", "Product", "Material"])
        layout.addWidget(search_by_label, 0, 0)
        layout.addWidget(search_by_dropdown, 0, 1)
        
        # Second Line: Element Label, Text Entry, Add Button, List Button
        element_label = QLabel("Element:")
        value_entry = QLineEdit()
        value_entry.returnPressed.connect(lambda: self.addToTable(search_by_dropdown, value_entry, query))
        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.addToTable(search_by_dropdown, value_entry, query))
        list_button = QPushButton("...")
        list_button.clicked.connect(lambda: self.showList(search_table))
        layout.addWidget(element_label, 1, 0)
        layout.addWidget(value_entry, 1, 1)
        layout.addWidget(add_button, 1, 2)
        layout.addWidget(list_button, 1, 3)
        
        # Third Line: Current Search List Label
        current_list_label = QLabel("Current search list")
        layout.addWidget(current_list_label, 2, 0, 1, 4)
        
        # Fourth Line: List Widget
        # search_table = QTableView()
        search_table = QTreeView()
        search_table.setModel(query)
        # search_table.setColumnWidth(0,110)
        # search_table.setColumnWidth(1,80)
        # search_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        # search_table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        # search_table.verticalHeader().setFixedWidth(20)
        # search_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Add table features
        # search_table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        # search_table.customContextMenuRequested.connect(lambda event: self.openTableContextMenu(event,search_table, query))
        
        layout.addWidget(search_table, 3, 0, 1, 4)
        
        # Set layout to groupbox_left
        self.setLayout(layout)

    # def addToTable(self, field_entry: QComboBox, value_entry: QLineEdit , query: QuickQuery):
    def addToTable(self, field_entry: QComboBox, value_entry: QLineEdit , query: MyQuery):
        field = field_entry.currentText()
        value = value_entry.text()
        if value:
            # query.add_to_data((field,"=",value))
            query.add_to_data(field,value)
            query.layoutChanged.emit()
            value_entry.setText("")

    def deleteSelectedItem(self, tableView : QTableView, query: QuickQuery):
        indexes = tableView.selectedIndexes()
        if indexes:
            for index in indexes:
                del query._data[index.row()]
            query.layoutChanged.emit()
            tableView.clearSelection()

    def showList(self, search_table: QTableView):
        pass
        # list_content = [search_table.item(i).text() for i in range(search_table.count())]
        # print("Current Search List:", list_content)
        
    def openTableContextMenu(self, event, search_table: QTableView, query: QuickQuery):
        context_menu = QMenu(search_table)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.deleteSelectedItem(search_table, query))
        context_menu.addAction(delete_action)
        context_menu.exec(search_table.mapToGlobal(event))

class RequestTab(QWidget):
    df_data_update = QtCore.pyqtSignal(pd.DataFrame)

    def __init__(self) -> None:
        super().__init__()
        # self.query = QuickQuery()
        self.query = MyQuery()
        self.lims_data = pd.DataFrame()
        self.lims_table_data = PandasModel(self.lims_data)
        self.lims_tree_data = GroupPandasModel(["PROJECT_NAME","SAMPLE_NUMBER","ANALYSIS","REPLICATE"])
        self.lims_table_data.model_change.connect(self.update_tree_data)
        layout = QVBoxLayout()

        # Grid Layout
        grid_layout = QGridLayout()
        
        # Left Part of the Grid Layout
        # Top: Search Mode ComboBox
        search_mode_combobox = QComboBox()
        search_mode_combobox.addItem("Quick Search")
        search_mode_combobox.addItem("Advanced Search")
        search_mode_combobox.currentIndexChanged.connect(self.onSearchModeChanged)  # Connect signal to a method
        grid_layout.addWidget(search_mode_combobox, 0, 0, 1, 2)  # row 0, column 0, span 1 row, 2 columns
        # Middle: Group Box
        groupbox_left = QuickSearch(self.query)        
        grid_layout.addWidget(groupbox_left, 1, 0, 2, 2)  # row 1, column 0, span 1 row, 2 columns
        # Bottom: Preview Button
        preview_button = QPushButton("Launch Query")
        preview_button.clicked.connect(lambda: self.preview_query(search_mode_combobox))
        grid_layout.addWidget(preview_button, 3, 0, 1, 2)  # row 2, column 0, span 1 row, 2 columns

        # Right Part of the Grid Layout
        # Use of a splitter
        splitter  = QSplitter(self)
        splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        grid_layout.addWidget(splitter, 0,2,3,1)  # row 1, column 2, span 3 row, 1 column
        # Top
        upper_pannel = QWidget(splitter)
        upper_pannel_layout = QVBoxLayout(upper_pannel)
        self.query_result = QTableView()
        self.query_result.setModel(self.lims_table_data)
        self.query_result.setSortingEnabled(True)
        self.query_result.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.query_result.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.query_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.query_result.horizontalHeader().sortIndicatorChanged.connect(self.onSortIndicatorChanged)
        upper_pannel_layout.addWidget(self.query_result) 
        # Bot
        bot_pannel = QWidget(splitter)
        bot_pannel_layout = QGridLayout(bot_pannel)        
        tree_mode_combobox = QComboBox()
        tree_mode_combobox.setEnabled = False
        tree_mode_combobox.addItem("Groupby DDT")
        tree_mode_combobox.addItem("Groupby Material")
        tree_mode_combobox.currentIndexChanged.connect(self.onTreeModeChanged)  # Connect signal to a method
        bot_pannel_spacer = QSpacerItem(20,40,QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        bot_pannel_layout.addWidget(tree_mode_combobox,0,0,1,1)
        bot_pannel_layout.addItem(bot_pannel_spacer,0,1,1,1)
        self.queryTree_result = QTreeView()
        self.queryTree_result.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.queryTree_result.setModel(self.lims_tree_data)
        self.queryTree_result.setExpandsOnDoubleClick(True)    
        self.queryTree_result.header().setMinimumSectionSize(150)
        self.queryTree_result.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.queryTree_result.header().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        bot_pannel_layout.addWidget(self.queryTree_result,1,0,1,2)  # row 1, column 2, span 1 row, 1 column
        bot_pannel_layout.setColumnStretch(1, 1)
        # Bottom: Send to Selection Button
        send_to_selection_button = QPushButton("Send to Selection")
        grid_layout.addWidget(send_to_selection_button, 3, 2, 1, 1)  # row 2, column 2, span 1 row, 1 column
        grid_layout.setColumnMinimumWidth(1, 150)
        grid_layout.setColumnStretch(2, 1)
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def onSortIndicatorChanged(self, column, order):
        self.lims_table_data.sort(column,order)

    def update_tree_data(self, value:bool):
        self.lims_tree_data.create_model(self.lims_data)
        self.queryTree_result.expandAll()

    def onTreeModeChanged(self, index):
        display_mode = index  # 0 for groupby DDT, 1 for groupby Material
        if display_mode == 0:
            print("Switched to groupby DDT mode")
            self.lims_tree_data.groupColumns = ["PROJECT_NAME","SAMPLE_NUMBER","ANALYSIS","REPLICATE"]
        else:
            print("Switched to groupby Material mode")
            self.lims_tree_data.groupColumns = ["PRODUCT","MATERIAL_NAME","ANALYSIS","REPLICATE"]
        if self.lims_tree_data.rowCount()>0:
            self.lims_tree_data.create_model(self.lims_data)
            self.queryTree_result.expandAll()

    def onSearchModeChanged(self, index):
        pass
        # search_mode = index  # 0 for Quick Search, 1 for Advanced Search
        # if search_mode == 0:
        #     print("Switched to Quick Search mode")
        # else:
        #     print("Switched to Advanced Search mode")

    def preview_query(self, search_mode):
        if LIMS.connection_LIMS():
            con = QSqlDatabase.database("LIMS")
            my_query = QSqlQuery(self.query.createQuery(), con)
            results = []
            titles = []
            record = my_query.record()
            for i in range(record.count()):
                titles.append(record.fieldName(i))
            while my_query.next():
                row = []
                for i in range(record.count()):
                    row.append(my_query.value(i))
                results.append(row)
            self.lims_data = pd.DataFrame(data=results, columns=titles)
            self.lims_table_data.set_dataFrame(self.lims_data)
            self.df_data_update.emit(self.lims_data)
            my_query.finish()
            LIMS.close_connection()
            LIMS.remove_connection()
            print("End of data update")
        else:
            print("erreur à l'ouverture du LIMS")
        
    def add_to_query(self, search_mode):
        if search_mode == 0: # Logic for Quick Search mode
            print("Quick")
        else: # Logic for Advanced Search mode
            print('Advance')
        
    def update_df_data(self, df_data:pd.DataFrame):
        self.lims_data = df_data
        self.lims_table_data.set_dataFrame(self.lims_data)