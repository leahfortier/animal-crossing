from abc import ABC

from typing import List, Type, Callable, Set

from scripts.item.villagerdb import get_written_name
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


class DataRow(ABC):
    def __init__(self, has_variation: bool, data: Data, row: List[str]):
        self.name = data.get('Name', row)  # type: str
        self.source = data.get("Source", row)  # type: str

        self.variation = ''  # type: str
        if has_variation:
            self.variation = data.get('Variation', row)
            if self.variation == 'NA':
                self.variation = ''

    # Returns the written name with its variation
    # Ex: 'acid washed jacket black'
    def get_written_name(self) -> str:
        return get_written_name(self.name + " " + self.variation)

    # No condition by default
    def condition(self):
        return True


# Filters out all rows which do not match the source filter
class SourceRow(DataRow):
    def __init__(self, source_filter: str, data: Data, row: List[str]):
        super().__init__(False, data, row)
        self.filtered = self.source == source_filter

    def condition(self):
        return self.filtered


# Parses each sheet tab and converts into a combined list of data_type
# Ex: data_type: ClothingItem -> return type: List[ClothingItem]
def get_all_items(data_type: Type, tabs: List[str]) -> List:
    items = []
    for tab_name in tabs:
        data = read_item_sheet(tab_name)
        for row in data.rows:
            items.append(data_type(data, row))
    return items
