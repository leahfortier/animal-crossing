from typing import Set, List, Callable, Type, Union

from scripts.googlesheets.sheets import read_item_sheet, Data

ConditionType: Type = Callable[[Data, List[str]], bool]

# A type to represent either a single string or a list of strings
Strings: Type = Union[str, List[str]]


# Converts the Strings object into a List
def get_strs(s: Strings) -> List[str]:
    if type(s) == str:
        return [s]
    return s


def print_totals(total_missing: int, total_items: int) -> None:
    if total_items == 0:
        print("No matches for that condition.")
    else:
        percentage = 100 * (total_items - total_missing) / total_items
        print("\n{0}/{1} Missing -- {2:.2f}% Complete".format(total_missing, total_items, percentage))


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
