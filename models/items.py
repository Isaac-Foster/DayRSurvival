from dataclasses import dataclass
from typing import Any
from enum import Enum

class Types(Enum):
  hunt = 'hunt'
  item = 'item'


@dataclass
class Item:
    name: str
    amount: int
    value: int
    type: Types