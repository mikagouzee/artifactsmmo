from api_client import api, CHAR_NAME

def rest():
  endpoint = f'/my/{CHAR_NAME}/action/rest'
  return api.request('POST', endpoint)