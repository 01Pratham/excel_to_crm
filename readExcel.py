import pandas as pd

def readExcel(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        exit()
    result = []
    current_phase = None
    current_group = None
    current_phase_data = None
    current_group_data = None

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        phase = row['Phase_name']
        group = row['Group_name']
        group_qty = row['Group_qty']
        sku = row['Product_SKU']
        product = row['Product_Name']
        product_qty = row['Product_qty']

        if pd.notna(phase):
            if current_phase_data:
                result.append(current_phase_data)
            current_phase_data = {'Phase': phase, 'Groups': []}
            current_group_data = None
            current_phase = phase

        if pd.notna(group):
            if current_group_data:
                    current_phase_data['Groups'].append(current_group_data)
            current_group_data = {'Group': group, 'GroupQty' : group_qty,'Items': []}
            current_group = group

        if pd.notna(sku):
            current_items_data = {"SKU_Code": sku, 'Product': product, 'Quantity': product_qty}
            current_group_data['Items'].append(current_items_data)

    if current_phase_data:
        if current_group_data:
            current_phase_data['Groups'].append(current_group_data)
        result.append(current_phase_data)
    # return result
    print(result)


readExcel("template.xlsx")