from .get_all_maps import get_all_maps
from helpers import closest_coordinates
from models import world_map

def get_closest_map(hero, content_type,content_code, layer="overworld", hide_blocked_maps=True):
  call = get_all_maps(layer, content_type,content_code, hide_blocked_maps)

  if call["total"] == 1:
    return world_map(**call["data"][0])
  
  start = (hero.x, hero.y)

  shortest = float('inf')
  destination = None
  for val in call["data"]:
    map = world_map(**val)
    crt = closest_coordinates(start, (map.x, map.y))
    if crt < shortest:
      destination = map
      shortest = crt

  return destination
    
