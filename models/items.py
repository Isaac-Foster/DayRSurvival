from dataclasses import dataclass
from pydantic import BaseModel
from database import cur


@dataclass
class Item:
    name: str
    amount: int
    value: int


@dataclass
class ItemDB(Item):
    type: str


@dataclass
class CItem:
    name: str
    amount: str
    type: str


@dataclass
class Calc_Item(ItemDB):
    ...


@dataclass
class Items:
    items: list

    def __post_init__(self):
        self.items = [CItem(**x) for x in self.items]


    def sum(self):
        values = []
        
        for item in self.items:

            colum = str(item.type) + "s"
            
            amount, value = cur.execute(
                f"SELECT amount, value FROM {colum} WHERE name=?",
                [item.name]
            ).fetchone()

            item.value = ((item.amount // amount) * value)

            values.append(Calc_Item(**item.__dict__).__dict__)

        return {"items": values, "total": sum([x["value"] for x in values])}