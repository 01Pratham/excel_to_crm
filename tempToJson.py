import temp  
import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter


def getPhaseTenure(PhaseName):
    df = pd.read_excel("template.xlsx" , sheet_name= "PhasesDetails")
    for index, row in df.iterrows():
        if row["Phases"] == PhaseName:
            return int(row['Tenure'])
"""
wb = openpyxl.Workbook()
data = temp.merged_dict
sheet = wb.create_sheet(title= "Sheet")
"""


phaseList = []
groupList = {}
phaseTenure = {}
products = []

for phase , pVals in temp.merged_dict.items():
    phaseList.append(phase)
    groupList[phase] = []
    newP = phase.split("_")[0]
    if newP in temp.getPhases():
        phaseTenure[phase] = getPhaseTenure(newP)
    for groups , gVals in pVals.items():
        groupList[phase].append(groups)
        for items, iVals in gVals.items():
            products.append(items)

products = list(set(products))



tblHeaders = ["Phase Name", "Duration" , "Group Name", "Group Qty"]
tblHeaders += products




