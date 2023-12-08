from controller.tblDetails import DataProcessor
import json

obj = DataProcessor("template.xlsx")

mergedDict = obj.getFromVmWorkingSheeet()

with open("test.json", "w+") as fo:
    fo.write(json.dumps(mergedDict , indent=4))