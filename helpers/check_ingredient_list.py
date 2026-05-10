from helpers import find_in_bag


def check_ingredient_list(bag, craft):
  for ingredient in craft["items"]:
    hold_qty = find_in_bag(bag, ingredient["code"])
    if  hold_qty < ingredient["quantity"]:
      print(f"Missing {ingredient["quantity"] - hold_qty} {ingredient["code"]} ! Can't proceed with craft")
      return False
  return True  
