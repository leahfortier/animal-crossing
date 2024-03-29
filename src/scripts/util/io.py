import json

from typing import List, IO, TextIO

ac_folder = "/Users/leahfortier/Dropbox/games/animal crossing/"

in_file_path = "../in/"
out_file_path = ac_folder + "villagerdb/"


def open_file(filename: str, file_path: str):
    path = file_path + filename
    try:
        return open(path, "r")
    except IOError:
        # File does not exist
        print("could not open " + path)


# Returns each line in the file
def read_file(filename: str, file_path=in_file_path) -> List[str]:
    f = open_file(filename, file_path)
    contents: List[str] = f.readlines()
    f.close()
    return [line.strip() for line in contents]


# Opens the specified file and reads the json string contents into a map
def read_json_file(filename: str, file_path=in_file_path, default=None, object_hook=None):
    if default is None:
        default = {}

    f = open_file(filename, file_path)
    if f:
        json_data = json.load(f, object_hook=object_hook)
        f.close()
        return json_data
    else:
        # Okay if file doesn't exist, just print and create a new map
        return default


def read_json_out_file(filename: str):
    return read_json_file(filename, file_path=out_file_path)


def write_input_json_file(filename: str, json_data):
    write_json_file(filename, json_data, file_path=in_file_path)


# Creates the specified file and saves the input map as a json string
# json_data should be a valid json data type
def write_json_file(filename: str, json_data, file_path=out_file_path, cls=None):
    f = open(file_path + filename, "w")
    json.dump(json_data, f, indent=4, sort_keys=True, cls=cls)
    f.close()
