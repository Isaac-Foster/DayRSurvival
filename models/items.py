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
        item.type = type_item
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
class Items:
    items: list[CalItem] | list[Item]

    def sum(self):
        values = get_values(self)

        return {"items": values, "total": sum([x["value"] for x in values])}


@dataclass
class DropAmount:
    fixed: int = 0
    min: int = 0
    max: int = 0


@dataclass
class Cost:
    fixed: list[CalItem]
    min: list[CalItem]
    max: list[CalItem]


@dataclass
class Craft(Name):
    drop: DropAmount
    resources: list[CalItem]

    def __post_init__(self):
        if isinstance(self.drop, dict):
            self.drop = DropAmount(**self.drop) 
        
        if isinstance(self.resources[0], dict):
            self.resources = [CalItem(**x) for x in self.resources]


    def __to_dict__(self):
        self.drop = self.drop.__dict__
        self.resources = [x.__dict__  for x in self.resources]
        return self.__dict__


@dataclass
class CraftCal:
    crafts: list[CalItem]

    def cost_items(self):
        crafts = []

        for item in self.crafts:
            data = collect.find_one(dict(name=item.name))
            data.pop("_id")
            craft = Craft(**data)
            resources = craft.resources
            cost = dict(fixed=[], min=[], max=[])

            for resource in resources:
                
                if craft.drop.fixed:
                    resource.amount *= item.amount
                    cost["fixed"].append(
                        CalItem(resource.name, resource.amount)
                    )
                else:
                    mn = ceil(item.amount / craft.drop.max)
                    mx = ceil(item.amount / craft.drop.min)
                    cost["min"].append(
                        CalItem(resource.name, mn)
                    )

                    cost["max"].append(
                        CalItem(resource.name, mx)
                    )
            cost = {k:v for k,v in cost.items() if v}
            craft.drop = {k: v for k, v in craft.drop.__dict__.items() if v}
            craft.resources = cost

            crafts.append(craft)
        self.crafts = crafts