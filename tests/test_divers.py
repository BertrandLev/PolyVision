from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a splitter widget
        splitter = QSplitter(self)

        # Create a left panel widget
        left_panel = QWidget(splitter)
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.addWidget(QPushButton("Button 1"))
        left_panel_layout.addWidget(QPushButton("Button 2"))

        # Create a right panel widget
        right_panel = QWidget(splitter)
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.addWidget(QPushButton("Button 3"))
        right_panel_layout.addWidget(QPushButton("Button 4"))

        # Add the panels to the splitter widget
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        # Set the splitter widget as the central widget of the main window
        self.setCentralWidget(splitter)

        # Create a button to show/hide the left panel
        toggle_button = QPushButton("Toggle Left Panel", self)
        toggle_button.clicked.connect(lambda: left_panel.setVisible(not left_panel.isVisible()))
        self.addToolBar("Toggle").addWidget(toggle_button)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()