
from PyQt6.QtWidgets import (QTabWidget, QMainWindow)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
from ui.QWidgetRequest import RequestTab
from ui.QWidgetSelection import SelectionTab
from ui.QWidgetAnalysis import AnalysisTab
from ui.QWidgetExport import ExportTab

import pandas as pd

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
    data_updated = pyqtSignal(pd.DataFrame)

    def __init__(self, parent: QMainWindow) -> None:
        super(Session,self).__init__(parent)

        self.df_data = pd.DataFrame()
        # Création des quatres onglets
        self.request_tab = RequestTab()
        self.data_updated.connect(self.request_tab.update_df_data)
        self.request_tab.df_data_update.connect(self.update_df_data)
        self.addTab(self.request_tab, "Request")
        self.selection_tab = SelectionTab()
        self.addTab(self.selection_tab, "Selection")
        self.analysis_tab = AnalysisTab()
        self.data_updated.connect(self.analysis_tab.update_df_data)
        self.addTab(self.analysis_tab, "Analysis")

        self.export_tab = ExportTab()
        self.addTab(self.export_tab, "Export")

    def update_df_data(self, df_data:pd.DataFrame):
        self.df_data = df_data
        self.data_updated.emit(self.df_data)