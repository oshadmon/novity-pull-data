import json
import requests

def publish_policy(conn:str, policy:dict):
    new_policy = f"<new_policy={json.dumps(policy)}>"
    headers = {
        'command': 'blockchain insert where policy=!new_policy and local=true and master=!ledger_conn',
        'User-Agent': 'AnyLog/1.23'
    }

    try:
        r = requests.post(url=f"http://{conn}", headers=headers, data=new_policy)
    except Exception as error:
        raise Exception(f"Failed to POST data against {conn} (Error: {error})")
    else:
        if not 200 <= int(r.status_code) < 300:
            raise ConnectionError(f"Failed to POST data against {conn} (Error: {r.status_code})")


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


def get_columns(conn:str, table_name:str):
    """
    Extract list of columns for each table
    """
    cmd = f"get columns where dbms=cos and table={table_name} and format=json"
    output = execute_get(conn=conn, command=cmd, is_query=False)

    # remove columns associated with AnnyLog data management
    for column in ['row_id', 'insert_timestamp', 'tsd_name', 'tsd_id']:
        del output[column]
    return output
