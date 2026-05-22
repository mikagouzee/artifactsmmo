def is_equipped(hero, item):
  code = item["code"]
  match item["subtype"]:
    case "utility":
      return hero.utility_slot_1 == code or hero.utility_slot_2 == code
    case "leg_armor":
      return hero.leg_armor_slot == code
    case "boots":
      return hero.boots == code
    case "weapon":
      return hero.weapon_slot == code
    case "shield": 
      return hero.shield_slot == code
    case "helmet":
      return hero.helmet_slot == code
    case "ring":
      return hero.ring1_slot == code or hero.ring2_slot == code
    case "amulet":
      return hero.amulet_slot == code