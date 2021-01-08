from typing import List

from scripts.util.io import ac_folder, read_file
from scripts.util.user import free_stuff_user


def compare_free_stuff():
    free_stuff: List[str] = free_stuff_user.get_all_written_items()
    given_stuff: List[str] = read_file("mouse-given.txt", file_path=ac_folder)

    for item in free_stuff:
        if item in given_stuff:
            print("ALREADY GIVEN: " + item)
        # else:
        #     print(item)


if __name__ == '__main__':
    compare_free_stuff()
