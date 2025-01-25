import json
import requests

CONN = '45.79.18.179:32349'
TABLES = {
    'wwp_analog': None,
    'wwp_digital': None,
    'wp_analog': None,
    'wp_digital': None
}

def write_data(table_name:str, data_type:str, data:list):
    file_path = f'{table_name}.{data_type}.json'
    try:
        with open(file_path, 'w') as f:
            f.write("[\n")
            for value in data:
                try:
                    f.write("\t" + json.dumps(value) + ",\n")
                except Exception as error:
                    raise Exception(f"Failed to dump data into {file_path} (Error: {error})")
            f.write("]")
    except Exception as error:
        raise Exception(f"Failed to open file {file_path} (Error: {error})")


def execute_get(conn:str, command:str, is_query:bool=False):
    headers = {
        "command": command,
        "User-Agent": "AnyLog/1.23"
    }

    if is_query is True:
        headers['destination'] = 'network'

    try:
        r = requests.get(url=f"http://{conn}", headers=headers)
    except Exception as error:
        raise Exception(f"Failed to execute GET against {conn} (Error: {error})")
    else:
        if not 200 <= int(r.status_code) < 300:
            raise ConnectionError(f"Failed to execute GET against {conn} (Network Error: {r.status_code})")
        try:
            output = r.json()
        except Exception:
            output = r.text
    return output


def get_columns():
    """
    Extract list of columns for each table
    """
    for table in TABLES:
        cmd = f"get columns where dbms=cos and table={table} and format=json"
        output = execute_get(conn=CONN, command=cmd, is_query=False)
        columns = list(output.keys())
        # remove columns associated with AnnyLog data management
        for column in ['row_id', 'insert_timestamp', 'tsd_name', 'tsd_id']:
            columns.pop(columns.index(column))
        TABLES[table] = columns


def get_raw_data(table_name:str, columns:list):
    """
    Get latest 1 day of data
    https://github.com/AnyLog-co/documentation/blob/master/queries.md#the-period-function
    """
    query = f'sql cos format=json:list and stat=false "SELECT {",".join(columns)} FROM {table_name} WHERE period(day, 1, now(), timestamp)"'
    output = execute_get(conn=CONN, command=query, is_query=True)
    write_data(table_name=table_name, data_type='raw', data=output)


def get_increments(table_name:str, columns:list):
    """
    Get summary of data over a given interval
    https://github.com/AnyLog-co/documentation/blob/master/queries.md#the-increment-function

    due to the amount of computation (we're on a single machine) I've limited the query to run only against 6 columns
    """
    query = f'sql cos format=json:list and stat=false "SELECT increments(minute, 10, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
    group_by = []
    i = 0
    for column in columns:
        if 'analog' in table_name and column != 'timestamp':
            query += f'min({column}) as min_{column}, '
            query += f'avg({column}) as avg_{column}, '
            query += f'max({column}) as max_{column}, '
        elif column != 'timestamp':
            query += f"{column}, "
            group_by.append(column)
        i += 1
        if i > 5:
            break

    query = query.rsplit(",", 1)[0] + f' FROM {table_name} WHERE timestamp >= NOW() - 1 day'
    if group_by:
        query += f" GROUP BY {','.join(group_by)}"
    query += ';"'
    output = execute_get(conn=CONN, command=query, is_query=True)
    write_data(table_name=table_name, data_type='increments', data=output)


if __name__ == '__main__':
    get_columns()
    for table in TABLES:
        get_raw_data(table_name=table, columns=TABLES[table])
        get_increments(table_name=table, columns=TABLES[table])