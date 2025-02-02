import argparse
import json
import os

from rest_code import execute_get
from file_io import write_data

CONN = '172.236.61.154:32349'


def get_plant(plant_name:str=None):
    cmd = "blockchain get plant"
    if plant_name:
        cmd += f' where name="{plant_name}"'
    cmd += f' bring [*][id] separator=,'
    output = execute_get(conn=CONN, command=cmd, is_query=False)
    return output

def get_policy(policy_type:str, plant_id:str=None, plant_name:str=None):
    cmd = f"blockchain get {policy_type}"
    if policy_type == 'plant' and plant_name:
        cmd += f" where name={plant_name}"
    elif plant_id:
        cmd += f" where plant={plant_id}"

    output = execute_get(conn=CONN, command=cmd, is_query=False)
    return output


def main():
    output = execute_get(conn=CONN, command='blockchain get plant bring [*][name] separator=,', is_query=False)

    plants=output.split(',')
    parse = argparse.ArgumentParser()
    parse.add_argument('--policy-type', type=str, default='plant', choices=['plant', 'tag', 'monitoring'], help='policy type')
    parse.add_argument('--plant-name', type=str, default=None, choices=plants, help='list of plants')
    parse.add_argument('--write-file', type=bool, const=True, default=False, nargs='?', help='write polciies to file')
    args = parse.parse_args()

    plant_id = None
    if args.policy_type in ['tag', 'monitoring'] and args.plant_name is not None:
        plant_id = get_plant(plant_name=args.plant_name)
    policies = get_policy(policy_type=args.policy_type, plant_id=plant_id, plant_name=args.plant_name)

    if args.write_file is True:
        if not os.path.isdir('metadata'):
            os.makedirs('metadata')

        file_name = os.path.join('metadata', f'{args.policy_type}.json')
        if args.plant_name:
            file_name  = os.path.join('metadata', f'{args.plant_name.replace(" ", "_")}.{args.policy_type}.json')
        write_data(file_path=file_name, data=policies)
    else:
        print(json.dumps(policies, indent=2))



if __name__ == '__main__':
    main()