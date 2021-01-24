from typing import List, Set, Dict, TextIO

from scripts.item.nookazon import read_nookazon_file, NookazonItem, get_rotated_names
from scripts.item.villagerdb import UserList, get_written_name
from scripts.util.io import ac_folder
from scripts.util.user import clothing_user, furniture_user, rugs_user, walls_floors_user, NookazonUser, \
    craftable_user, free_stuff_user

owned_lists: List[UserList] = [furniture_user, clothing_user, rugs_user, walls_floors_user, craftable_user]
all_owned_items: Set[str] = set()


def get_all_owned_items() -> Set[str]:
    global all_owned_items
    if len(all_owned_items) > 0:
        return all_owned_items

    items = []
    for user in owned_lists:
        items = items + user.get_all_written_items()

    all_owned_items = set(items)
    return all_owned_items


class WishlistUser:
    def __init__(self, folder: str, user: UserList):
        self.folder = folder
        self.user = user
        self.file_suffixes = ["", "-given", "-missing"]

    # Ex: animal crossing/wishlists/peachy/peachy-missing.txt
    def open_file(self, file_suffix: str) -> TextIO:
        file_name = ac_folder + 'wishlists/' + self.folder + "/" + self.folder + file_suffix + ".txt"
        return open(file_name, "r")

    def read_file(self, file_suffix: str) -> List[str]:
        file = self.open_file(file_suffix)
        items = file.readlines()
        items = [item.strip() for item in items]
        items = [item.replace("-", "").replace("+", "") for item in items if not item.endswith(":") and item != ""]
        return items

    # Returns all the items from each of the files
    def get_file_items(self) -> List[str]:
        items = []
        for suffix in self.file_suffixes:
            items = items + self.read_file(suffix)
        return items

    # Returns all the items from user's wishlist
    def get_wishlist_items(self) -> List[str]:
        return self.user.get_all_written_items()

    def backup_lists_contains(self, item_name: str, lists_set: Set[str]) -> bool:
        return False

    def backup_wishlist_contains(self, item_name: str) -> bool:
        return False

    def check_missing(self):
        items = get_all_owned_items()
        missing_items = self.read_file("-missing")
        overlap = [item for item in missing_items if item in items]
        for item in overlap:
            print("NOT MISSING??? " + item)

    def check_free(self):
        free_items: Set[str] = set(free_stuff_user.get_all_written_items())
        order_items = self.read_file("")
        overlap = [item for item in order_items if item in free_items]
        for item in overlap:
            print(item + " IS FREEEEEE")


class NookazonWishlist(WishlistUser):
    def __init__(self, folder: str, user: NookazonUser):
        super().__init__(folder, user)
        self.wishlist: Dict[str, NookazonItem] = {}

    # Unable to read wishlists directly from nookazon, so instead parsing a manual file consisting
    # of a copied and pasted version of all of the text on the wishlist page.....
    def read_wishlist(self) -> Dict[str, NookazonItem]:
        if len(self.wishlist) == 0:
            file = self.open_file("-nookazon")
            lines = file.readlines()
            items: List[NookazonItem] = read_nookazon_file(lines, self.user.username)
            for item in items:
                # item.print_base_name()
                base_name = get_written_name(item.base_name)
                if base_name in self.wishlist:
                    print(base_name + " ALREADY IN WISHLIST!!!")
                self.wishlist[base_name] = item
        return self.wishlist

    def get_wishlist_items(self) -> List[str]:
        return [item_name for item_name in self.read_wishlist()]

    def backup_lists_contains(self, item_name: str, lists_set: Set[str]) -> bool:
        wishlist_items: Dict[str, NookazonItem] = self.read_wishlist()
        potential_names: List[str] = wishlist_items[item_name].potential_names
        for potential_name in potential_names:
            if potential_name in lists_set:
                return True
        # print(item_name, potential_names, wishlist_items[item_name].full_item_name)
        return False

    def backup_wishlist_contains(self, item_name: str) -> bool:
        wishlist_items: Dict[str, NookazonItem] = self.read_wishlist()
        potential_names: List[str] = get_rotated_names(item_name)
        for potential_name in potential_names:
            if potential_name in wishlist_items:
                return True
        # print(item_name, potential_names)
        return False


def check_user(user: WishlistUser):
    print(user.user.get_url())

    list_items: List[str] = user.get_file_items()
    wishlist_items: List[str] = user.get_wishlist_items()

    # Still check items for duplicates and unmissings even though cannot update wishlist changes
    if len(wishlist_items) == 0:
        print("Wishlist not found.")
        wishlist_items = list_items

    items = set()
    for item in list_items:
        if item in items:
            print('duplicate item ' + item)
            return
        items.add(item)

    for item in wishlist_items:
        if item not in items and not user.backup_lists_contains(item, items):
            print(item + " not found in lists.")

    for item in items:
        if item not in wishlist_items and not user.backup_wishlist_contains(item):
            print(item + " not found on wishlist!!")

    user.check_missing()
    user.check_free()


if __name__ == '__main__':
    check_user(WishlistUser("summer", UserList('summerbowl', 'wishlist')))
    check_user(WishlistUser("kajsa", UserList('kajsa', 'wishlist')))
    check_user(WishlistUser("peachy", UserList('tsunpeach', 'wishlist')))
    check_user(NookazonWishlist('oofhelia', NookazonUser('2388988778', 'oofhelia0186')))
    check_user(NookazonWishlist('cheryl', NookazonUser('3053266368', 'Sequinn3791')))
    check_user(NookazonWishlist('destiny', NookazonUser('723532342', 'sbspexpert6120')))
