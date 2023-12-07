from controller.read_excel import ExcelProcessor

class DataProcessor(ExcelProcessor):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.group_list = {}
        self.phase_tenure = {}
        self.products = []

    def process_data(self):
        for phase, p_vals in self.result.items():
            self.group_list[phase] = []
            new_p = phase.split("_")[0]
            if new_p in self.get_phases():
                self.phase_tenure[phase] = self.get_phase_tenure(new_p)
            for groups, g_vals in p_vals.items():
                self.group_list[phase].append(groups)
                for items, i_vals in g_vals.items():
                    self.products.append(items)

        self.products = list(set(self.products))

# if __name__ == "__main__":
#     file_path = "readExcel/template.xlsx"
#     excel_processor = ExcelProcessor(file_path)
#     excel_processor.process_excel()

#     data_processor = DataProcessor(file_path)
#     data_processor.process_data()
#     data_processor.create_excel()
