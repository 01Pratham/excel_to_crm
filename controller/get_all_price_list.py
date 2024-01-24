import requests
def price_list(price_list_name):    
    url = "https://swayatta.esds.co.in:31199/production/pricing_list_master.php"

    payload = {}
    headers = {
    'Authorization': 'Basic Y3JtaWFwaWNsaWVudDo2QUc/eFIkczQ7UDkkPz8hSw=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    Res = response.json()
    
    price_lists = Res['result']['pricing_list']
    for dict in price_lists:
        if dict["pricing_list_name"] == price_list_name:
            return (dict)
    
    
# price_list("General Price List")

# def getProdID(product):
#     productList = price_list('General Price List')['products']  # Get the list