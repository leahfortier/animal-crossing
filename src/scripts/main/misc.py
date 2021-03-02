from scripts.analysis.config import FreqConfig
from scripts.analysis.data import check_items
from scripts.item.sheets_item import DataRow, Condition
from scripts.progress.furniture import items_progress_filename
from scripts.util.sheets import item_tabs
from scripts.util.user import clothing_user, craftable_user, walls_floors_user, rugs_user, UserList, furniture_user
from scripts.util.util import Strings


def is_orderable(item: DataRow) -> bool:
    return item.catalog == 'For sale'


# Prints out missing orderable items and frequencies
def check_furniture() -> None:
    config = FreqConfig(items_progress_filename)
    check_items(furniture_user, item_tabs, is_orderable, config)

    # Similar to above but prints out each missing variation instead of totals
    # check_items(furniture_user, item_tabs, is_orderable)


# Special recipes to be ignored
def recipe_condition(row: DataRow) -> bool:
    return row.name not in ["bridge construction kit", "campsite construction kit"]


# Checks all the recipes (excluding a couple special cases)
def check_recipes() -> None:
    check_items(craftable_user, "Recipes", recipe_condition)


# Checks all the umbrellas which can be purchased from Nook's Cranny
def check_umbrellas() -> None:
    check_nooks_items(clothing_user, "Umbrellas")


# Checks all the wallpapers and floorings which can be purchased from Nook's Cranny
def check_walls_and_floors() -> None:
    check_nooks_items(walls_floors_user, ["Wallpaper", "Floors"])


# Checks all the rugs that come from Saharah
def check_rugs() -> None:
    check_source_items(rugs_user, "Rugs", "Saharah")


# Returns a condition which filters out all rows which do not match the source filter
def source_filter(source_name: str) -> Condition:
    return lambda row: row.source == source_name


# Compares all the items in the tabs from Nook's Cranny to the user's items
def check_nooks_items(user_list: UserList, tabs: Strings):
    check_source_items(user_list, tabs, "Nook's Cranny")


# Compares all the items in the tabs with the specified source to the user's items
def check_source_items(user_list: UserList, tabs: Strings, source_name: str):
    check_items(user_list, tabs, source_filter(source_name))


if __name__ == '__main__':
    check_furniture()
    # check_recipes()
    # check_umbrellas()
    # check_walls_and_floors()
    # check_rugs()

    # Other examples
    # Prints all items that you can change clothing at
    # print_grouping(item_tabs, "Interact", "Wardrobe")

    # All DIY stations or musical instruments
    # print_grouping(item_tabs, "Tag", "Work Bench")
    # print_grouping(item_tabs, "Tag", "Musical Instrument")

    # Items that play music and all 2x1 Surfaces
    # print_condition(floor_item_tabs, lambda data, row: data.get("Speaker Type", row) != "Does not play music")
    # print_condition(floor_item_tabs, lambda data, row: data.get("Size", row) == "2x1" and data.get("Surface", row) == "Yes")
