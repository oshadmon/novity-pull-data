from rest_code import execute_get, get_columns, publish_policy

CONN = "104.237.130.228:32049"

TABLE_MAPPING = {
    "wwp": {
        "wwp_analog": {
            # http://23.239.12.151:3100/d/ads1vwji3bvnkd/overview?orgId=1&refresh=5m
            "Influent Flow": {"column": "hw_influent", "unit": "gpm"},
            "Total Influent Flow - Today": {"column": "hw_influent_ttlzr_curday", "unit": "mgal"},
            "Total Influent Flow - Yesterday": {"column": "hw_influent_ttlzr_yesday", "unit": "mgal"},
            "UV Filter #1": {"column": "uv_signal1_ai", "unit": "% kill"},
            "UV Filter #2": {"column": "uv_signal2_ai", "unit": "% kill"},
            "Tank A": {"column": "am_ta_do_ai", "unit": "ppm"},
            "Tank B": {"column": "am_tb_do_ai", "unit": "ppm"},
            "Blower #1": {
                "column": "am_pdb1_status",
                "unit": "status",
                "mapping": {0: "IDLE", 1: "Running", 2: "Standby"}
            },
            "Blower #2": {
                "column": "am_pdb2_status",
                "unit": "status",
                "mapping": {0: "IDLE", 1: "Running", 2: "Standby"}
            },
            "Blower #3": {
                "column": "am_pdb3_status",
                "unit": "status",
                "mapping": {0: "IDLE", 1: "Running", 2: "Standby"}
            },
            "Blower #4": {
                "column": "am_pdb4_status",
                "unit": "status",
                "mapping": {0: "IDLE", 1: "Running", 2: "Standby"}
            },
            "Speed #1": {"column": "am_pdb1_feedback", "unit": "hz"},
            "Speed #2": {"column": "am_pdb2_feedback", "unit": "hz"},
            "Speed #3": {"column": "am_pdb3_feedback", "unit": "hz"},
            "Speed #4": {"column": "am_pdb4_feedback", "unit": "hz"}        }
    },
    "pp": {
        "pp_pm": {
            "Monitor": {
                "column": "monitor_id",
                "unit": "string",
            },
            "Real Power": {
                "column": "realpower",
                "unit": "MW"
            },
            "Reactive Power": {
                  "column": "reactivepower",
                  "unit": "kVAr",
                  "multiply": 0.1
              },
            "Power Factor": {
                "column": "powerfactor",
                "unit": "",
                "multiply": 0.1
              },
            "A-B Current": {
                  "column": "a_current",
                  "unit": "A"
              },
            "B-C Current": {
                  "column": "b_current",
                  "unit": "A"
              },
            "C-A Current": {
                "column": "c_current",
                "unit": "A"
            },
            "A-B Voltage": {
                "column": "a_n_voltage",
                "unit": "kV",
                "multiply": 0.01
            },
            "B-C Voltage": {
                "column": "b_n_voltage",
                "unit": "kV",
                "multiply": 0.01
            },
            "C-A Voltage": {
                "column": "c_n_voltage",
                "unit": "kV",
                "multiply": 0.01
            },
            "Frequency": {
                "column": "frequency",
                "unit": "Hz",
                "multiply": 0.01
            }
        }
    }
}

for code in TABLE_MAPPING:
    for table in TABLE_MAPPING[code]:
        plant_policy_id = execute_get(conn=CONN, command=f'blockchain get plant where code={code} bring [*][id]',
                                      is_query=False)

        for name in TABLE_MAPPING[code][table]:
            columns = get_columns(conn=CONN, table_name=table)
            column = TABLE_MAPPING[code][table][name]['column']
            new_policy = {
                "tag": {
                    "name": name,
                    "company": "Smart City",
                    "table": table,
                    "column": column,
                    "data type": columns[column],
                    "unit of measurement": TABLE_MAPPING[code][table][name]['unit'],
                    "plant": plant_policy_id
                }
            }
            if 'mapping' in TABLE_MAPPING[code][table][name]:
                new_policy['tag']['mapping'] = TABLE_MAPPING[code][table][name]['mapping']
            if 'multiply' in TABLE_MAPPING[code][table][name]:
                new_policy['tag']['multiply'] = TABLE_MAPPING[code][table][name]['multiply']

            output = execute_get(conn=CONN,
                                 command=f'blockchain get tag where name="{TABLE_MAPPING[code][table][name]}" and table={table} bring.count',
                                 is_query=False)
            if not output:
                publish_policy(conn=CONN, policy=new_policy)
