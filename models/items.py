from dataclasses import dataclass

@dataclass
class Item:
    name: str
    amount: int
    value: int