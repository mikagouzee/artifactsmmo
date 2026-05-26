class Bag:
  def __init__(self, source=None):
    self._items = dict[str,int]={}
    if source is not None:
      self._load(source)
      
  def _load(self, source):
    if isinstance(source, Bag):
      self._items = dict(source._items)
    elif isinstance(source, dict):
      self._items = {k: v for k, v in source.items() if v > 0}
    elif isinstance(source, list):
      for entry in source:
        code = entry["code"]
        qty = entry.get("quantity", 0)
        if qty > 0:
          self.items["code"] = self._items.get(code, 0) + qty
          
    else:
      raise TypeError(f"Bag : unsupported source type {type(source)}")
    
  # ------------------------------------------------------------------ #
  #  Queries                                                             #
  # ------------------------------------------------------------------ #

  def get(self, item_code: str) -> int:
      return self._items.get(item_code, 0)

  def weight(self) -> int:
      """Nombre total d'items (toutes quantités sommées)."""
      return sum(self._items.values())

  def max_craftable(self, item: dict) -> int:
      """Combien de fois on peut crafter cet item avec le contenu du bag."""
      recipe = item.get("craft", {})
      required_items = recipe.get("items", [])
      craft_quantity = recipe.get("quantity", 1)

      if not required_items:
          return 0

      craftable = float("inf")
      for ingredient in required_items:
          code = ingredient.get("code")
          needed = ingredient.get("quantity", 0)
          if needed <= 0:
              continue
          craftable = min(craftable, self.get(code) // needed)

      if craftable <= 0 or craftable == float("inf"):
          return 0
      return craftable * craft_quantity

  def has_ingredients(self, craft: dict) -> bool:
      """Vérifie que le bag contient tous les ingrédients pour un craft."""
      for ingredient in craft.get("items", []):
          if self.get(ingredient["code"]) < ingredient["quantity"]:
              print(f"Missing {ingredient['quantity'] - self.get(ingredient['code'])} "
                    f"{ingredient['code']} — can't craft")
              return False
      return True

  # ------------------------------------------------------------------ #
  #  Mutations                                                           #
  # ------------------------------------------------------------------ #

  def add(self, item_code: str, quantity: int):
      self._items[item_code] = self._items.get(item_code, 0) + quantity

  def merge(self, other) -> "Bag":
      """Retourne un nouveau Bag = self + other (sans modifier self)."""
      result = Bag(self)
      for code, qty in Bag(other)._items.items():
          result.add(code, qty)
      return result

  # ------------------------------------------------------------------ #
  #  Serialisation                                                       #
  # ------------------------------------------------------------------ #

  def to_list(self) -> list:
      """Format API : [{"code": ..., "quantity": ...}]"""
      return [{"code": k, "quantity": v} for k, v in self._items.items()]

  def to_dict(self) -> dict:
      return dict(self._items)

  def __repr__(self):
        return f"Bag({self._items})"
