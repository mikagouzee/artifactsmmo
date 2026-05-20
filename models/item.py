from dataclasses import dataclass
from typing import List

from models.recipe import recipe

  
@dataclass
class item_condition:
  code: str
  #operator: eq
  value: int

@dataclass
class item_effect:
  code: str
  value: int
  description: str

@dataclass
class item:
    _id:int
    name: str
    code: str
    level: int
    type: str
    subtype: str
    description: str
    conditions: List[item_condition]
    effects: List[item_effect]
    craft: recipe
    tradeable: bool
