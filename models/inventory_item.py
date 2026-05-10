from dataclasses import dataclass

@dataclass
class inventory_item:
    slot: int
    code: str
    quantity: int
      