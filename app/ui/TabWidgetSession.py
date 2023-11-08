import typing
from PyQt6.QtWidgets import (QTabWidget, QWidget, QToolBar, QMainWindow)
from PyQt6.QtGui import QAction
from ui.QWidgetRequest import RequestTab
from ui.QWidgetSelection import SelectionTab
from ui.QWidgetAnalysis import AnalysisTab
from ui.QWidgetExport import ExportTab

class Session(QTabWidget):
    """
    Cette classe gère les intéractions et échange de données entre les différents onglets d'une session.

    Attributes:
        RequestTab (object) : Contient l'onglet qui va gérer la partie requete
        SelectionTab (object) : Contient l'onglet qui va gérer la sélection des échantillons
        AnalysisTab (object) : Contient l'onglet qui permet l'analyse des données
        ExportTab (object) : Contient l'onglet qui permet l'export des données
        
    Returns:
        
    """
    def __init__(self, parent: QMainWindow) -> None:
        super(Session,self).__init__(parent)

        # Création des quatres onglets
        self.request_tab = RequestTab()
        self.addTab(self.request_tab, "Request")
        self.selection_tab = SelectionTab()
        self.addTab(self.selection_tab, "Selection")
        self.analysis_tab = AnalysisTab()
        self.addTab(self.analysis_tab, "Analysis")
        self.export_tab = ExportTab()
        self.addTab(self.export_tab, "Export")
