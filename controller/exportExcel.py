from controller.tblDetails import DataProcessor
import xlsxwriter
import pandas as pd
import os


import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.worksheet._reader")

def exportExcel(file_path) :
    # try: 
        data_processor = DataProcessor(file_path)
        data = data_processor.merged_dicts()
        tbl_header = data_processor.tblHeaders()
        phase_list = data_processor.getPhases()
        phase_tenure = data_processor.phaseTenure()
        GetPhasesGroups = data_processor.GetPhasesGroups()

        def getIndexiveList(val , index , list_size):
            indexive_list = []
            for i in range(0,list_size):
                if i == index:
                    indexive_list.append(val)
                else:
                    indexive_list.append("")
            return indexive_list

        res = {}
        column = {}
        for phase, pVal in data.items():
            res[phase] = {}
            column[phase] = []
            for head in tbl_header:
                Length = len(GetPhasesGroups[phase])
                column[phase].append(head)
                if head == "Phase Name":
                    res[phase][head] = getIndexiveList(phase, 0, Length)        
                if head == "Duration":
                    res[phase][head] = getIndexiveList(phase_tenure[phase], 0, Length)
                if head == "Group Name":
                    res[phase][head] = GetPhasesGroups[phase]
                if head == "Group Qty":
                    res[phase][head] = []
                    for group in GetPhasesGroups[phase]:
                        if "VM" in group:
                            res[phase][head].append(pVal[group]["qty"])
                        else:
                            res[phase][head].append(1)
                if head not in ["Phase Name","Duration","Group Name","Group Qty"]:
                    res[phase][str(data_processor.read_product_master(head , "getProdId"))] = getIndexiveList("", 0 , Length)
                    res[phase][head] = getIndexiveList("", 0 , Length)
                    res[phase]["Recurring Discount - " + str(column[phase].index(head))] = getIndexiveList("", 0 , Length)


        for phase, pVal in data.items():
            Length = len(GetPhasesGroups[phase])
            for group in GetPhasesGroups[phase]:
                for Col, L in res[phase].items():
                    if Col not in ["Phase Name", "Duration", "Group Name", "Group Qty"]:
                        if "Recurring Discount" in Col:
                            try:
                                discount = data[phase][group][column[phase][int(Col.replace("Recurring Discount - " , ""))]]['discount'] 
                                res[phase]["Recurring Discount - " + str(Col.replace("Recurring Discount - " , ""))][GetPhasesGroups[phase].index(group)] = int(discount)
                            except KeyError:
                                res[phase]["Recurring Discount - " + str(Col.replace("Recurring Discount - " , ""))][GetPhasesGroups[phase].index(group)] = ""
                            except ValueError:
                                pass
                        else:
                            try:
                                product_qty = data[phase][group][Col]['product_qty']
                                res[phase][Col][GetPhasesGroups[phase].index(group)] = int(product_qty)
                                res[phase][str(data_processor.read_product_master(Col , "getProdId"))][GetPhasesGroups[phase].index(group)] = int(product_qty)
                            except KeyError:
                                res[phase][Col][GetPhasesGroups[phase].index(group)] = ""
                                res[phase][str(data_processor.read_product_master(head , "getProdId"))][GetPhasesGroups[phase].index(group)] = ""
                                
        outputFilePath = os.path.join("static", "output", "output.xlsx")
        with pd.ExcelWriter(outputFilePath, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('eNlight Instance')

            header_format = workbook.add_format({'bold': False, 'bg_color': '#0066ff', 'border': 1, "font_color" : "white" , 'text_wrap': True})
            column_width = 15
            worksheet.set_column(0, len(tbl_header) - 1, column_width)  # Assuming all rows have the same length

            for D, Arr in res.items():
                df = pd.DataFrame(Arr)

                df.to_excel(writer, sheet_name='eNlight Instance', startrow=0, startcol=0, index=False, header=False )

                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)

                for row_num in range(1, len(df) + 1):
                    for col_num in range(len(df.columns)):
                        worksheet.write(row_num, col_num, df.iloc[row_num - 1, col_num], workbook.add_format({'border': 1}))
        return True
    # except Exception as e:
    #     return False