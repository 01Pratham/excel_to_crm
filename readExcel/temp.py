import pandas as pd
from pprint import pprint
import re
import json
import openpyxl as xl


file = "readExcel/template.xlsx"

xl_file = pd.ExcelFile(file)

SheetNames = xl_file.sheet_names
result ={}
def getFromCommanSheets():
    phases = []
    for sheet in SheetNames:
        if sheet == "VM Working" or sheet == "product_mater":
            continue 
        if sheet == "PhasesDetails" : 
            dfPhases = pd.read_excel(file, sheet)
            for index , row in dfPhases.iterrows():
                phases.append(row['Phases'])
                for sheet2 in SheetNames:
                    if sheet2 == "PhasesDetails" or sheet2 == "VM Working" or sheet2 == "product_mater":
                        continue
                    result[row['Phases'] +"_"+ sheet2 ] = {}
        else:
            df = pd.read_excel(file, sheet)
            for index , row in df.iterrows():
                for key , val in row.to_dict().items():
                    if key == "group":
                        for phase in phases:
                            if pd.isna(row["group"]):
                                continue
                            result[phase +"_"+sheet][row["group"]] = {}
                    
    for sheet in SheetNames:
        if sheet == "VM Working" or sheet == "product_mater" or sheet == "PhasesDetails":
            continue 
        df = pd.read_excel(file, sheet)
        for index , row in df.iterrows():
            for phase in phases:
                if not pd.isna(row["Product Name"]):
                    result[phase +"_"+sheet][row["group"]][row["Product Name"]] = {
                        "product_qty" : row[phase],
                        "product_sku" : "CCVRAT0000000000"
                    }
              
    return result
def getFromVmWorkingSheeet():
    result = {}
    phases = []
    group = []
    let= []

    for sheet in SheetNames:
        if sheet == "PhasesDetails":
            dfPhases = pd.read_excel(file, sheet)
            for index , row in dfPhases.iterrows():
                phases.append(row['Phases'])
                result[row['Phases']] = {}
        if sheet == "VM Working":
            df = pd.read_excel(file, sheet)
            for index , row in df.iterrows():
                for key , val in row.to_dict().items():
                    for phase in phases:
                        if key == "BOM_Name":
                            let.append(row["BOM_Name"])
                        if "VM" in key and "Name" in key:
                            group.append(val)
                            result[phase][row["VM Name"] + " VM"] = {
                                "CPU":{
                                    "product_qty" : row["Core " + phase],
                                    "product_sku" : "CCVCVS0000000000"
                                },
                                "RAM":{
                                    "product_qty" : row["RAM " + phase],
                                    "product_sku" : "CCVRAT0000000000"
                                },
                                "Disk":{
                                    "product_qty" : row["DISK " + phase],
                                    "product_sku" : "STBT1P0000000000"
                                },
                                row["OS"]:{
                                    "product_qty" : row["OS "+ phase],
                                    "product_sku" : "STBT1P0000000000"
                                },
                                row["DB"]:{
                                    "product_qty" : row["DB "+ phase],
                                    "product_sku" : "STBT1P0000000000"
                                },
                                "qty" : row["VM " + phase]
                            
                            }
                            # result[phase][val]["qty"] = row["VM " + phase]
    # print(let)
    newRes = {}
    let = list(set(let))
    for _K , _V in result.items():
        for _P in let:
            newRes[_K +"_"+_P] = _V

    return newRes


def getPhases():
    phases = []
    for sheet in SheetNames:
        if sheet == "PhasesDetails":
            dfPhases = pd.read_excel(file, sheet)
            for index , row in dfPhases.iterrows():
                phases.append(row['Phases'])
    return phases
def merge_dicts(dict1, dict2):
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged




dict1 = getFromVmWorkingSheeet()
dict2 = getFromCommanSheets()

merged_dict = merge_dicts(dict1, dict2)

json_data = json.dumps(merged_dict , indent=4)
# fo = open("test.json","w+")
# fo.write(json_data)
