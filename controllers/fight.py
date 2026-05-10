from api_client import api, CHAR_NAME
from models.fight import Fight

def fight():
  endpoint = f'/my/{CHAR_NAME}/action/fight'
  print(f"Hero starts a fight")
  res = api.request('POST', endpoint)
  return Fight(**res["data"])  #data["fight"]["result"]