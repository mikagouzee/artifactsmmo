from api_client import api, CHAR_NAME
from models.hero import hero

def get_char():
  endpoint = f'/my/characters'
  res = api.request('GET', endpoint)
  # print(res["data"][0])
  # print(type(res))
  # print(type(res["data"]))
  my_hero = hero(**res["data"][0])
  return my_hero
  
