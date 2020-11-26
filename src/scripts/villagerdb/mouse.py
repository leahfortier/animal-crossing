from typing import List

from scripts.villagerdb.util import UserList, get_all_user_items, ItemRow, ac_folder

free_stuff_list = UserList('dragonair', 'free-stuff')


def get_item_name(item: ItemRow) -> str:
    item = item.full_item_name
    item = item.lower()
    item = item.replace("(", "")
    item = item.replace(")", "")
    item = item.replace("-", " ")
    if '/' in item:
        item = item[:item.rfind('/')]
    item = item.strip()
    return item


def read_file() -> List[str]:
    file = open(ac_folder + "mouse-given.txt", "r")
    items = file.readlines()
    items = [item.strip() for item in items]
    return items


def compare_free_stuff():
    free_stuff = get_all_user_items(free_stuff_list)           # type: List[ItemRow]
    free_stuff = [get_item_name(item) for item in free_stuff]  # type: List[str]

    given_stuff = read_file()  # type: List[str]

    for item in free_stuff:
        if item in given_stuff:
            print("ALREADY GIVEN: " + item)
