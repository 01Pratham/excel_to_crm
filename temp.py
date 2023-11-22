import pandas as pd

file = "template.xlsx"

xl_file = pd.ExcelFile(file)

SheetNames = xl_file.sheet_names

for sheet in SheetNames:
    df = pd.read_excel(file, sheet)
    print (df)

