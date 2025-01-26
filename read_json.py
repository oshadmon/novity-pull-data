import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('file_name', type=str, default='blockchain.metadata.json', help='JSON file to read')
args = parser.parse_args()

full_path = os.path.expanduser(os.path.expandvars(args.file_name))
if os.path.isfile(full_path):
    try:
        with open(full_path, 'r') as f:
            # print(f.read().replace("\t", "").replace("\n",""))
            data = json.load(f)
            print(data)
    except Exception as error:
        raise Exception(f"Failed to read content in {full_path} (Error; {error})")
else:
    raise FileNotFoundError(f"Failed to locate {full_path}")
