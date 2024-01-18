import controller.get_product_info as prod
import controller.get_all_price_list as Plist

import pandas as pd

# prod.get_product_info()

file = "static/template.xlsx"
# def get_sku_from_excel(file = "static/template.xlsx"):
core_product_id = []
core_product_name = []
skucode = []
price = []
is_active = []
price_list = []
df = pd.read_excel(file, sheet_name="product_mater")
for index, row in df.iterrows():
    for key , val in row.to_dict().items():
        if "Unnamed" in key:
            continue
        if "price_list" in key:
            price_list.append(val)
            Pid = Plist.price_list(val)['pricing_list_id']
        if "skucode" in key:
            skucode.append(val)
            sku = val
        if "core_product_id" in key:
            core_product_id.append(prod.get_product_info(Pid,sku)['product_id'])
        if "core_product_name" in key:
            core_product_name.append(val)
        if "price" in key:
            price.append(val)
        if "is_active" in key:
            is_active.append(val)

    
    
l = list(zip(core_product_id, core_product_name, skucode, price, is_active, price_list))
        
        
print(l)