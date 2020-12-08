from typing import List

from scripts.villagerdb.user import free_stuff_user
from scripts.villagerdb.util import ac_folder, get_all_written_items


def read_file() -> List[str]:
    file = open(ac_folder + "mouse-given.txt", "r")
    items = file.readlines()
    items = [item.strip() for item in items]
    return items


def compare_free_stuff():
    free_stuff = get_all_written_items(free_stuff_user)  # type: List[str]
    given_stuff = read_file()  # type: List[str]

    for item in free_stuff:
        if item in given_stuff:
            print("ALREADY GIVEN: " + item)
        # else:
        #     print(item)
