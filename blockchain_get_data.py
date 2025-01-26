import argparse
from get_data import execute_get, write_data

DB_NAME = 'cos'

def __check_value(value):
    try:
        value = int(value)
    except Exception as error:
        raise argparse.ArgumentTypeError(f"{value} is an invalid int value")
    else:
        if value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return value


def blockchain_get_plant(conn:str, plant_code:str):
    """
    Get plant policy ID from blockchain based on plant_code
    """
    cmd = f'blockchain get plant where code={plant_code} bring [*][id]'
    plant_id = execute_get(conn=conn, command=cmd, is_query=False)

    return plant_id


def blockchain_get_tag(conn:str, plant_id:str):
    """
    Given plant code, get list of columns
    """
    cmd = f'blockchain get tag where plant={plant_id}'
    tags = execute_get(conn=conn, command=cmd, is_query=False)

    write_data(table_name='blockchain', data_type='metadata', data=tags)

    return tags


def period_query(conn:str, tags:dict, timestamp_column:str, interval_value:int, interval:str):
    """
    Get latest 1 day of data
    https://github.com/AnyLog-co/documentation/blob/master/queries.md#the-period-function
    """
    table_name = tags[0]['tag']['table']
    columns = [timestamp_column]
    for tag in tags:
        columns.append(tag['tag']['column'])

    query = f'sql {DB_NAME} format=json:list and stat=false "SELECT {",".join(columns)} FROM {table_name} WHERE period({interval}, {interval_value}, now(), {timestamp_column})"'
    output = execute_get(conn=conn, command=query, is_query=True)

    for index in range(len(output)):
        for tag in tags:
            column_name = tag['tag']['column']
            name = tag['tag']['name']
            if column_name in output[index]:
                output[index][name] = output[index].pop(column_name)
                if 'mapping' in tag['tag']:
                    output[index][name] = tag['tag']['mapping'][str(output[index][name])]


    write_data(table_name=table_name, data_type='raw', data=output)


def increments_query(conn:str, tags:dict, timestamp_column:str, interval_value:int, interval:str, where_interval:str, where_interval_value:str):
    """
    Get summary of data over a given interval
    https://github.com/AnyLog-co/documentation/blob/master/queries.md#the-increment-function
    """
    table_name = tags[0]['tag']['table']
    columns = [f"MIN({timestamp_column}) as min_ts", f"MAX({timestamp_column}) as max_ts"]
    group_by = []
    for tag in tags:
        if 'mapping' in tag['tag']:
            columns.append(tag['tag']['column'])
            group_by.append(tag['tag']['column'])
        else:
            columns.append(f'MIN({tag["tag"]["column"]})::float(3)')
            columns.append(f'AVG({tag["tag"]["column"]})::float(3)')
            columns.append(f'MAX({tag["tag"]["column"]})::float(3)')

    query = f'sql {DB_NAME} format=json:list and stat=false SELECT increments({interval}, {interval_value}, {timestamp_column}), {",".join(columns)} FROM {table_name} WHERE {timestamp_column} >= NOW() - {where_interval_value} {where_interval}  GROUP BY {",".join(group_by)}'
    output = execute_get(conn=conn, command=query, is_query=True)

    data = [{'Min Timestamp': row['min_ts'], 'Max Timestamp': row['max_ts']} for row in output]

    for index in range(len(output)):
        for tag in tags:
            for key in output[index]:
                if tag['tag']['column'] in key and 'min' in key:
                    data[index][f'MIN - {tag["tag"]["name"]}'] = output[index][key]
                elif tag['tag']['column'] in key and 'avg' in key:
                    data[index][f'AVG - {tag["tag"]["name"]}'] = output[index][key]
                elif tag['tag']['column'] in key and 'max' in key:
                    data[index][f'MAX - {tag["tag"]["name"]}'] = output[index][key]
                elif tag['tag']['column'] in key and 'mapping' in tag['tag']:
                    data[index][tag["tag"]["name"]] = tag['tag']['mapping'][str(output[index][key])]

    write_data(table_name=table_name, data_type='increments', data=data)


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
    parser =  argparse.ArgumentParser()
    parser.add_argument('--conn', type=str, default='45.79.18.179:32349', help='REST connection')
    parser.add_argument('--plant-code', type=str, default='wwp', choices=['wwp'], help='plant code')
    parser.add_argument('--timestamp-column', type=str, default='timestamp', help='timestamp column name')
    parser.add_argument('--increments-interval', type=str, default='minute', choices=['minute', 'hour', 'day'], help='increment time interval')
    parser.add_argument('--increments-interval-value', type=__check_value, default=10, help='increment time interval valaue')
    parser.add_argument('--where-interval', type=str, default='day', choices=['minute', 'hour', 'day'], help='where increment time interval in WHERE condition')
    parser.add_argument('--where-interval-value', type=__check_value, default=1, help='increment time interval used in WHERE condition')
    parser.add_argument('--all-data', type=bool, const=True, nargs='?', default=False, help='Get all data')
    parser.add_argument('--summary-data', type=bool, const=True, nargs='?', default=False, help='Get summary of data')
    args = parser.parse_args()

    plant_id = blockchain_get_plant(conn=args.conn, plant_code=args.plant_code)
    tags = blockchain_get_tag(conn=args.conn, plant_id=plant_id)


    if args.all_data is True:
        period_query(conn=args.conn, tags=tags, timestamp_column=args.timestamp_column,
                     interval_value=args.where_interval_value, interval=args.where_interval)

    if args.summary_data is True:
        increments_query(conn=args.conn, tags=tags, timestamp_column=args.timestamp_column,
                         interval_value=args.increments_interval_value, interval=args.increments_interval,
                         where_interval=args.where_interval, where_interval_value=args.where_interval_value)


if __name__ == '__main__':
    main()
