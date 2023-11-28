import pandas as pd
from pprint import pprint
import re
import json
import openpyxl as xl


file = "template.xlsx"

xl_file = pd.ExcelFile(file)

SheetNames = xl_file.sheet_names
result = []
def getFromCommanSheets():
    for sheet in SheetNames:
        if sheet == "VM Working" or sheet == "product_mater" or sheet == "PhasesDetails":
            continue 
        df = pd.read_excel(file, sheet)
        for index , row in df.iterrows():
            # print(row)

            keyList = list(row.keys())
            for key in keyList:
                if  key == "SKU" or  key == "Product Name" or key == "group":
                    continue
                result.append({key+" "+sheet : []})
                
    unique_list = []
    unique_phase_keys = []
    for d in result:
        if d not in unique_list:
            unique_list.append(d)

    for dict in unique_list:
        unique_phase_keys.append(list(dict.keys())[0])
        
    # print(unique_phase_keys)
    unique_group_keys = []

    for sheet in SheetNames:
        if sheet == "VM Working" or sheet == "product_mater" or sheet == "PhasesDetails":
            continue 
        df = pd.read_excel(file, sheet)
        for index , row in df.iterrows():
            for key in unique_phase_keys:
                for i,val in enumerate(unique_list):
                    if pd.isna(row["Product Name"]):
                        try:
                            keyProduct = {row["SKU"] : []}
                            unique_list[i][key].append(keyProduct)
                        except KeyError:
                            continue
                        # print(unique_list[i][key])
                    try:
                        for dict in unique_list[i][key]:
                            unique_group_keys.append(list(dict.keys())[0])
                    except KeyError:
                            continue


    unique_group_keys = list(set(unique_group_keys))

    newP = []

    for sheet in SheetNames:
        if sheet == "VM Working" or sheet == "product_mater" or sheet == "PhasesDetails":
            continue 
        df = pd.read_excel(file, sheet)
        for index , row in df.iterrows():   
            for i,val in enumerate(unique_list):
                phase = list(unique_list[i].keys())[0]
                for g, group in enumerate(unique_list[i][phase]):
                    if pd.isna(row["Product Name"]):
                        continue
                    try:
                        group = list(unique_list[i][phase][g].keys())[0]
                        phase_id = phase.replace(" "+sheet, '')
                        try:
                            if group == row["group"]:
                                unique_list[i][phase][g][group].append({
                                    "product_name" : row["Product Name"],
                                    "product_sku" : row["SKU"],
                                    "product_qty" : row[phase_id]
                                })
                        except KeyError:
                            continue
                    except KeyError:
                        continue
    return unique_list


                

def getFromVmWorkingSheeet():
    result = []
    phases = []
    test = []
    import openpyxl as xl

    wb = xl.load_workbook(filename=file)

    for sheetName in wb.sheetnames:
        if sheetName == "VM Working":
            sheetData = wb[sheetName]
            for row in sheetData.iter_cols():
                for cell in row:
                    for merged_cell_range in sheetData.merged_cells.ranges:
                        if cell.coordinate in merged_cell_range:
                            if cell.value is None:
                                continue
                            if cell.value == "VM Details":
                                continue

                            # Check if the cell has a fill and get the RGB color
                            if cell.fill is not None and cell.fill.start_color is not None:
                                background_color = cell.fill.start_color
                                print(f"Background color of {cell.coordinate}: {background_color}")
                                # print(background_color) 
                            else:
                                print(f"No background color for {cell.coordinate}")

                            # Convert the value to string before appending
                            result.append({str(cell.value): []})
                            phases.append(str(cell.value))
                        else:
                            continue


                    

    # print(test)
getFromVmWorkingSheeet()