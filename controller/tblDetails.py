from controller.read_excel import ExcelProcessor
import pandas as pd

class DataProcessor(ExcelProcessor):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.group_list = {}
        self.phase_tenure = {}
        self.products = []

    def getPhaseTenure(self , PhaseName):
        df = pd.read_excel(self.file_path , sheet_name= "PhasesDetails")
        for index, row in df.iterrows():
            if row["Phases"] == PhaseName:
                return int(row['Tenure'])

    def tblHeaders(self):
        for phase, p_vals in self.merged_dicts().items():
            self.group_list[phase] = []
            new_p = phase.split("_")[0]
            if new_p in self.getPhases():
                self.phase_tenure[phase] = self.get_phase_tenure(new_p)
            for groups, g_vals in p_vals.items():
                self.group_list[phase].append(groups)
                for items, i_vals in g_vals.items():
                    if items == "qty" or items == "Select DB":
                        continue
                    self.products.append(items)

        self.products = list(set(self.products))
        tblHeaders = ["Phase Name", "Duration" , "Group Name", "Group Qty"]
        tblHeaders += self.products
        return tblHeaders
    
    def phaseTenure(self):
        phase_tenure = {}
        for phase, p_vals in self.merged_dicts().items():
            new_p = phase.split("_")[0]
            if new_p in self.getPhases():
                phase_tenure[phase] = self.get_phase_tenure(new_p)
        return phase_tenure
    
    def groupList(self):
        group_list = {}
        for phase, p_vals in self.merged_dicts().items():
            group_list[phase] = []
            for groups, g_vals in p_vals.items():
                group_list[phase].append(groups)
        return group_list

# if __name__ == "__main__":
#     file_path = "readExcel/template.xlsx"
#     excel_processor = ExcelProcessor(file_path)
#     excel_processor.process_excel()

#     data_processor = DataProcessor(file_path)
#     data_processor.process_data()
#     data_processor.create_excel()
