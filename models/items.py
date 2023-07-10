from pydantic.dataclasses import dataclass
from database import cur, commit


def get_values(self):
    values = []
    for item in self.items:
        amount, value, type_item = cur.execute(
                f"SELECT amount, value, type FROM items WHERE name LIKE ?",
                [item.name]
            ).fetchone()

        item.value = ((item.amount // amount) * value)
        item.type = type_item
        values.append(item)
    return values


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
    items: list[CalItem] | list[Item]

    def sum(self):
        values = get_values(self)

        return {"items": values, "total": sum([x["value"] for x in values])}


@dataclass
class Craft:
    crafts: list[CalItem]

    def make_items(self):
        for item in self.crafts:
            print(item, type(item))