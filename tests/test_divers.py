from PyQt6.QtWidgets import QApplication, QTableView, QHeaderView, QVBoxLayout, QWidget, QTableWidget, QAbstractItemView, QStandardItemModel, QStandardItem

class MultiLevelHeaderModel(QStandardItemModel):
    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 1 or section == 2 or section == 3:
                return "Header 1"
            elif section == 4 or section == 5:
                return "Header 2"
            elif section == 0:
                return ""
            elif section == 6:
                return "Sub 1"
            elif section == 7 or section == 8:
                return "Sub 2"
            elif section == 9 or section == 10:
                return "Sub 3"
            elif section == 11 or section == 12:
                return "Sub 4"
            elif section == 13 or section == 14:
                return "Sub 5"
        return super().headerData(section, orientation, role)

class MultiLevelHeaderExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Multi-Level Header Example')

        data = [
            ["Row 1", "Data 1-1", "Data 1-2", "Data 1-3", "Data 1-4", "Data 1-5"],
            ["Row 2", "Data 2-1", "Data 2-2", "Data 2-3", "Data 2-4", "Data 2-5"],
            ["Row 3", "Data 3-1", "Data 3-2", "Data 3-3", "Data 3-4", "Data 3-5"]
        ]

        table = QTableWidget(self)
        table.setRowCount(len(data))
        table.setColumnCount(len(data[0]))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        # Set up the vertical header (leftmost column)
        vertical_header = table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Set up the horizontal header
        horizontal_header = table.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Set up multi-level header model
        header_model = MultiLevelHeaderModel(1, 15, self)
        table.setHorizontalHeaderModel(header_model)

        # Allow selecting entire rows
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Create layout and add the table
        layout = QVBoxLayout(self)
        layout.addWidget(table)

if __name__ == '__main__':
    app = QApplication([])
    example = MultiLevelHeaderExample()
    example.show()
    app.exec()
