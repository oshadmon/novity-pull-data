from blockchain_waste_water import plant_policy

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

TAGS = {
    "Monitor": {"column": "monitor_id"},
    "Real Power": {"column": "realpower"},
    "Reactive Power": {
        "column": "reactivepower",
        "multiply": 0.1
    },
    "Power Factor": {
        "column": "reactivefactor",
        "multiply": 0.1
    },
    "A-B Current": {"column" "a_current"},
    "B-C Current": {"column": "b_current"},
    "C-A Current": {"column": "c_current"},

    "A-B Voltage": {
        "column": "a_n_voltage",
        "multiply": 0.01
    },
    "B-C Voltage": {
        "column": "b_n_voltage",
        "multiply": 0.01
    },
    "C-A Voltage": {
        "column": "c_n_voltage",
        "multiply": 0.01
    },
    "Frequency": {
        "column": "frequency",
        "multiply": 0.01
    }
}


if __name__ == '__main__':
    plant_policy()