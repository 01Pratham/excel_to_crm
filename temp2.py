import pandas as pd
from pprint import pprint
import re
import json
import openpyxl as xl


file = "template.xlsx"
xl_file = pd.ExcelFile(file)
SheetNames = xl_file.sheet_names
result = {}
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
                result[row['Phases'] +" "+ sheet2 ] = {}
    else:
        df = pd.read_excel(file, sheet)
        for index , row in df.iterrows():
            for key , val in row.to_dict().items():
                if key == "group":
                    for phase in phases:
                        if pd.isna(row["group"]):
                             continue
                        result[phase +" "+sheet][row["group"]] = {}
                
for sheet in SheetNames:
    if sheet == "VM Working" or sheet == "product_mater" or sheet == "PhasesDetails":
        continue 
    df = pd.read_excel(file, sheet)
    for index , row in df.iterrows():
        for phase in phases:
            if not pd.isna(row["Product Name"]):
                result[phase +" "+sheet][row["group"]][row["Product Name"]] = {
                    "product_qty" : row[phase],
                    "product_sku" : "CCVRAT0000000000"
                }
                

fo = open("test.json", "w+")
fo.write(json.dumps(result , indent=4))
fo.close()

