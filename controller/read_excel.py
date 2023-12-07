import pandas as pd
import openpyxl as xl

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.result = {}
        self.phases = []

    def get_phase_tenure(self, phase_name):
        df = pd.read_excel(self.file_path, sheet_name="PhasesDetails")
        for index, row in df.iterrows():
            if row["Phases"] == phase_name:
                return int(row['Tenure'])

    def process_excel(self):
        for phase, p_vals in self.result.items():
            self.phases.append(phase)
            for groups, g_vals in p_vals.items():
                for items, i_vals in g_vals.items():
                    pass  # Your logic for processing Excel data

    def create_excel(self):
        wb = xl.Workbook()
        sheet = wb.create_sheet(title="Sheet")
        # Your logic for creating Excel goes here
        wb.save("output.xlsx")
