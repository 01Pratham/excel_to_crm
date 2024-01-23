import controller.get_product_info as prod
import controller.get_all_price_list as Plist
import pandas as pd
import controller.exportExcel as e

# prod.get_product_info()

file = "static/Temp2.xlsx"
# def get_sku_from_excel(file = "static/template.xlsx"):

print(e.exportExcel(file))