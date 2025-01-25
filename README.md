# Pulling Smart City Data

The following provides a sample script to pull data from our smart city demo. 

[blockchain_tagging.py](blockchain_tagging.py) - Generate a list of tags (one per column) for `wwp_analog` data

[blockchain_get_data.py](blockchain_get_data.py) - Using information from tags, execute `increment` and `period` 
queries.

The select columns for tags is based <a href="http://23.239.12.151:3100/d/ads1vwji3bvnkd/overview?orgId=1&refresh=5m" targer="_blanl">Waste Water Dashboard</a>

[get_data.py](get_data.py) - Given a list of tables (_water_ and _waste water_), generate a list of corresponding columns,,
and get raw data, as well as summary data for the last 24 hours. The data is then stored into corresponding files. 


## Comments
**What is period**: The period function finds the first occurrence of data before or at a specified date and considers 
the readings in a period of time which is measured by the type of the time interval. 

**What is increments**: The increments functions considers data in increments of time (i.e. every 5 minutes) within a 
time range