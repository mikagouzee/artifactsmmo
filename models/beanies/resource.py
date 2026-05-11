from beanie import Document, Indexed
from typing import List

from pydantic import BaseModel

class ResourceDrop(BaseModel):
    code: str
    rate: int

class Resource(Document):
    name: str
    code: Indexed(str, unique=True)
    skill: Indexed(str)
    level: int
    drops: List[ResourceDrop]

    class Settings:
        name = "resources"