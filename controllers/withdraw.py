from api_client import api, CHAR_NAME

def withdraw(item_code, quantity=1):
  endpoint = f'/my/{CHAR_NAME}/action/bank/withdraw/item'
  payload = {'code':item_code, 'quantity':quantity}
  print(f"Withdrawing {quantity} {item_code} !")
  return api.request('POST', endpoint, payload)