import argparse
import json
import os.path

from rest_code import execute_get
from file_io import write_data

CONN = "172.236.61.154:32349"

def __check_value(value):
    try:
        value = int(value)
    except Exception as error:
        raise argparse.ArgumentTypeError(f"{value} is an invalid int value")
    else:
        if value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return value


def __format_results(results:dict, tags_list:list, monitor_list):
    for tag in tags_list:
        if tag['tag']['column'] in results:
            if 'multiply' in tag['tag']:
                results[tag['tag']['column']] = results[tag['tag']['column']] * tag['tag']['multiply']
            elif 'mapping' in tag['tag']:
                results[tag['tag']['column']] = tag['tag']['mapping'][str(results[tag['tag']['column']])]
            results[tag['tag']['name']] = results.pop(tag['tag']['column'])
        elif f"min_{tag['tag']['column']}" in results:
            column_name = f"min_{tag['tag']['column']}"
            if 'multiply' in tag['tag']:
                results[column_name] = results[column_name] * tag['tag']['multiply']
            elif 'mapping' in tag['tag']:
                results[tag['tag']['column']] = tag['tag']['mapping'][str(results[column_name])]
            results[f"Min {tag['tag']['name']}"] = results.pop(column_name)
        elif f"max_{tag['tag']['column']}" in results:
            column_name = f"max_{tag['tag']['column']}"
            if 'multiply' in tag['tag']:
                results[column_name] = results[column_name] * tag['tag']['multiply']
            elif 'mapping' in tag['tag']:
                results[tag['tag']['column']] = tag['tag']['mapping'][str(results[column_name])]
            results[f"Max {tag['tag']['name']}"] = results.pop(column_name)
        elif f"avg_{tag['tag']['column']}" in results:
            column_name = f"avg_{tag['tag']['column']}"
            if 'multiply' in tag['tag']:
                results[column_name] = results[column_name] * tag['tag']['multiply']
            elif 'mapping' in tag['tag']:
                results[tag['tag']['column']] = tag['tag']['mapping'][str(results[column_name])]
            results[f"Avg {tag['tag']['name']}"] = results.pop(column_name)

        # if tag['tag']['column'] in results:
        #     if 'multiply' in tag['tag']:
        #         results[f"min_{tag['tag']['column']}"] = results[f"min_{tag['tag']['column']}"] * tag['tag']['multiply']
        #     if 'mapping' in tag['tag']:
        #         results[tag['tag']['name']] = tag['tag']['mapping'][str(results[tag['tag']['name']])]
        #     results[tag['tag']['name']] = results.pop(tag['tag']['column'])
        #
        # elif f"min_{tag['tag']['column']}" in results:
        #     if 'multiply' in tag['tag']:
        #         results[f"min_{tag['tag']['column']}"] = results[f"min_{tag['tag']['column']}"] * tag['tag']['multiply']
        #     if 'mapping' in tag['tag']:
        #         results[f"min_{tag['tag']['column']}"] = tag['tag']['mapping'][str(results[tag['tag']['name']])]
        #     results[f"Min {tag['tag']['name']}"] = results.pop(f"min_{tag['tag']['column']}")
        #
        # elif f"avg_{tag['tag']['column']}" in results:
        #     results[f"Avg {tag['tag']['name']}"] = results.pop(f"avg_{tag['tag']['column']}")
        # elif f"max_{tag['tag']['column']}" in results:
        #     results[f"Max {tag['tag']['name']}"] = results.pop(f"max_{tag['tag']['column']}")
        # if all('Monitor' in x for x in [results, tag['tag']['name']]):
        #     try:
        #         results[tag['tag']['name']] = monitor_list[results[tag['tag']['name']].strip()]
        #     except:
        #         pass

    return results

def __write_data(results:list, plant:str, query_type:str):
    if not os.path.isdir('data'):
        os.makedirs('data')
    file_path = os.path.join('data', f'{plant}.{query_type}.0.json')
    write_data(file_path=file_path, data=results)

def __print_results(results:list):
    for result in results:
        print(json.dumps(result) + "\n")


def __execute_request(command:str, tag_policies:list, monitor_list, query_type:str, plant_code:str, file_store:bool=False):
    print(command)
    output = execute_get(conn=CONN, command=command, is_query=True)
    for i in range(len(output)):
        output[i] = __format_results(results=output[i], tags_list=tag_policies, monitor_list=monitor_list)

    if file_store:
        __write_data(results=output, plant=plant_code, query_type=query_type)
    else:
        __print_results(results=output)


