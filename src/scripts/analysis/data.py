from typing import List, Type, Callable, Set

from scripts.item.sheets_item import Options
from scripts.util.sheets import Data, read_item_sheet

ConditionType: Type = Callable[[Data, List[str]], bool]


# Print each base name that meets the specified condition (does not print variations)
# Note: the condition method will run for every row and additional checks can be inserted here as necessary
def print_condition(tab_names: List[str], condition: ConditionType) -> None:
    printed = set()  # type: Set[str]
    for tab_name in tab_names:
        data = read_item_sheet(tab_name)  # type: Data
        for row in data.rows:
            name = data.get("Name", row)
            if condition(data, row) and name not in printed:
                print(name)
                printed.add(name)


def print_grouping(tab_names: List[str], group_col: str, group_val: str) -> None:
    groups = set()  # type: Set[str]

    # Keep track of every group while checking for the specified group value
    def group_condition(data: Data, row: List[str]) -> bool:
        group = data.get(group_col, row)
        groups.add(group)
        return group == group_val

    # Prints all rows with the specified group
    print_condition(tab_names, group_condition)

    # Print all values for this column
    print("\nGrouping for " + group_col + ":")
    for group in groups:
        print("\t", group)


# Parses each sheet tab and converts into a combined list of data_type
# Ex: data_type: ClothingItem -> return type: List[ClothingItem]
def get_all_items(data_type: Type, tabs: List[str], options: Options) -> List:
    items = []
    for tab_name in tabs:
        data = read_item_sheet(tab_name)
        for row in data.rows:
            items.append(data_type(data, row, options))
    return items
