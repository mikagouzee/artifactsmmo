from helpers import check_ingredient_list, check_skill_level


def can_craft(context, craft):
  return check_skill_level(context.current_hero, craft) and check_ingredient_list(context.current_hero.inventory, craft)
