from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Optional, List


class MapContent(BaseModel):
    type:str
    code:str

class MapTile(Document):
    map_id: Indexed(int, unique=True)
    name: str
    x: int
    y: int
    layer: str
    content: Optional[MapContent] = None
    blocked: bool = False

    class Settings:
        name = "world_map" # Nom de la collection dans Mongo
        indexes = [
            [("x", 1), ("y", 1), ("layer", 1)]
        ]