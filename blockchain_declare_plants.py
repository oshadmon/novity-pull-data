# script to declare plants and corresponding
from rest_code import *

CONN = "104.237.130.228:32049"

PLANTS = {
    "waste water": {
        "code": "wwp",
        "address": "192nd Road, Sabetha, KS 66534",
        "loc": "39.914097, -95.793013"
    },
    "power plant": {
        "code": "pp",
        "address": "805 Main St, Sabetha, KS 66534",
        "loc": "39.902911, -95.800508"
    },
    "water plant": {
        "code": "wp",
        "address": "66534, Sabetha, KS 66534",
        "loc": "39.907251, -95.898826"
    }
}


new_policy = {
    "plant": {
        "name": None,
        "company": "Smart City",
        "code": None,
        "address": None,
        "loc": None,
        "dbms": "cos",
    }
}

for plant in PLANTS:
    new_policy['plant']['name'] = plant
    for key in PLANTS[plant]:
        new_policy['plant'][key] = PLANTS[plant][key]
    # check if policy exists
    output = execute_get(conn=CONN, command=f'blockchain get plant where name="{plant}" bring.count',
                         is_query=False)
    if not output:
        publish_policy(conn=CONN, policy=new_policy)
