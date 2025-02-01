import json
import requests
from get_data import execute_get

# CONN = '45.79.18.179:32349'
CONN = '104.237.130.228:32149'
plants = {
    "waste water": {
        "code": "wwp",
        "address": "192nd Road, Sabetha, KS 66534",
        "loc": "39.914097, -95.793013"
    },
    "power plant": {
        "code": "pp",
        "address": "805 Main St, Sabetha, KS 66534",
        "loc": "39.902911, -95.800508"
    }

    # "water": {
    #     "code": "wp",
    #     "address": "66534, Sabetha, KS 66534",
    #     "loc": "39.907251, -95.898826"
    # }
}

table_mapping = {
    "wwp": {
        "wwp_analog": {
            # http://23.239.12.151:3100/d/ads1vwji3bvnkd/overview?orgId=1&refresh=5m
            "hw_influent": {"name": "Influent Flow", "unit": "gpm"},
            "hw_influent_ttlzr_curday": {"name": "Total Influent Flow - Today", "unit": "mgal"},
            "hw_influent_ttlzr_yesday": {"name": "Total Influent Flow - Yesterday", "unit": "mgal"},
            "uv_signal1_ai": {"name": "UV Filter #1", "unit": "% kill"},
            "uv_signal2_ai": {"name": "UV Filter #2", "unit": "% kill"},
            "am_ta_do_ai": {"name": "Tank A" , "unit": "ppm"},
            "am_tb_do_ai": {"name": "Tank B", "unit":  "ppm"},
            "am_pdb1_status": {
                "name": "Blower #1",
                "unit": "status",
                "mapping": {
                    0: "IDLE",
                    1: "Running",
                    2: "Standby"
                }
            },
            "am_pdb2_status": {
                "name": "Blower #2",
                "unit": "status",
                "mapping": {
                    0: "IDLE",
                    1: "Running",
                    2: "Standby"
                }
            },"am_pdb3_status": {
                "name": "Blower #3",
                "unit": "status",
                "mapping": {
                    0: "IDLE",
                    1: "Running",
                    2: "Standby"
                }
            },
            "am_pdb4_status": {
                "name": "Blower #4",
                "unit": "status",
                "mapping": {
                    0: "IDLE",
                    1: "Running",
                    2: "Standby"
                }
            },
            "am_pdb1_feedback": {"name": "Speed #1", "unit": "hz"},
            "am_pdb2_feedback": {"name": "Speed #2", "unit": "hz"},
            "am_pdb3_feedback": {"name": "Speed #3", "unit": "hz"},
            "am_pdb4_feedback": {"name": "Speed #4", "unit": "hz"},

        }
    }
}


def publish_policy(policy:dict):
    ledger_conn = '104.237.130.228:32048'
    new_policy = f"<new_policy={json.dumps(policy)}>"
    headers = {
        'command': 'blockchain insert where policy=!new_policy and local=true and master=!ledger_conn',
        'User-Agent': 'AnyLog/1.23',
        'destination': ledger_conn
    }

    try:
        r = requests.post(url=f"http://{CONN}", headers=headers, data=new_policy)
    except Exception as error:
        raise Exception(f"Failed to POST data against {CONN} (Error: {error})")
    else:
        if not 200 <= int(r.status_code) < 300:
            raise ConnectionError(f"Failed to POST data against {CONN} (Error: {r.status_code})")


def get_columns(table_name:str):
    """
    Extract list of columns for each table
    """
    cmd = f"get columns where dbms=cos and table={table_name} and format=json"
    output = execute_get(conn='45.79.18.179:32349', command=cmd, is_query=False)

    # remove columns associated with AnnyLog data management
    for column in ['row_id', 'insert_timestamp', 'tsd_name', 'tsd_id']:
        del output[column]
    return output


def plant_policy():
    """
    Publish plant policy to blockchain
    """
    new_policy = {
        "plant": {
            "name": None,
            "company": "Smart City",
            "code": None,
            "address": None,
            "loc": None
        }
    }

    for plant in plants:
        new_policy['plant']['name'] = plant
        for key in plants[plant]:
            new_policy['plant'][key] = plants[plant][key]
        # check if policy exists
        output = execute_get(conn=CONN, command=f'blockchain get plant where name="{plant}" bring.count', is_query=False)
        if not output:
            publish_policy(policy=new_policy)

def mapping_policy():
    for code in table_mapping:
        for table in table_mapping[code]:
            plant_policy_id = execute_get(conn=CONN, command=f'blockchain get plant where code={code} bring [*][id]', is_query=False)
            columns = get_columns(table_name=table)
            for column in table_mapping[code][table]:
                new_policy = {
                    "tag": {
                        "name": table_mapping[code][table][column]['name'],
                        "company": "Smart City",
                        "table": table,
                        "column": column,
                        "data type": columns[column],
                        "unit of measurement": table_mapping[code][table][column]['unit'],
                        "plant": plant_policy_id
                    }
                }
                if 'mapping' in table_mapping[code][table][column]:
                    new_policy['tag']['mapping'] = table_mapping[code][table][column]['mapping']

                output = execute_get(conn=CONN, command=f'blockchain get tag where name="{table_mapping[code][table][column]}" and table={table} bring.count', is_query=False)
                if not output:
                    publish_policy(new_policy)



if __name__ == '__main__':
    plant_policy()
    mapping_policy()

