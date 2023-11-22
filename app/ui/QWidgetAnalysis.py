from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableView)

from my_module.model import PandasModel, GroupPandasModel
import pandas as pd

class AnalysisTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.lims_data = pd.DataFrame()
        self.lims_table_data = PandasModel(self.lims_data)

        self.pivot_result = QTableView()
        self.pivot_result.setModel(self.lims_table_data)

        layout = QVBoxLayout()
        layout.addWidget(self.pivot_result)
        # Add widgets to the Selection tab
        self.setLayout(layout)

    def update_df_data(self, df_data:pd.DataFrame):
        self.lims_data = df_data.pivot(index=["PRODUCT","MATERIAL_NAME","SAMPLE_NUMBER","REPLICATE"],
                                   columns="RESULT_NAME",values="RESULT").reset_index()
        self.lims_table_data.set_dataFrame(self.lims_data)