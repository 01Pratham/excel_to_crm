import requests
import json

def get_product_info(pricing_list_id = 1 , product_sku_code = "CCSTNKBTI000000"):
    url = "https://swayatta.esds.co.in:31199/production/configurator_pricing_list_api_rest.php"

    payload = json.dumps({
    "pricing_list_id": pricing_list_id,
    "product_sku_code": product_sku_code
    })
    headers = {
    'Authorization': 'Basic Y3JtaWFwaWNsaWVudDo2QUc/eFIkczQ7UDkkPz8hSw==',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    Res = response.json()
    if Res['result']["pricing_data"] == []:
        return {
            "product_id": '',
                "product_name": '',
                "product_description": '',
                "product_sku_code": '',
                "product_sku_code_id": '',
                "product_is_grouped": '',
                "product_group_product_ids": '',
                "product_is_discountable": '',
                "pricing_level_id": '',
                "pricing_level_name": '',
                "pricing_list_id": '',
                "selling_price": '',
                "selling_currency_id": '',
                "selling_currency": '',
                "recurring_selling_price": '',
                "recurring_selling_currency_id": '',
                "recurring_selling_currency": '',
                "expiry_date": '',
                "is_approved": '',
                "forecasted_onetime_price": '',
                "forecasted_recurring_price": '',
                "forecasted_tenure_months": '',
                "is_active": '',
                "is_deleted": '',
        }
    else : 
        product_info = Res['result']["pricing_data"][-1]
        return product_info

# get_product_info()