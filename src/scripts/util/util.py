from typing import List, Type, Union, Dict

# A type to represent either a single string or a list of strings
Strings: Type = Union[str, List[str]]


# Converts the Strings object into a List
def get_strs(s: Strings) -> List[str]:
    if type(s) == str:
        return [s]
    return s


# Ex: Accessories Stand (Black) -> accessories stand black
def get_written_name(full_item_name: str) -> str:
    item = full_item_name.strip()
    item = item.lower()
    item = item.replace("(", "")
    item = item.replace(")", "")
    item = item.replace("-", " ")
    item = item.replace("s' ", "s ")
    item = item.replace(" recipe", "")
    if '/' in item:
        item = item[:item.rfind('/')]
    item = item.strip()
    return item


def print_items(title: str, item_list: List[str]):
    if len(item_list) > 0:
        print(title + ":")
        for item_name in item_list:
            print("\t", item_name)
        print()


def print_totals(total_missing: int, total_items: int) -> None:
    if total_items == 0:
        print("No matches for that condition.")
    else:
        percentage = 100 * (total_items - total_missing) / total_items
        print("\n{0}/{1} Missing -- {2:.2f}% Complete".format(total_missing, total_items, percentage))


def get_if(map: Dict[str, any], key: str, default: any) -> any:
    if key in map:
        return map[key]
    return default
