from api_client import api, CHAR_NAME

def move(x, y):
  endpoint = f'/my/{CHAR_NAME}/action/move'
  payload = {'x':x, 'y':y}
  print(f"Moving to x {x} - y {y}")
  return api.request('POST', endpoint, payload)