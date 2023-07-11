from dataclasses import dataclass, Field
from math import ceil

from database import cur, commit
from mongo import connect

collect = connect.database.crafts


def get_values(self):
    values = []
    for item in self.items:
        amount, value, type_item = cur.execute(
                f"SELECT amount, value, type FROM items WHERE name LIKE ?",
                [item.name]
            ).fetchone()

        item.value = ((item.amount // amount) * value)

        item = CItem(**item.__dict__)

        values.append(item)
    return values


@dataclass
class Name:
    name: str


@dataclass
class Item(Name):
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
class CalItem(Name):
    amount: int


@dataclass
class CItem(CalItem):
    value: int


@dataclass
class Items:
    items: list[CalItem] | list[Item]

    def sum(self):
        values = get_values(self)
        return {"items": values, "total": sum([x.value for x in values])}