from typing import List

from scripts.util.io import ac_folder
from scripts.util.user import free_stuff_user


def read_file() -> List[str]:
    file = open(ac_folder + "mouse-given.txt", "r")
    items = file.readlines()
    items = [item.strip() for item in items]
    return items


def compare_free_stuff():
    free_stuff: List[str] = free_stuff_user.get_all_written_items()
    given_stuff: List[str] = read_file()

    for item in free_stuff:
        if item in given_stuff:
            print("ALREADY GIVEN: " + item)
        # else:
        #     print(item)


if __name__ == '__main__':
    compare_free_stuff()
