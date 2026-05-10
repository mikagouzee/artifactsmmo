from api_client import api, CHAR_NAME

def deposit(item_code, quantity=1):
  if(quantity < 1):
    raise Exception(f"deposit value cannot be lower than 1 : {quantity}")
  
  endpoint = f'/my/{CHAR_NAME}/action/bank/deposit/item'

  payload = [{'code':item_code, 'quantity':quantity}]

  print(f"Deposing {quantity} {item_code} !")
  return api.request('POST', endpoint, payload)