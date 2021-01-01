from typing import List

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
