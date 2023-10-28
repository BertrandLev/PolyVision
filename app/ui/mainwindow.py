from PyQt6.QtWidgets import (QMainWindow, QWidget, QToolBar, QMessageBox)
from PyQt6.QtGui import QAction
from ui.TabWidgetSession import Session

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 800, 600)  # Set initial window size
        
        # Session variable
        self.session = None

        # Central Widget
        self.setCentralWidget(QWidget())

        # Tool bar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        # Menu Bar
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        # New session Action
        new_session_action = QAction("New session", self)
        new_session_action.triggered.connect(self.session_new)
        file_menu.addAction(new_session_action)
        toolbar.addAction(new_session_action)

        # Close session Action
        close_session_action = QAction("Close session", self)
        close_session_action.triggered.connect(self.session_close)
        file_menu.addAction(close_session_action)
        toolbar.addAction(close_session_action)

        # Exit Action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menubar.addMenu("Help")

        # About Action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAboutDialog)
        help_menu.addAction(about_action)
        toolbar.addAction(about_action)

    def session_new(self):
        self.session = Session()
        self.setCentralWidget(self.session)

    def session_close(self):
        # implementer une demande de sauvegarde de session
        self.setCentralWidget(QWidget())
        self.session = None

    def showAboutDialog(self):
        about_text = "Data Analysis Application v1.0\n\nDeveloped by Bertrand Levaché"
        QMessageBox.about(self, "About Data Analysis Application", about_text)
