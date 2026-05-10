from models import hero


def check_skill_level(my_hero:hero, craft):
  skillname = craft["skill"]
  skillname+="_level"
  skill = getattr(my_hero, skillname)
  if skill >= craft["level"]:
    return True
  
  return False