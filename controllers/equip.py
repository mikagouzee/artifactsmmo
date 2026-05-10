from api_client import api, CHAR_NAME

def equip(item_code, slot="weapon", qtty=1):
  endpoint = f'/my/{CHAR_NAME}/action/equip'

  payload = {
    'code':item_code,
    'slot':slot,
    'quantity':qtty}

  print(f"Equiping {qtty} {item_code} as {slot} !")
  return api.request('POST', endpoint, payload)