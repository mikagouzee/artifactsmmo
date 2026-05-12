from pydantic import BaseModel, Field
from typing import List, Optional, Any

class BaseModelConfig(BaseModel):
    class Config:
        extra = "ignore" # Ignore les champs non définis dans la classe

# --- Sub-models ---
class InteractionContent(BaseModelConfig):
    type: str
    code: str

class Interaction(BaseModelConfig):
    content: Optional[InteractionContent] = None
    transition: Optional[Any] = None

class Drop(BaseModelConfig):
    code: str
    rate: int
    min_quantity: int
    max_quantity: int

class Effect(BaseModelConfig):
    code: str
    value: int
    description: str

class CraftItem(BaseModelConfig):
    code: str
    quantity: int

class Craft(BaseModelConfig):
    skill: str
    level: int
    items: List[CraftItem]
    quantity: int

# --- Main Models ---

class MapTile(BaseModelConfig):
    map_id: int # Si l'API renvoie map_id, sinon utilise x/y/layer
    name: str
    x: int
    y: int
    layer: str
    interactions: Optional[Interaction] = None

class Resource(BaseModelConfig):
    name: str
    code: str
    skill: str
    level: int
    drops: List[Drop]

class Item(BaseModelConfig):
    name: str
    code: str
    level: Optional[int] = None
    type: str
    subtype: Optional[str] = None
    description: Optional[str] = None
    effects: List[Effect] = []
    craft: Optional[Craft] = None
    tradeable: bool = True