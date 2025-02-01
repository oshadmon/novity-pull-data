# Pulling Smart City Data

The following provides a sample script to pull data from our smart city demo. 

[blockchain_tagging.py](blockchain_waste_water.py) - Generate a list of tags (one per column) for `wwp_analog` data

[blockchain_get_data.py](blockchain_get_data.py) - Using information from tags, execute `increment` and `period` 
queries. The code also generates a file called `blockchain.metadata.json` which contains a list of tags extracted from
the blockchain. 

```shell
python3 blockchain_get_data.py --help
<<COMMENT
usage: blockchain_get_data.py [-h] [--conn CONN] [--plant-code {wwp}] [--timestamp-column TIMESTAMP_COLUMN] [--increments-interval {minute,hour,day}]
                              [--increments-interval-value INCREMENTS_INTERVAL_VALUE] [--where-interval {minute,hour,day}] [--where-interval-value WHERE_INTERVAL_VALUE] [--all-data [ALL_DATA]]
                              [--summary-data [SUMMARY_DATA]]

optional arguments:
    -h, --help                                                  show this help message and exit
    --conn                          CONN                        REST connection
    --plant-code                    PLANT_CODE                  plant code
    --increments-interval           INCREMENTS_INTERVAL         increment time interval
    --increments-interval-value     INCREMENTS_INTERVAL_VALUE   increment time interval value
    --where-interval                WHERE_INTERVAL              where increment time interval in WHERE condition
    --where-interval-value          WHERE_INTERVAL_VALUE        increment time interval used in WHERE condition
    --all-data                      [ALL_DATA]                  Get all data
    --summary-data                  [SUMMARY_DATA]              Get summary of data
<<

python3 blockchain_get_data.py \
  --conn 45.79.18.179:32349 \
  --plant-code wwp \
  --timestamp-column timestamp \
  --increments-interval minute \
  --increments-interval-value 10 \
  --where-interval day \
  --where-interval-value 1 \
  --all-data \
  --summary-data
```

The select columns for tags is based <a href="http://23.239.12.151:3100/d/ads1vwji3bvnkd/overview?orgId=1&refresh=5m" targer="_blanl">Waste Water Dashboard</a>

[get_data.py](get_data.py) - Given a list of tables (_water_ and _waste water_), generate a list of corresponding columns,,
and get raw data, as well as summary data for the last 24 hours. The data is then stored into corresponding files. 

[read_json.py](read_json.py) - Example for reading data from JSON file. Used to validate write is correct.


## JSON files
[blockchain.metadata.json](blockchain.metadata.json) - Blockchain data for tags

[wwp_analog.increments.json](wwp_analog.increments.json) - summary of data over last hour in 10 minute intervals 

[wwp_analog.raw.json](wwp_analog.raw.json) - raw data over last hour 

## Comments
**What is period**: The period function finds the first occurrence of data before or at a specified date and considers 
the readings in a period of time which is measured by the type of the time interval. 

```json
[
	{"timestamp": "2025-01-24 01:55:50.161299", "Influent Flow": "139.775", "Total Influent Flow - Today": "0.16999722", "Total Influent Flow - Yesterday": "0.22298019", "UV Filter #1": -57, "UV Filter #2": 16, "Tank A": "0.69", "Tank B": "6.18", "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Running", "Speed #1": 0, "Speed #2": 0, "Speed #3": 60, "Speed #4": 24},
	{"timestamp": "2025-01-24 01:56:20.285080", "Influent Flow": "149.75833", "Total Influent Flow - Today": "0.17007045", "Total Influent Flow - Yesterday": "0.22298019", "UV Filter #1": -57, "UV Filter #2": 16, "Tank A": "0.7", "Tank B": "6.2", "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Running", "Speed #1": 0, "Speed #2": 0, "Speed #3": 60, "Speed #4": 24},
	{"timestamp": "2025-01-24 01:56:50.408106", "Influent Flow": "157.745", "Total Influent Flow - Today": "0.17014368", "Total Influent Flow - Yesterday": "0.22298019", "UV Filter #1": -57, "UV Filter #2": 16, "Tank A": "0.7", "Tank B": "6.19", "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Running", "Speed #1": 0, "Speed #2": 0, "Speed #3": 60, "Speed #4": 24},
	{"timestamp": "2025-01-24 01:57:20.533670", "Influent Flow": "163.735", "Total Influent Flow - Today": "0.1702254", "Total Influent Flow - Yesterday": "0.22298019", "UV Filter #1": -57, "UV Filter #2": 16, "Tank A": "0.7", "Tank B": "6.24", "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Running", "Speed #1": 0, "Speed #2": 0, "Speed #3": 60, "Speed #4": 24}
]
```

