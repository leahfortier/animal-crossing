from typing import List, Dict

from scripts.villagerdb.util import UserList, get_all_user_items, write_json_file


def get_all_items(user: UserList) -> List[str]:
    user_items = get_all_user_items(user)
    return [item.full_item_name for item in user_items]


def add_compare(compare_map: Dict[str, List[str]], user: UserList, user_items: List[str], other_items: List[str]):
    only_user = [item_name for item_name in user_items if item_name not in other_items]
    compare_map[user.username + "/" + user.list_name + " only"] = only_user


def compare_lists(first_user: UserList, second_user: UserList, extension: str):
    first_items = get_all_items(first_user)
    second_items = get_all_items(second_user)

    compare_map = {}  # type: Dict[str, List[str]]
    add_compare(compare_map, first_user, first_items, second_items)
    add_compare(compare_map, second_user, second_items, first_items)

    write_json_file("comparison-" + extension + ".txt", compare_map)


compare_lists(UserList('dragonair', 'furniture'), UserList('polygonia', 'owned-furniture'), "furniture")
compare_lists(UserList('dragonair', 'craftable'), UserList('polygonia', 'diys-owned'), "diys")
