from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableView)

from my_module.model import PandasModel, GroupPandasModel
import pandas as pd

class AnalysisTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.lims_data = pd.DataFrame()
        self.lims_table_data = PandasModel(self.lims_data)

        self.query_result = QTableView()
        self.query_result.setModel(self.lims_table_data)

        layout = QVBoxLayout()
        layout.addWidget(self.query_result)
        # Add widgets to the Selection tab
        self.setLayout(layout)

    def update_df_data(self, df_data:pd.DataFrame):
        self.lims_data = df_data
        self.lims_table_data.set_dataFrame(self.lims_data)