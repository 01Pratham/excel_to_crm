import pandas as pd

file = "template.xlsx"

df = pd.read_excel(file, "BOM")

print (df)