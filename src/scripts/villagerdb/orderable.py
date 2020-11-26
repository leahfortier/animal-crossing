from typing import Dict, List

import requests
from lxml import html

from scripts.villagerdb.furniture import items_filename
from scripts.villagerdb.util import write_json_file, read_json_file, get_all_searchable_items

orderable_filename = "orderable.txt"

non_orderables = ['brake-tapper',
                  'campsite-sign',
                  'fortune-cookie-cart',
                  'market-place-decoration',
                  'ok-motors-sign']
orderables = ['fire-pit']


def is_orderable(extension: str) -> bool:
    page = requests.get('https://villagerdb.com' + extension)
    tree = html.fromstring(page.text)

    table_rows = tree.xpath("//table[@class='table item-game-data'][1]//tr/td")
    row_data = {}  # type: Dict[str, str]
    for row in table_rows[::2]:
        row_data[row.text.strip()] = row.getnext().text_content().strip()

    location = row_data.get('Where to get', '')
    if 'Pocket Camp promotion' in location \
            or 'seasonally available' in location \
            or 'Nook Miles System' in location:
        return False

    assert extension.startswith('/item/')
    extension = extension[6:]
    if extension in non_orderables:
        return False
    elif extension in orderables:
        return True

    if 'Orderable?' in row_data:
        orderable = row_data['Orderable?']
        assert orderable in ['Yes', 'No']
        return orderable == "Yes"

    if extension.endswith("-model"):
        return False
    elif extension.endswith("-poster"):
        return False
    elif extension.endswith("-trophy"):
        return False
    elif extension.endswith("-mailbox"):
        return False
    elif extension.startswith("dal-"):
        return False
    elif extension.startswith("moms-"):
        return False
    elif 'birthday' in extension:
        return False
    elif 'pirate' in extension:
        return False

    print(extension)
    assert False


def check_missing_items():
    # Load items previously looked up
    orderable_map = read_json_file(orderable_filename)  # type: Dict[str, bool]

    # Items should only be on furniture list if they are orderable
    item_map = read_json_file(items_filename)  # type: Dict[str, List[str]]
    for item_name in item_map:
        orderable_map[item_name] = True

    search_items = get_all_searchable_items('items/furniture/', '&tag=Not%20Craftable')
    for item in search_items:
        item_name = item.item_name
        if item_name not in orderable_map:
            orderable_map[item_name] = is_orderable(item.extension)
            print(item_name, orderable_map[item_name])

    write_json_file(orderable_filename, orderable_map)

    missing_items = [item_name for item_name in orderable_map if
                     orderable_map[item_name] and item_name not in item_map]  # type: List[str]
    write_json_file("full-missing.txt", missing_items)


check_missing_items()
