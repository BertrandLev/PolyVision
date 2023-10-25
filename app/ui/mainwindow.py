
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 800, 600)  # Set initial window size

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Label
        label = QLabel("Welcome to the Data Analysis Application!")
        layout.addWidget(label)

        # Set the layout
        central_widget.setLayout(layout)
