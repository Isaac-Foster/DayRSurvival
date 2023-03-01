from pydantic.dataclasses import dataclass
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
    amount: int


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
            item.__dict__.pop("__initialised__")

            amount, value, type_item = cur.execute(
                f"SELECT amount, value, type FROM items WHERE name=?",
                [item.name]
            ).fetchone()

            item.value = ((item.amount // amount) * value)
            item.type = type_item
            calc = Calc_Item(**item.__dict__).__dict__
            calc.pop("__initialised__")
            values.append(calc)

        return {"items": values, "total": sum([x["value"] for x in values])}