def main():
    """
    :optional arguments:
        -h, --help                                                  show this help message and exit
        --conn                          CONN                        REST connection
        --plant-code                    PLANT_CODE                  plant code
        --increments-interval           INCREMENTS_INTERVAL         increment time interval
        --increments-interval-value     INCREMENTS_INTERVAL_VALUE   increment time interval value
        --where-interval                WHERE_INTERVAL              where increment time interval in WHERE condition
        --where-interval-value          WHERE_INTERVAL_VALUE        increment time interval used in WHERE condition
        --all-data                      [ALL_DATA]                  Get all data
        --summary-data                  [SUMMARY_DATA]              Get summary of data
    :return:
    """
    monitoring = execute_get(conn=CONN, command='blockchain get monitoring bring [*][code] separator=,', is_query=False).split(",")
    monitoring.append(None)
    parser =  argparse.ArgumentParser()
    parser.add_argument('--plant-code', type=str, default='wwp', choices=['pp', 'wp', 'wwp'], help='plant code')
    parser.add_argument('--timestamp-column', type=str, default='timestamp', help='timestamp column name')
    parser.add_argument('--interval', type=str, default='day', choices=['minute', 'hour', 'day'], help='time interval size')
    parser.add_argument('--interval-value', type=__check_value, default=1, help='increment time interval valaue')
    parser.add_argument('--increments-interval', type=str, default='minute', choices=['minute', 'hour', 'day'], help='time interval size')
    parser.add_argument('--increments-interval-value', type=__check_value, default=10, help='increment time interval valaue')
    parser.add_argument('--monitor-where', type=str, default=None, choices=monitoring, help='monitoring value for where condition')
    parser.add_argument('--limit', type=__check_value, default=None, help='limit row returned')
    parser.add_argument('--raw-data', type=bool, const=True, nargs='?', default=False, help='Get all data')
    parser.add_argument('--aggregate-data', type=bool, const=True, nargs='?', default=False, help='Get summary of data')
    parser.add_argument('--file-store', type=bool, const=True, nargs='?', default=False, help='write results to file')
    args = parser.parse_args()

    cmd = f'blockchain get plant where code={args.plant_code}'
    plant = execute_get(conn=CONN, command=cmd, is_query=False)
    plant_id = plant[0]['plant']['id']
    dbms = plant[0]['plant']['dbms']

    monitor_list = {}

    if args.plant_code == 'pp':
        table_name = f"{args.plant_code}_pm"
        cmd = f"blockchain get monitoring where plant={plant_id}"
        output = execute_get(conn=CONN, command=cmd, is_query=False)
        for monitor in output:
            monitor_list[monitor['monitoring']['code']] = monitor['monitoring']['name']

        cmd = f"blockchain get tag where table={table_name}"
        tag_policies = execute_get(conn=CONN, command=cmd, is_query=False)
    else:
        table_name = f"{args.plant_code}_analog"
        cmd = f"blockchain get tag where table={table_name}"
        tag_policies = execute_get(conn=CONN, command=cmd, is_query=False)

    anylog_cmd = f"sql {dbms} format=json:list and stat=false"
    if args.raw_data is True:
        query = f"SELECT {args.timestamp_column}, "
        for tag in tag_policies:
            query += f"{tag['tag']['column']}, "
        query = query.rsplit(',', 1)[0]
        query += f" FROM {table_name} WHERE period({args.interval}, {args.interval_value}, NOW(), {args.timestamp_column})"
        if args.plant_code == 'pp' and args.monitor_where is not None:
            query += f' and monitoring_id={args.monitor_where}'
        if args.limit is not None:
            query += f" limit {args.limit}"

        cmd = anylog_cmd + " " + query
        __execute_request(command=cmd, tag_policies=tag_policies, monitor_list=monitor_list, query_type='raw',
                          plant_code=args.plant_code, file_store=args.file_store)

    if args.aggregate_data is True:
        query = f"SELECT increments({args.increments_interval}, {args.increments_interval_value}, {args.timestamp_column}), min({args.timestamp_column}) as min_ts, max({args.timestamp_column}) as max_ts, "
        group_by = []
        for tag in tag_policies:
            if tag['tag']['data type'] in ['numeric', 'integer', 'float', 'double']:
                column = tag['tag']['column']
                query += f"min({column})::float(3) as min_{column}, avg({column})::float(3) as avg_{column}, max({column})::float(3) as max_{column},"
            else:
                column = tag['tag']['column']
                query += f"{column}, "
                group_by.append(column)
        query = query.rsplit(',', 1)[0]
        query += f" FROM {table_name} WHERE {args.timestamp_column} <= NOW() - {args.interval_value} {args.interval}"
        if args.plant_code == 'pp' and args.monitor_where is not None:
            query += f' and monitoring_id={args.monitor_where}'
        if group_by:
            query += f" GROUP BY {','.join(group_by)}"
        if args.limit is not None:
            query += f" limit {args.limit}"

        cmd = anylog_cmd + " " + query
        __execute_request(command=cmd, tag_policies=tag_policies, monitor_list=monitor_list, query_type='aggregate',
                          plant_code=args.plant_code, file_store=args.file_store)












if __name__ == '__main__':
    main()
