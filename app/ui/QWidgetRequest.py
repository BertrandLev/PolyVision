from PyQt6 import QtCore
from PyQt6.QtWidgets import (QTableView, QTreeView, QWidget, QVBoxLayout, QComboBox,
                             QGroupBox, QPushButton, QGridLayout, QLabel,
                             QLineEdit, QMenu, QHeaderView,
                             QTableWidgetItem, QHeaderView)
from PyQt6.QtGui import QAction
from PyQt6.QtSql import QSqlQuery, QSqlQueryModel, QSqlDatabase
from my_module.model import QuickQuery, TableToTreeProxyModel
import database as LIMS

class QuickSearch(QGroupBox):
    def __init__(self, query:QuickQuery ) -> None:
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
        search_table = QTableView()
        search_table.setModel(query)

        # Add table features
        search_table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        search_table.customContextMenuRequested.connect(lambda event: self.openTableContextMenu(event,search_table, query))
        
        layout.addWidget(search_table, 3, 0, 1, 4)
        
        # Set layout to groupbox_left
        self.setLayout(layout)

    def addToTable(self, field_entry: QComboBox, value_entry: QLineEdit , query: QuickQuery):
        field = field_entry.currentText()
        value = value_entry.text()
        if value:
            query.conditions.append((field,"=",value))
            query.layoutChanged.emit()
            value_entry.setText("")

    def deleteSelectedItem(self, tableView : QTableView, query: QuickQuery):
        indexes = tableView.selectedIndexes()
        if indexes:
            for index in indexes:
                del query.conditions[index.row()]
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
    def __init__(self) -> None:
        super().__init__()
        self.query = QuickQuery()
        self.lims_table_data = QSqlQueryModel()
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
        grid_layout.addWidget(groupbox_left, 1, 0, 1, 2)  # row 1, column 0, span 1 row, 2 columns

        # Bottom: Preview Button
        preview_button = QPushButton("Preview")
        preview_button.clicked.connect(lambda: self.preview_query(search_mode_combobox))
        grid_layout.addWidget(preview_button, 2, 0, 1, 2)  # row 2, column 0, span 1 row, 2 columns

        # Right Part of the Grid Layout
        # Middle: Group Box
        self.query_result = QTableView()
        self.query_result.setModel(self.lims_table_data)
        grid_layout.addWidget(self.query_result, 1, 2, 1, 1)  # row 1, column 2, span 1 row, 1 column
        self.queryTree_result = QTreeView()
        self.queryTree_result.setModel(TableToTreeProxyModel(self.lims_table_data))
        grid_layout.addWidget(self.queryTree_result, 2, 2, 1, 1)  # row 1, column 2, span 1 row, 1 column

        # Bottom: Send to Selection Button
        send_to_selection_button = QPushButton("Send to Selection")
        grid_layout.addWidget(send_to_selection_button, 3, 2, 1, 1)  # row 2, column 2, span 1 row, 1 column

        layout.addLayout(grid_layout)
        self.setLayout(layout)

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
            self.lims_table_data.setQuery(my_query)
            print("End of data update")
        else:
            print("erreur à l'ouverture du LIMS")
        
    def add_to_query(self, search_mode):
        if search_mode == 0: # Logic for Quick Search mode
            print("Quick")
        else: # Logic for Advanced Search mode
            print('Advance')
        