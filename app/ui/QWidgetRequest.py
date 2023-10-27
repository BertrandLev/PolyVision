from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QComboBox,
                             QGroupBox, QPushButton, QGridLayout, QLabel,
                             QLineEdit, QListWidget)

class RequestTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()

        # Grid Layout
        grid_layout = QGridLayout()

        # Left Part of the Grid Layout
        # Top: Search Mode ComboBox
        search_mode_combobox = QComboBox()
        search_mode_combobox.addItem("Quick Search")
        search_mode_combobox.addItem("Advanced Search")
        grid_layout.addWidget(search_mode_combobox, 0, 0, 1, 2)  # row 0, column 0, span 1 row, 2 columns

        # Middle: Group Box
        groupbox_left = QGroupBox("Search Criteria")
        groupbox_layout = QGridLayout()
        
        # First Line: Search by Label and Dropdown List
        search_by_label = QLabel("Search by:")
        search_by_dropdown = QComboBox()
        search_by_dropdown.addItems(["DDT", "LIMS n°", "Product", "Material"])
        groupbox_layout.addWidget(search_by_label, 0, 0)
        groupbox_layout.addWidget(search_by_dropdown, 0, 1)

        # Second Line: Element Label, Text Entry, Add Button, List Button
        element_label = QLabel("Element:")
        element_entry = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.addToList(element_entry, search_list))
        list_button = QPushButton("...")
        list_button.clicked.connect(lambda: self.showList(search_list))
        groupbox_layout.addWidget(element_label, 1, 0)
        groupbox_layout.addWidget(element_entry, 1, 1)
        groupbox_layout.addWidget(add_button, 1, 2)
        groupbox_layout.addWidget(list_button, 1, 3)

        # Third Line: Current Search List Label
        current_list_label = QLabel("Current search list")
        groupbox_layout.addWidget(current_list_label, 2, 0, 1, 4)

        # Fourth Line: List Widget
        search_list = QListWidget()
        groupbox_layout.addWidget(search_list, 3, 0, 1, 4)

        groupbox_left.setLayout(groupbox_layout)
        grid_layout.addWidget(groupbox_left, 1, 0, 1, 2)  # row 1, column 0, span 1 row, 2 columns


        # Bottom: Preview Button
        preview_button = QPushButton("Preview")
        grid_layout.addWidget(preview_button, 2, 0, 1, 2)  # row 2, column 0, span 1 row, 2 columns

        # Right Part of the Grid Layout
        # Top: None
        
        # Middle: Group Box
        groupbox_right = QGroupBox("Result Details")
        grid_layout.addWidget(groupbox_right, 1, 2, 1, 1)  # row 1, column 2, span 1 row, 1 column

        # Bottom: Send to Selection Button
        send_to_selection_button = QPushButton("Send to Selection")
        grid_layout.addWidget(send_to_selection_button, 2, 2, 1, 1)  # row 2, column 2, span 1 row, 1 column

        layout.addLayout(grid_layout)
        self.setLayout(layout)

        # Connect signals and add functionality for the buttons here...

    def onSearchModeChanged(self, index):
        search_mode = index  # 0 for Quick Search, 1 for Advanced Search
        if search_mode == 0:
            print("Switched to Quick Search mode")
            # Implement logic for Quick Search mode
        else:
            print("Switched to Advanced Search mode")
            # Implement logic for Advanced Search mode

    def addToList(self, element_entry, search_list):
        element = element_entry.text()
        if element:
            search_list.addItem(element)
            element_entry.clear()

    def showList(self, search_list):
        list_content = [search_list.item(i).text() for i in range(search_list.count())]
        print("Current Search List:", list_content)