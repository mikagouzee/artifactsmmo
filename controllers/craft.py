from api_client import api, CHAR_NAME

def craft(item_code, quantity=1):
  endpoint = f'/my/{CHAR_NAME}/action/crafting'
  payload = {'code':item_code, 'quantity':quantity}

  return api.request('POST', endpoint, payload)