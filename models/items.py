from dataclasses import dataclass, field
from database import cur, commit

from typing import Optional

@dataclass
class Item:
    name: str
    amount: int | None = None
    value: int | None = None
    type: str | None = None

    def insert(self):
        cur.execute(
            "INSERT OR IGNORE INTO items(name, amount, value, type)"
            " VALUES(?, ?, ?, ?)",
            (self.name.strip(), self.amount, self.value, self.type)
        )
        commit()


@dataclass
class CalItem:
    name: str
    amount: int


@dataclass
class Items:
    items: list

    def __post_init__(self):
        self.items = [Item(**x) for x in self.items]


    def sum(self):
        values = []
        #print(self.items)
        for item in self.items:
            amount, value, type_item = cur.execute(
                    f"SELECT amount, value, type FROM items WHERE name LIKE ?",
                    [item.name]
                ).fetchone()

            item.value = ((item.amount // amount) * value)
            item.type = type_item
            values.append(item.__dict__)

        return {"items": values, "total": sum([x["value"] for x in values])}