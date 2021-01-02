from scripts.analysis.config import check_items
from scripts.item.sheets_item import DataRow, Options, Condition
from scripts.util.user import clothing_user, craftable_user, walls_floors_user, rugs_user, UserList
from scripts.util.util import Strings


# Special recipes to be ignored
def recipe_condition(row: DataRow) -> bool:
    return row.name not in ["bridge construction kit", "campsite construction kit"]


# Checks all the recipes (excluding a couple special cases)
def check_recipes() -> None:
    check_items(craftable_user, "Recipes", Options().with_condition(recipe_condition))


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
    condition: Condition = source_filter(source_name)
    check_items(user_list, tabs, Options().with_condition(condition))


if __name__ == '__main__':
    # check_recipes()
    check_umbrellas()
    # check_walls_and_floors()
    # check_rugs()
