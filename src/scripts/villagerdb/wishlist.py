from typing import List, Set

from scripts.villagerdb.user import clothing_user, furniture_user, rugs_user
from scripts.villagerdb.util import UserList, ac_folder, get_all_written_items

user_lists = [furniture_user, clothing_user, rugs_user]  # List[UserList]
all_list_items = set()  # Set[str]


def get_all_list_items() -> Set[str]:
    global all_list_items
    if len(all_list_items) > 0:
        return all_list_items

    items = []
    for user in user_lists:
        items = items + get_all_written_items(user)

    all_list_items = set(items)
    return all_list_items


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

    def check_missing(self):
        items = get_all_list_items()
        missing_items = self.read_file(self.folder + "-missing")
        overlap = [item for item in missing_items if item in items]
        for item in overlap:
            print("NOT MISSING??? " + item)


def check_user(user: WishlistUser):
    print(user.user.get_url())

    wishlist_items = get_all_written_items(user.user)  # type: List[str]
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

    user.check_missing()


if __name__ == '__main__':
    check_user(WishlistUser("summer", UserList('summerbowl', 'wishlist')))
    check_user(WishlistUser("kajsa", UserList('kajsa', 'wishlist')))
    check_user(WishlistUser("peachy", UserList('tsunpeach', 'wishlist')))
