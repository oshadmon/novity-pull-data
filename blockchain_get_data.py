from get_data import execute_get, CONN, write_data

TIMESTAMP_COLUMN = 'timestamp'
PLANT_CODE = 'wwp'
DB_NAME = 'cos'


def blockchain_get_plant(plant_code:str):
    """
    Get plant policy ID from blockchain based on plant_code
    """
    cmd = f'blockchain get plant where code={plant_code} bring [*][id]'
    plant_id = execute_get(conn=CONN, command=cmd, is_query=False)

    return plant_id


def blockchain_get_tag(plant_id:str):
    """
    Given plant code, get list of columns
    """
    cmd = f'blockchain get tag where plant={plant_id}'
    tags = execute_get(conn=CONN, command=cmd, is_query=False)

    write_data(table_name='blockchain', data_type='metadata', data=tags)

    return tags


def period_query(tags):
    """
    Get latest 1 day of data
    https://github.com/AnyLog-co/documentation/blob/master/queries.md#the-period-function
    """
    table_name = tags[0]['tag']['table']
    columns = [TIMESTAMP_COLUMN]
    for tag in tags:
        columns.append(tag['tag']['column'])

    query = f'sql {DB_NAME} format=json:list and stat=false "SELECT {",".join(columns)} FROM {table_name} WHERE period(day, 1, now(), timestamp)"'
    output = execute_get(conn=CONN, command=query, is_query=True)
    for index in range(len(output)):
        for tag in tags:
            column_name = tag['tag']['column']
            name = tag['tag']['name']
            if column_name in output[index]:
                output[index][name] = output[index].pop(column_name)
                if 'mapping' in tag['tag']:
                    output[index][name] = tag['tag']['mapping'][str(output[index][name])]

    write_data(table_name=table_name, data_type='raw', data=output)


def increments_query(tags):
    """
    Get summary of data over a given interval
    https://github.com/AnyLog-co/documentation/blob/master/queries.md#the-increment-function
    """
    table_name = tags[0]['tag']['table']
    columns = [f"MIN({TIMESTAMP_COLUMN}) as min_ts", f"MAX({TIMESTAMP_COLUMN}) as max_ts"]
    group_by = []
    for tag in tags:
        if 'mapping' in tag['tag']:
            columns.append(tag['tag']['column'])
            group_by.append(tag['tag']['column'])
        else:
            columns.append(f'MIN({tag["tag"]["column"]})::float(3)')
            columns.append(f'AVG({tag["tag"]["column"]})::float(3)')
            columns.append(f'MAX({tag["tag"]["column"]})::float(3)')

    query = f'sql {DB_NAME} format=json:list and stat=false SELECT increments(minute, 10, {TIMESTAMP_COLUMN}), {",".join(columns)} FROM {table_name} WHERE {TIMESTAMP_COLUMN} >= NOW() - 1 day GROUP BY {",".join(group_by)}'
    output = execute_get(conn=CONN, command=query, is_query=True)

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
    plant_id = blockchain_get_plant(plant_code=PLANT_CODE)
    tags = blockchain_get_tag(plant_id=plant_id)
    period_query(tags=tags)
    increments_query(tags=tags)

if __name__ == '__main__':
    main()
