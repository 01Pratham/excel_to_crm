import pandas as pd
import openpyxl as xl
import json

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.xl_file = pd.ExcelFile(file_path)
        self.SheetNames = self.xl_file.sheet_names
        

    def get_phase_tenure(self, phase_name):
        df = pd.read_excel(self.file_path, sheet_name="PhasesDetails")
        for index, row in df.iterrows():
            if row["Phases"] == phase_name:
                return int(row['Tenure'])

    def getFromCommanSheets(self):
        phases = []
        result = {}
        for sheet in self.SheetNames:
            if sheet == "VM Working" or sheet == "product_mater":
                continue 
            if sheet == "PhasesDetails" : 
                dfPhases = pd.read_excel(self.file_path, sheet)
                for index , row in dfPhases.iterrows():
                    phases.append(row['Phases'])
                    for sheet2 in self.SheetNames:
                        if sheet2 == "PhasesDetails" or sheet2 == "VM Working" or sheet2 == "product_mater":
                            continue
                        result[row['Phases'] +"_"+ sheet2 ] = {}
            else:
                df = pd.read_excel(self.file_path, sheet)
                for index , row in df.iterrows():
                    for key , val in row.to_dict().items():
                        if key == "group":
                            for phase in phases:
                                if pd.isna(row["group"]):
                                    continue
                                result[phase +"_"+sheet][row["group"]] = {}
                        
        for sheet in self.SheetNames:
            if sheet == "VM Working" or sheet == "product_mater" or sheet == "PhasesDetails":
                continue 
            df = pd.read_excel(self.file_path, sheet)
            for index , row in df.iterrows():
                for phase in phases:
                    if not pd.isna(row["Product Name"]):
                        result[phase +"_"+sheet][row["group"]][row["Product Name"]] = {
                            "product_qty" : row[phase],
                            "product_sku" : "CCVRAT0000000000"
                        }
                
        return result


    def getFromVmWorkingSheeet(self):
        result = {}
        phases = []
        group = []
        let= {}

        for sheet in self.SheetNames:
            if sheet == "PhasesDetails":
                dfPhases = pd.read_excel(self.file_path, sheet)
                for index , row in dfPhases.iterrows():
                    phases.append(row['Phases'])
                    result[row['Phases']] = {}
            if sheet == "VM Working":
                df = pd.read_excel(self.file_path, sheet)
                for index , row in df.iterrows():
                    for key , val in row.to_dict().items():
                        for phase in phases:
                            if key == "BOM_Name":
                                let[row["BOM_Name"]] = []

        for sheet in self.SheetNames:
            if sheet == "PhasesDetails":
                dfPhases = pd.read_excel(self.file_path, sheet)
                for index , row in dfPhases.iterrows():
                    phases.append(row['Phases'])
                    result[row['Phases']] = {}
            if sheet == "VM Working":
                df = pd.read_excel(self.file_path, sheet)
                for index , row in df.iterrows():
                    for key , val in row.to_dict().items():
                        for phase in phases:
                            if "VM" in key and "Name" in key:
                                for l,p in let.items():
                                    if  row["BOM_Name"]== l:
                                        let[l].append(val + " VM")
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
        newRes = {}
        newLet = {}
        for _B, _P in let.items():
            newLet[_B] = list(set(_P))
        for _K, _V in result.items():
            for _B,_P in newLet.items():
                for _G , _v in _V.items():
                    if _G in newLet[_B]:
                        newRes[_K +"_" + _B] = {} 
        for _K, _V in result.items():
            for _B,_P in newLet.items():
                for _G , _v in _V.items():
                    if _G in newLet[_B]:
                        newRes[_K +"_" + _B][_G] = _v


        return newRes

    def merge_dicts(self,dict1, dict2):
        merged = dict1.copy()
        for key, value in dict2.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged


    def merged_dicts(self):
        dict1 = self.getFromVmWorkingSheeet()
        dict2 = self.getFromCommanSheets()

        merged_dict = self.merge_dicts(dict1, dict2)

        return merged_dict

    def getJsonData(self, var):
        json_data = json.dumps(var , indent=4)
        return json_data
    
    def getPhases(self):
        phases = []
        for sheet in self.SheetNames:
            if sheet == "PhasesDetails":
                dfPhases = pd.read_excel(self.file_path, sheet)
                for index , row in dfPhases.iterrows():
                    phases.append(row['Phases'])
        return phases