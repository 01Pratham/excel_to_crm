import pandas as pd

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
    group.append({sheet : []})
    for index, row in df.iterrows():
        if pd.notna(row['SKU']) and not pd.notna(row['Product Name']):
            # group[sheet].append(row['SKU'])
            print(type(group[1][sheet]))
            continue
        # print(row)

print(group)
