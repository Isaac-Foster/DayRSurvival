from math import ceil
from statistics import median
from pprint import pprint

craft = {'banha': {'max': 3, 'min': 5}, "items":  {'toucinho cru': 1, 'sal': 1, 'agua limpa': 1}}

def q(item: dict, amount):
    name_item = list(item.keys())[0]
    make = item[name_item]
    amt = {k: ceil(amount / v) for k, v in make.items()}
    amounts = {x: [] for x, _ in amt.items()}

    for k, v in item["items"].items():
        for kk, vv in amt.items():
            amounts[kk].append((k, v * vv))

    med = median(amt[x] for x in amt)
    print(med)

    return {name_item: {x: dict(v) for x, v in amounts.items()}, "amount": amount}

pprint(q(craft, 3000))