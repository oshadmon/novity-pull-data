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
