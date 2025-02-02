from rest_code import execute_get, publish_policy

CONN = "172.236.61.154:32349"

# http://23.239.12.151:3100/d/bdr5ti5cfz18gb/overview?orgId=1&refresh=5m&tab=transform
MONITOR_LIST = {
    "KPL": "Westar Interconnection",
    "BF1": "West Feeder",
    "BF2": "East Feeder",
    "BF3": "Center Feeder",
    "BF4": "Industrial Feeder",
    "BSP": "Station Power",

    "BCT": "Bus Tie 12470/12470",
    "CBT": "Bus Tie 12470/12470",

    "CF1": "Southeast Feeder",
    "CF2": "SAC Homes",
    "CF3": "North Feeder",
    "CSP": "Station Power",

    "CDT": "Bus Tie 12470/2400",
    "DCT": "Bus Tie 2400/12470",

    "DF1": "North Residence",
    "DF2": "North Main",
    "DF3": "Wenger West",
    "DF4": "South Main",
    "DSP": "Station Power"
}

plant_policy_id = execute_get(conn=CONN, command=f'blockchain get plant where code=pp bring [*][id]',
                              is_query=False)

for code in MONITOR_LIST:
    new_policy = {
        "monitoring": {
            "name": MONITOR_LIST[code],
            "code": code,
            "plant": plant_policy_id
        }
    }

    output = execute_get(conn=CONN,
                         command=f'blockchain get monitoring where code={code} bring.count', is_query=False)
    if not output:
        publish_policy(conn=CONN, policy=new_policy)

