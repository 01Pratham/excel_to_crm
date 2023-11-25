import pandas as pd
from pprint import pprint
import re

file = "template.xlsx"

xl_file = pd.ExcelFile(file)

SheetNames = xl_file.sheet_names
result = []

for sheet in SheetNames:
    if sheet == "VM Working" or sheet == "product_mater" :
        continue 
    df = pd.read_excel(file, sheet)
    for index , row in df.iterrows():
        keyList = list(row.keys())
        for key in keyList:
            if  key == "SKU" or  key == "Product Name":
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
    if sheet == "VM Working" or sheet == "product_mater" :
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
    if sheet == "VM Working" or sheet == "product_mater" :
        continue 
    df = pd.read_excel(file, sheet)
    for index , row in df.iterrows():
        for phase in unique_phase_keys:
            phase_id = phase.replace(" "+sheet, '')
            for i,val in enumerate(unique_list):
                if not pd.isna(row["Product Name"]):
                    for group in unique_group_keys:

                        try:
                            for j,gVal in enumerate(unique_list[i][key]):
                                # print(phase_id)

                                try:
                                    unique_list[i][phase_id + " " + sheet][j][group].append({
                                        "product_name" : row["Product Name"],
                                        "product_sku" : row["SKU"],
                                        "product_qty" : row[phase_id]
                                    })
                                    # newP.append({phase_id:row[phase_id]})
                                except KeyError:
                                    continue
                        except KeyError:
                            continue

                # if not pd.isna(row["Product Name"]):



print(unique_list)



