# Pulling Smart City Data

* [blockchain_seed.py](blockchain_seed.py) - copy of blockchain policies from network (used for prep / pre-deployment)
  * copies cluster, operator and table definition policies 
  
* [blockchain_declare_plants.py](blockchain_declare_plants.py) - create plant policies
```json
 {"plant" : {"name" : "power plant",
             "company" : "Smart City",
             "code" : "pp",
             "address" : "805 Main St, Sabetha, KS 66534",
             "loc" : "39.902911, -95.800508",
             "dbms" : "cos",
             "id" : "2dd2282c3758888214c8388f2e7ae751",
             "date" : "2025-02-01T02:34:09.583701Z",
             "ledger" : "global"}}
```
* [blockchain_tags.py](blockchain_tags.py) - create tag policies based on plant 
```json
 {"tag" : {"name" : "C-A Voltage",
           "company" : "Smart City",
           "table" : "pp_pm",
           "column" : "c_n_voltage",
           "data type" : "integer",
           "unit of measurement" : "kV",
           "plant" : "2dd2282c3758888214c8388f2e7ae751",
           "multiply" : 0.01,
           "id" : "74516232a987b63eb3a17aa8076c665d",
           "date" : "2025-02-01T02:42:28.621181Z",
           "ledger" : "global"}}
```

* [blockchain_monitoring.py](blockchain_monitoring.py) - for power plant, create `monitoring` policies
```json
 {"monitoring" : {"name" : "South Main",
                  "code" : "DF4",
                  "plant" : "2dd2282c3758888214c8388f2e7ae751",
                  "id" : "aef0292e46bc6ca799b074c2faebb0fe",
                  "date" : "2025-02-01T02:50:30.393996Z",
                  "ledger" : "global"}}
```

* [rest_code.py](rest_code.py) - file dedicated to REST calls



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
