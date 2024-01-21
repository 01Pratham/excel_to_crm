import pandas as pd
# import openpyxl as xl
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

    def getFromCommanSheets(self, type = ""):
        phases = []
        result = {}
        PhaseData = {}
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
                        PhaseData[row['Phases'] +"_"+ sheet2 ] = []
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
                        PhaseData[phase +"_"+sheet].append(row["group"])
                        result[phase +"_"+sheet][row["group"]][row["Product Name"]] = {
                            "product_qty" : row[phase],
                            "discount" : row["Discount Percent"] if not pd.isna(row["Discount Percent"]) else 0
                        }
                
        if type == "":
            return result
        else:
            return PhaseData


    def getFromVmWorkingSheeet(self , type = ""):
        result = {}
        phases = []
        group = []
        let= {}

        PhaseData = {}

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
                                    "vCPU static Cloud - Compute":{
                                        "product_qty" : row["Core " + phase],
                                        "discount" : self.read_product_master("vCPU Static Cloud- Compute")
                                    },
                                    "vRAM static Cloud- Compute":{
                                        "product_qty" : row["RAM " + phase],
                                        "discount" : self.read_product_master("vRAM Static- Compute")
                                    },
                                    "Block Storage - 1 IOPS / GB":{
                                        "product_qty" : row["DISK " + phase],
                                        "discount" : self.read_product_master("Block Storage - 1 IOPS / GB")
                                    },
                                    row["OS"]:{
                                        "product_qty" : row["OS "+ phase],
                                        "discount" : self.read_product_master(row["OS"])
                                    },
                                    "qty" : row["VM " + phase]
                                }
                                
                                if row["DB"] != "Select DB" : 
                                    result[phase][row["VM Name"] + " VM"][row["DB"]]= {
                                        "product_qty" : row["DB "+ phase],
                                        "discount" : self.read_product_master(row["DB"])
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
                        PhaseData[_K +"_" + _B] = []
        for _K, _V in result.items():
            for _B,_P in newLet.items():
                for _G , _v in _V.items():
                    if _G in newLet[_B]:
                        newRes[_K +"_" + _B][_G] = _v
                        PhaseData[_K +"_" + _B].append(_G)

        if type == '':
            return newRes
        else:
            return PhaseData

    def merge_dicts(self,dict1, dict2):
        merged = dict1.copy()
        for key, value in dict2.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged


    def merged_dicts(self ):
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
    
    def read_product_master(self, prod):
        for sheet in self.SheetNames:
            if sheet == "product_mater":
                productMasterDf = pd.read_excel(self.file_path, sheet)
                for index , row in productMasterDf.iterrows():
                    if prod == row['VM Related Products'] :
                        return row['Discount Percent']
                    else : 
                        return 0
     
    def GetPhasesGroups(self):
        dict1 = self.getFromVmWorkingSheeet("GetPhasesGroups")
        dict2 = self.getFromCommanSheets("GetPhasesGroups")
        data = {} 
        for key , groups in dict1.items():
            dict2[key] = list(set(dict2[key]))
            data[key] = dict1.get(key, []) + dict2.get(key, [])
        # # data = self.merged_dicts("GetPhasesGroups")
        return data