**What is increments**: The increments functions considers data in increments of time (i.e. every 5 minutes) within a 
time range
```json
[
	{"Min Timestamp": "2025-01-24 01:57:20.533670", "Max Timestamp": "2025-01-24 01:59:21.031060", "MIN - Influent Flow": 0.223, "AVG - Influent Flow": 0.223, "MAX - Influent Flow": 0.223, "MIN - Total Influent Flow - Today": 0.17, "AVG - Total Influent Flow - Today": 0.17, "MAX - Total Influent Flow - Today": 0.171, "MIN - Total Influent Flow - Yesterday": 0.223, "AVG - Total Influent Flow - Yesterday": 0.223, "MAX - Total Influent Flow - Yesterday": 0.223, "MIN - UV Filter #1": -57.0, "AVG - UV Filter #1": -57.0, "MAX - UV Filter #1": -57.0, "MIN - UV Filter #2": 16.0, "AVG - UV Filter #2": 16.0, "MAX - UV Filter #2": 16.0, "MIN - Tank A": 0.64, "AVG - Tank A": 0.674, "MAX - Tank A": 0.7, "MIN - Tank B": 6.08, "AVG - Tank B": 6.144, "MAX - Tank B": 6.24, "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Running", "MIN - Speed #1": 0.0, "AVG - Speed #1": 0.0, "MAX - Speed #1": 0.0, "MIN - Speed #2": 0.0, "AVG - Speed #2": 0.0, "MAX - Speed #2": 0.0, "MIN - Speed #3": 60.0, "AVG - Speed #3": 60.0, "MAX - Speed #3": 60.0, "MIN - Speed #4": 24.0, "AVG - Speed #4": 24.0, "MAX - Speed #4": 24.0},
	{"Min Timestamp": "2025-01-24 01:59:51.153371", "Max Timestamp": "2025-01-24 01:59:51.153371", "MIN - Influent Flow": 0.223, "AVG - Influent Flow": 0.223, "MAX - Influent Flow": 0.223, "MIN - Total Influent Flow - Today": 0.171, "AVG - Total Influent Flow - Today": 0.171, "MAX - Total Influent Flow - Today": 0.171, "MIN - Total Influent Flow - Yesterday": 0.223, "AVG - Total Influent Flow - Yesterday": 0.223, "MAX - Total Influent Flow - Yesterday": 0.223, "MIN - UV Filter #1": -57.0, "AVG - UV Filter #1": -57.0, "MAX - UV Filter #1": -57.0, "MIN - UV Filter #2": 16.0, "AVG - UV Filter #2": 16.0, "MAX - UV Filter #2": 16.0, "MIN - Tank A": 0.7, "AVG - Tank A": 0.7, "MAX - Tank A": 0.7, "MIN - Tank B": 6.12, "AVG - Tank B": 6.12, "MAX - Tank B": 6.12, "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Standby", "MIN - Speed #1": 0.0, "AVG - Speed #1": 0.0, "MAX - Speed #1": 0.0, "MIN - Speed #2": 0.0, "AVG - Speed #2": 0.0, "MAX - Speed #2": 0.0, "MIN - Speed #3": 60.0, "AVG - Speed #3": 60.0, "MAX - Speed #3": 60.0, "MIN - Speed #4": 0.0, "AVG - Speed #4": 0.0, "MAX - Speed #4": 0.0},
	{"Min Timestamp": "2025-01-24 02:00:21.286790", "Max Timestamp": "2025-01-24 02:09:53.651068", "MIN - Influent Flow": 0.223, "AVG - Influent Flow": 0.223, "MAX - Influent Flow": 0.223, "MIN - Total Influent Flow - Today": 0.171, "AVG - Total Influent Flow - Today": 0.172, "MAX - Total Influent Flow - Today": 0.173, "MIN - Total Influent Flow - Yesterday": 0.223, "AVG - Total Influent Flow - Yesterday": 0.223, "MAX - Total Influent Flow - Yesterday": 0.223, "MIN - UV Filter #1": -57.0, "AVG - UV Filter #1": -57.0, "MAX - UV Filter #1": -57.0, "MIN - UV Filter #2": 16.0, "AVG - UV Filter #2": 16.0, "MAX - UV Filter #2": 16.0, "MIN - Tank A": 0.37, "AVG - Tank A": 0.451, "MAX - Tank A": 0.65, "MIN - Tank B": 5.46, "AVG - Tank B": 5.803, "MAX - Tank B": 6.13, "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Standby", "MIN - Speed #1": 0.0, "AVG - Speed #1": 0.0, "MAX - Speed #1": 0.0, "MIN - Speed #2": 0.0, "AVG - Speed #2": 0.0, "MAX - Speed #2": 0.0, "MIN - Speed #3": 53.0, "AVG - Speed #3": 56.65, "MAX - Speed #3": 60.0, "MIN - Speed #4": 0.0, "AVG - Speed #4": 0.0, "MAX - Speed #4": 0.0},
	{"Min Timestamp": "2025-01-24 02:10:23.773998", "Max Timestamp": "2025-01-24 02:19:56.129585", "MIN - Influent Flow": 0.223, "AVG - Influent Flow": 0.223, "MAX - Influent Flow": 0.223, "MIN - Total Influent Flow - Today": 0.173, "AVG - Total Influent Flow - Today": 0.174, "MAX - Total Influent Flow - Today": 0.174, "MIN - Total Influent Flow - Yesterday": 0.223, "AVG - Total Influent Flow - Yesterday": 0.223, "MAX - Total Influent Flow - Yesterday": 0.223, "MIN - UV Filter #1": -57.0, "AVG - UV Filter #1": -57.0, "MAX - UV Filter #1": -57.0, "MIN - UV Filter #2": 16.0, "AVG - UV Filter #2": 16.0, "MAX - UV Filter #2": 16.0, "MIN - Tank A": 0.35, "AVG - Tank A": 0.37, "MAX - Tank A": 0.39, "MIN - Tank B": 4.72, "AVG - Tank B": 5.079, "MAX - Tank B": 5.44, "Blower #1": "IDLE", "Blower #2": "IDLE", "Blower #3": "Running", "Blower #4": "Standby", "MIN - Speed #1": 0.0, "AVG - Speed #1": 0.0, "MAX - Speed #1": 0.0, "MIN - Speed #2": 0.0, "AVG - Speed #2": 0.0, "MAX - Speed #2": 0.0, "MIN - Speed #3": 47.0, "AVG - Speed #3": 50.0, "MAX - Speed #3": 53.0, "MIN - Speed #4": 0.0, "AVG - Speed #4": 0.0, "MAX - Speed #4": 0.0}
]
```
