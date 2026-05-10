from api_client import api, CHAR_NAME

def gather():
  endpoint = f'/my/{CHAR_NAME}/action/gathering'
  return api.request('POST', endpoint)