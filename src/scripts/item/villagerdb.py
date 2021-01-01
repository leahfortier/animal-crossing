import json

import requests
from lxml import html
from typing import Dict
from typing import List

from scripts.util.user import UserList
from scripts.util.util import get_written_name


# Returns all possible variations as listed on villagerdb
# Ex: Beach Towel -> ["Blue", "Colorful", ..., "Yellow"]
# Ex: Electric Guitar -> ["Cherry", "Cherry / Chic logo", ..., "Sunburst / Rock logo"]
def get_all_variations(extension: str) -> List[str]:
    assert extension.startswith('/item/')

    page = requests.get('https://villagerdb.com' + extension)
    tree = html.fromstring(page.text)

    item_entity = tree.xpath("//div[@data-entity-type='item']")[0]
    variations_json = item_entity.get('data-variations')

    # List of all variations
    return list(json.loads(variations_json).values())


class Item:
    def __init__(self, item_name: str, extension: str):
        self.item_name = item_name
        self.extension = extension
        self.variations = []

    def add_variations(self, *variations: str):
        self.variations.append(*variations)


# All the relevant information about a single item row
# Note: each variation should have a separate ItemRow entry
class ItemRow:
    def __init__(self, row):
        row_link = row.xpath('div/div/a[2]')[0]

        # Ex: '/item/accessories-stand'
        self.extension: str = row_link.get('href')

        # Ex: 'Accessories Stand (Black)'
        self.full_item_name: str = row.get('data-name')

        # Ex: 'Accessories Stand'
        self.item_name: str = row_link.text

    # Ex: Accessories Stand (Black) -> accessories stand black
    def get_written_name(self) -> str:
        return get_written_name(self.full_item_name)


def get_all_user_items(user: UserList) -> List[ItemRow]:
    page = requests.get(user.get_url())
    tree = html.fromstring(page.text)
    items = tree.xpath('/html/body/div[2]/main/ul/li')

    items_list = []  # type: List[ItemRow]
    for row in items:
        items_list.append(ItemRow(row))

    return items_list


# Read's the user's villagerdb list and return a map of each item
def get_user_variations(user: UserList) -> Dict[str, Item]:
    user_items = get_all_user_items(user)  # type: List[ItemRow]

    # Holds the variations of items the user has
    # Key is a pair of the item name and its url extension
    # If the item has no variations, it will map to a list of size one containing the empty string
    variations_map = {}  # type: Dict[str, Item]

    for item in user_items:
        # Ex: 'Accessories Stand (Black)' and 'Accessories Stand'
        full_name = item.full_item_name
        item_name = item.item_name

        # Ex: '(Black)'
        # Note: Not all items will have a variation and this will be empty
        # (it may have customizable options but really need to trust user input to know this)
        assert full_name.startswith(item_name)
        variation = full_name[len(item_name):].strip()
        assert variation == '' or (variation.startswith('(') and variation.endswith(')'))
        variation = variation[1:-1]

        # First variation of this item in the list
        if item_name not in variations_map:
            variations_map[item_name] = Item(item_name, item.extension)

        # Add this variation to the map
        variations_map[item_name].add_variations(variation)

    return variations_map
