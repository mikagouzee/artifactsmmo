from api_client import api, CHAR_NAME


def use_item(item_code, qtty=1):
  endpoint = f'/my/{CHAR_NAME}/action/fight'
  payload = {  "code": item_code, "quantity": qtty }
  res = api.request('POST', endpoint)
  

# {
#   "data": {
#     "cooldown": {
#       "total_seconds": 0,
#       "remaining_seconds": 0,
#       "started_at": "2019-08-24T14:15:22Z",
#       "expiration": "2019-08-24T14:15:22Z",
#       "reason": "movement"
#     },
#     "item": {
#       "name": "string",
#       "code": "string",
#       "level": 1,
#       "type": "string",
#       "subtype": "string",
#       "description": "string",
#       "conditions": [
#         {
#           "code": "string",
#           "operator": "eq",
#           "value": 0
#         }
#       ],
#       "effects": [
#         {
#           "code": "string",
#           "value": 0,
#           "description": "string"
#         }
#       ],
#       "craft": {
#         "skill": "weaponcrafting",
#         "level": 0,
#         "items": [
#           {
#             "code": "string",
#             "quantity": 1
#           }
#         ],
#         "quantity": 0
#       },
#       "tradeable": true
#     },
#     "character": {
#       "name": "string",
#       "account": "string",
#       "skin": "men1",
#       "level": 0,
#       "xp": 0,
#       "max_xp": 0,
#       "gold": 0,
#       "speed": 0,
#       "mining_level": 0,
#       "mining_xp": 0,
#       "mining_max_xp": 0,
#       "woodcutting_level": 0,
#       "woodcutting_xp": 0,
#       "woodcutting_max_xp": 0,
#       "fishing_level": 0,
#       "fishing_xp": 0,
#       "fishing_max_xp": 0,
#       "weaponcrafting_level": 0,
#       "weaponcrafting_xp": 0,
#       "weaponcrafting_max_xp": 0,
#       "gearcrafting_level": 0,
#       "gearcrafting_xp": 0,
#       "gearcrafting_max_xp": 0,
#       "jewelrycrafting_level": 0,
#       "jewelrycrafting_xp": 0,
#       "jewelrycrafting_max_xp": 0,
#       "cooking_level": 0,
#       "cooking_xp": 0,
#       "cooking_max_xp": 0,
#       "alchemy_level": 0,
#       "alchemy_xp": 0,
#       "alchemy_max_xp": 0,
#       "hp": 0,
#       "max_hp": 0,
#       "haste": 0,
#       "critical_strike": 0,
#       "wisdom": 0,
#       "prospecting": 0,
#       "initiative": 0,
#       "threat": 0,
#       "attack_fire": 0,
#       "attack_earth": 0,
#       "attack_water": 0,
#       "attack_air": 0,
#       "dmg": 0,
#       "dmg_fire": 0,
#       "dmg_earth": 0,
#       "dmg_water": 0,
#       "dmg_air": 0,
#       "res_fire": 0,
#       "res_earth": 0,
#       "res_water": 0,
#       "res_air": 0,
#       "effects": [
#         {
#           "code": "string",
#           "value": 0
#         }
#       ],
#       "x": 0,
#       "y": 0,
#       "layer": "interior",
#       "map_id": 0,
#       "cooldown": 0,
#       "cooldown_expiration": "2019-08-24T14:15:22Z",
#       "weapon_slot": "string",
#       "rune_slot": "string",
#       "shield_slot": "string",
#       "helmet_slot": "string",
#       "body_armor_slot": "string",
#       "leg_armor_slot": "string",
#       "boots_slot": "string",
#       "ring1_slot": "string",
#       "ring2_slot": "string",
#       "amulet_slot": "string",
#       "artifact1_slot": "string",
#       "artifact2_slot": "string",
#       "artifact3_slot": "string",
#       "utility1_slot": "string",
#       "utility1_slot_quantity": 0,
#       "utility2_slot": "string",
#       "utility2_slot_quantity": 0,
#       "bag_slot": "string",
#       "task": "string",
#       "task_type": "string",
#       "task_progress": 0,
#       "task_total": 0,
#       "inventory_max_items": 0,
#       "inventory": [
#         {
#           "slot": 0,
#           "code": "string",
#           "quantity": 0
#         }
#       ]
#     }
#   }
# }