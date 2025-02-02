import os
import json

def write_data(file_path:str, data:list):
    try:
        with open(file_path, 'w') as f:
            f.write("[\n")
            for value in data:
                try:
                    if value != data[-1]:
                        f.write("\t" + json.dumps(value) + ",\n")
                    else:
                        f.write("\t" + json.dumps(value) + "\n")
                except Exception as error:
                    raise Exception(f"Failed to dump data into {file_path} (Error: {error})")
            f.write("]")
    except Exception as error:
        raise Exception(f"Failed to open file {file_path} (Error: {error})")


def read_data(file_name:str):
    full_path = os.path.expanduser(os.path.expandvars(file_name))
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


if __name__ == '__main__':
    file_path  = input('File: ')
    read_data(read_data(file_path=file_path))