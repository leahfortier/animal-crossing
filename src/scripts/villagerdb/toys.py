from typing import List, Dict, Type

from scripts.villagerdb.furniture import items_progress_filename
from scripts.villagerdb.util import print_items, read_json_out_file, read_file

peachy_toys_file = "peachy-toys.txt"
MissingMap: Type = Dict[str, List[str]]

dee_missing: MissingMap = {
    'Dinosaur Toy': [],
    'Dollhouse': ['Pink'],
    'Kids\' Tent': [],
    'Mini Circuit': [],
    'Pop-up Book': [],
    'Puppy Plushie': ['Pink'],
    'RC Helicopter': ['Yellow'],
    'Set Of Stockings': ['Chic'],
    'Tin Robot': ['Orange', 'Black'],
}


def add_toy(toy_list: List[str], toy_name: str, variation: str) -> None:
    toy_list.append(toy_name + " - " + variation)


def get_missing() -> MissingMap:
    progress_map = read_json_out_file(items_progress_filename)

    missing_toys: MissingMap = {}
    for toy_name in dee_missing:
        missing: List[str] = []
        if "missing" in progress_map[toy_name]:
            missing = progress_map[toy_name]["missing"]
        missing_toys[toy_name] = missing

    return missing_toys


# Update peachy's toy list by copying this spreadsheet to input file:
# https://docs.google.com/spreadsheets/d/194e1iMe3L3zRyxuDXDMCuOYXMypThW4erwF46hTBl9s
def get_peachy_missing() -> MissingMap:
    peachy_missing: MissingMap = {}
    for toy_name in dee_missing:
        peachy_missing[toy_name] = []

    contents: List[str] = read_file(peachy_toys_file)[3:]
    for row in contents:
        split = row.split("\t")
        toy_name = split[0]
        variation = split[1]
        is_missing = split[2].strip() == "0"

        if toy_name.startswith("Kids"):
            toy_name = "Kids' Tent"
        elif toy_name == 'Pop-Up Book':
            toy_name = 'Pop-up Book'
        elif toy_name == 'Set of Stockings':
            toy_name = "Set Of Stockings"

        if is_missing:
            peachy_missing[toy_name].append(variation)

    return peachy_missing


def compare_toys(name: str, their_missing: MissingMap):
    for_them: List[str] = []
    from_them: List[str] = []
    both_missing: List[str] = []

    missing_toys: MissingMap = get_missing()
    for toy_name in their_missing:
        for variation in missing_toys[toy_name]:
            if variation not in their_missing[toy_name]:
                add_toy(from_them, toy_name, variation)
            else:
                add_toy(both_missing, toy_name, variation)

        for variation in their_missing[toy_name]:
            if variation not in missing_toys[toy_name]:
                add_toy(for_them, toy_name, variation)

    print_items("For " + name, for_them)
    print_items("From " + name, from_them)
    print_items("Both Missing", both_missing)


def print_missing():
    progress_map = read_json_out_file(items_progress_filename)

    missing_toys: Dict[str, List[str]] = get_missing()
    for toy_name in missing_toys:
        print(toy_name, progress_map[toy_name]["total"], missing_toys[toy_name])


if __name__ == '__main__':
    # compare_toys("Dee", dee_missing)
    # compare_toys("Peachy", get_peachy_missing())
    print_missing()
