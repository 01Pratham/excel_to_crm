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
            for i,val in enumerate(unique_list):
                for group in unique_group_keys:
                    if row["SKU"] == group and pd.isna(row["Product Name"]):
                        continue
                    try:
                        for j,gVal in enumerate(unique_list[i][phase]):
                            phase_id = phase.replace(" "+sheet, '')
                            try:
                                unique_list[i][phase][j][group].append({
                                    "product_name" : row["Product Name"],
                                    "product_sku" : row["SKU"],
                                    "product_qty" : row[phase_id]
                                })
                            except KeyError:
                                continue
                    except KeyError:
                        continue
                   
                # if not pd.isna(row["Product Name"]):




# print(unique_list)

a = open("test.txt","w+")
a.write(str(unique_list))

a.close()
