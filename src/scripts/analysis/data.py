from typing import List, Type, Callable, Set

from scripts.analysis.config import Config, PrintConfig
from scripts.item.sheets_item import DataRow, Condition, accept_all
from scripts.util.sheets import Data, read_item_sheet
from scripts.util.user import UserList
from scripts.util.util import print_totals, Strings, get_strs

ConditionType: Type = Callable[[Data, List[str]], bool]


# Print each base name that meets the specified condition (does not print variations)
# Note: the condition method will run for every row and additional checks can be inserted here as necessary
def print_condition(tab_names: List[str], condition: ConditionType) -> None:
    printed: Set[str] = set()
    for tab_name in tab_names:
        data: Data = read_item_sheet(tab_name)
        for row in data.rows:
            name = data.get("Name", row)
            if condition(data, row) and name not in printed:
                print(name)
                printed.add(name)


def print_grouping(tab_names: List[str], group_col: str, group_val: str) -> None:
    groups: Set[str] = set()

    # Keep track of every group while checking for the specified group value
    def group_condition(data: Data, row: List[str]) -> bool:
        value = data.get(group_col, row)
        groups.add(value)
        return value == group_val

    # Prints all rows with the specified group
    print_condition(tab_names, group_condition)

    # Print all values for this column
    print("\nGrouping for " + group_col + ":")
    for group in groups:
        print("\t", group)


# Parses each sheet tab and converts into a combined list of DataRow
def get_all_items(tabs: Strings) -> List[DataRow]:
    items = []
    for tab_name in get_strs(tabs):
        data = read_item_sheet(tab_name)
        for row in data.rows:
            items.append(DataRow(data, row))
    return items


# If only needing the name from each row and nothing else
def get_all_written_names(tabs: Strings) -> List[str]:
    items: List[DataRow] = get_all_items(tabs)
    return [item.get_written_name() for item in items]


# Compares the items in each tab sheet with the items in the specified user list (on villagerdb)
# Each row of the sheet should be of type data_type and filtering conditions should occur there as well
# Config objects handle extra things that can be happening if you want but honestly they're dumb
def check_items(user_list: UserList,
                tabs: Strings,
                condition: Condition = accept_all,
                config: Config = PrintConfig()) -> None:
    user_items: Set[str] = set(user_list.get_all_written_items())
    all_items: List[DataRow] = get_all_items(tabs)

    # Some items will be the same for our purposes (customizations etc.) and only want to count unique orderables
    seen_items: Set[str] = set()

    total_missing = 0
    total_items = 0
    for item in all_items:
        name = item.get_written_name()
        if name in seen_items or not condition(item):
            continue

        total_items += 1
        seen_items.add(name)

        if name not in user_items:
            total_missing += 1
            config.on_missing(item)

    config.finish()
    print_totals(total_missing, total_items)
