from typing import List

from scripts.villagerdb.util import UserList, get_all_user_items, ItemRow, ac_folder


class WishlistUser:
    def __init__(self, folder: str, user: UserList, *additional_suffix: str):
        self.folder = folder
        self.user = user
        self.file_suffixes = ["given", "missing", *additional_suffix]

    def read_file(self, file_name: str) -> List[str]:
        file = open(ac_folder + self.folder + "/" + file_name + ".txt", "r")
        items = file.readlines()
        items = [item.strip() for item in items]
        items = [item.replace("-", "").replace("+", "") for item in items if not item.endswith(":") and item != ""]
        return items

    def get_items(self) -> List[str]:
        items = self.read_file(self.folder)

        # Add all the items from each of the remaining lists
        for suffix in self.file_suffixes:
            items = items + self.read_file(self.folder + "-" + suffix)

        return items


def get_item_name(item: ItemRow) -> str:
    item = item.full_item_name
    item = item.lower()
    item = item.replace("(", "")
    item = item.replace(")", "")
    item = item.replace("-", " ")
    item = item.replace(" recipe", "")
    if '/' in item:
        item = item[:item.rfind('/')]
    item = item.strip()
    return item


def check_user(user: WishlistUser):
    print(user.user.get_url())

    wishlist_items = get_all_user_items(user.user)  # type: List[ItemRow]
    wishlist_items = [get_item_name(item) for item in wishlist_items]  # type: List[str]

    list_items = user.get_items()  # List[str]

    items = set()
    for item in list_items:
        if item in items:
            print('duplicate item ' + item)
            return
        items.add(item)

    for item in wishlist_items:
        if item not in items:
            print(item + " not found in lists.")

    for item in items:
        if item not in wishlist_items:
            print(item + " not found on wishlist!!")


check_user(WishlistUser("summer", UserList('summerbowl', 'wishlist')))
check_user(WishlistUser("kajsa", UserList('kajsa', 'wishlist')))
check_user(WishlistUser("peachy", UserList('tsunpeach', 'wishlist')))
