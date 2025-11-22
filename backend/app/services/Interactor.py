import json
import os
from pathlib import Path


def load_json(file_name:str):
    path = Path(__file__).resolve().parents[1] / "data" / file_name
    with path.open("r", encoding="UTF-8") as f:
        if f == None:
            raise FileNotFoundError("JSON file not found error")
        return json.load(f)

def write_to_json(file_name:str, data):
    path = Path(__file__).resolve().parents[1] / "data" / file_name
    tmp_path = path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="UTF-8") as t:
        json.dump(data, t, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)

def get_new_id(data, id_key:str):
    prev_id = data[-1][id_key]
    return str(int(prev_id) + 1)

#takes the name of a json file, the string key of ids for that file, and a new entry, and adds that 
#entry to the file.
def create_item(file_name:str, id_key:str, item: dict):
    data = load_json(file_name)
    new_id = get_new_id(data, id_key)
    item[id_key] = new_id
    data.append(item)
    write_to_json(file_name, data)

def remove_item(file_name:str, id_key:str, id: int):
    items = load_json(file_name)
    for item in items:
        if item[id_key] == str(id):
                items.remove(item)
    write_to_json(file_name, items)