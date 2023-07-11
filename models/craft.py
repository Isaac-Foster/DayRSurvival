from dataclasses import dataclass
from math import ceil


from models.items import Name, CalItem
from mongo import find_one


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
            data = find_one(collection="crafts", data=dict(name=item.name))
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

