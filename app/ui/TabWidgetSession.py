from PyQt6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QComboBox,
                             QGroupBox, QPushButton, QGridLayout)
from PyQt6.QtGui import QAction

class Session(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setupRequestTab()
        self.setupSelectionTab()
        self.setupAnalysisTab()
        self.setupExportTab()

    def setupRequestTab(self):
        self.request_tab = QWidget()
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
        self.request_tab.setLayout(layout)
        self.addTab(self.request_tab, "Request")

        # Connect signals and add functionality for the buttons here...

    def setupSelectionTab(self):
        self.selection_tab = QWidget()
        layout = QVBoxLayout()
        # Add widgets to the Selection tab
        self.selection_tab.setLayout(layout)
        self.addTab(self.selection_tab, "Selection")

    def setupAnalysisTab(self):
        self.analysis_tab = QWidget()
        layout = QVBoxLayout()
        # Add widgets to the Analysis tab
        self.analysis_tab.setLayout(layout)
        self.addTab(self.analysis_tab, "Analysis")

    def setupExportTab(self):
        self.export_tab = QWidget()
        layout = QVBoxLayout()
        # Add widgets to the Export tab
        self.export_tab.setLayout(layout)
        self.addTab(self.export_tab, "Export")

    def onSearchModeChanged(self, index):
        search_mode = index  # 0 for Quick Search, 1 for Advanced Search
        if search_mode == 0:
            print("Switched to Quick Search mode")
            # Implement logic for Quick Search mode
        else:
            print("Switched to Advanced Search mode")
            # Implement logic for Advanced Search mode