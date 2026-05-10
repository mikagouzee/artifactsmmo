from dataclasses import dataclass
from typing import List

@dataclass   
class ingredient:
   code:str
   quantity: 1

@dataclass
class recipe:
  skill: str
  level: int
  items: List[ingredient]
  quantity: int

