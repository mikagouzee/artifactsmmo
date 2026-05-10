from dataclasses import dataclass
from typing import List

@dataclass
class map_interaction_content: 
      type: str
      code: str

@dataclass
class map_access:
  type: str
  conditions: List[str]

@dataclass
class map_interactions:
  content: map_interaction_content
  transition: str


@dataclass
class world_map:
  map_id: int
  name: str
  skin: str
  x: int
  y: int
  layer: str
  access: map_access
  interactions: map_interactions
