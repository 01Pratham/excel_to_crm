import pandas as pd
import re

file = "template.xlsx"

xl_file = pd.ExcelFile(file)

SheetNames = xl_file.sheet_names
group = []
phase = []
item = []

for sheet in SheetNames:
    if sheet == "VM Working" or sheet == "product_mater" :
        continue 
    df = pd.read_excel(file, sheet) 
    # print(df)
    group.append({sheet : []})
    phase.append({sheet : []})
    for index, row in df.iterrows():
        print (row)
        if pd.notna(row['SKU']) and not pd.notna(row['Product Name']):
            group[-1][sheet].append(row['SKU'])
        else:
            item
            # continue
        keyList = list(row.keys())
        for key in keyList:
            if  key == "SKU" or  key == "Product Name":
                continue
    #         phase[-1][sheet].append(key)
    # phase[-1][sheet] = list(set(phase[-1][sheet]))
    


# print(phase)