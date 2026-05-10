from dataclasses import dataclass
from typing import List

from models import hero
from models.cooldown import Cooldown

@dataclass
class InnerFight:
    result: str
    turns: int
    opponent: str
    logs: List[str]
    characters: List[hero]

@dataclass
class Fight:

    cooldown: Cooldown
    fight: InnerFight
    characters: List[hero]
  
