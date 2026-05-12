def find_in_bag(bag, item_code):
  return next((x["quantity"] for x in bag if x["code"] == item_code), 0)

def check_bag_weight(bag):
  return sum((x["quantity"] for x in bag))

