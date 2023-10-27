from PyQt6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout)
from PyQt6.QtGui import QAction

from ui.QWidgetRequest import RequestTab
from ui.QWidgetSelection import SelectionTab
from ui.QWidgetAnalysis import AnalysisTab
from ui.QWidgetExport import ExportTab

class Session(QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.setupRequestTab()
        self.setupSelectionTab()
        self.setupAnalysisTab()
        self.setupExportTab()

    def setupRequestTab(self):
        self.request_tab = RequestTab()
        self.addTab(self.request_tab, "Request")
        
    def setupSelectionTab(self):
        self.selection_tab = SelectionTab()
        self.addTab(self.selection_tab, "Selection")

    def setupAnalysisTab(self):
        self.analysis_tab = AnalysisTab()
        self.addTab(self.analysis_tab, "Analysis")

    def setupExportTab(self):
        self.export_tab = ExportTab()
        self.addTab(self.export_tab, "Export")
        