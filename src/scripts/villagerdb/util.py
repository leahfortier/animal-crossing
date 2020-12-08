import json
from typing import List, Dict

import requests
from lxml import html

ac_folder = "/Users/leahfortier/Dropbox/games/animal crossing/"

in_file_path = "in/"
out_file_path = ac_folder + "villagerdb/"


# Opens the specified file and reads the json string contents into a map
def read_json_file(filename: str, file_path=in_file_path, default=None):
    if default is None:
        default = {}

    path = file_path + filename
    try:
        f = open(path, "r")
        json_data = json.load(f)
        f.close()
        return json_data
    except IOError:
        # Okay if file doesn't exist, just print and create a new map
        print("could not open " + path)
        return default


def write_input_json_file(filename: str, json_data):
    write_json_file(filename, json_data, file_path=in_file_path)


# Creates the specified file and saves the input map as a json string
# json_data should be a valid json data type
def write_json_file(filename: str, json_data, file_path=out_file_path):
    f = open(file_path + filename, "w")
    json.dump(json_data, f, indent=4, sort_keys=True)
    f.close()


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
        self.extension = row_link.get('href')  # type: str

        # Ex: 'Accessories Stand (Black)'
        self.full_item_name = row.get('data-name')  # type: str

        # Ex: 'Accessories Stand'
        self.item_name = row_link.text  # type: str

    # Ex: Accessories Stand (Black) -> accessories stand black
    def get_written_name(self) -> str:
        item = self.full_item_name
        item = item.lower()
        item = item.replace("(", "")
        item = item.replace(")", "")
        item = item.replace("-", " ")
        item = item.replace(" recipe", "")
        if '/' in item:
            item = item[:item.rfind('/')]
        item = item.strip()
        return item


# Holds the username and name of the user's list
# Gives the appropriate url for the item's list
class UserList:
    def __init__(self, username: str, list_name: str):
        self.username = username
        self.list_name = list_name

    def get_url(self) -> str:
        return 'https://villagerdb.com/user/' + self.username + '/list/' + self.list_name


def get_all_written_items(user: UserList) -> List[str]:
    items = get_all_user_items(user)
    return [item.get_written_name() for item in items]


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


def get_item_progress(all_variations: List[str], user_variations: List[str]):
    progress = {"total": str(len(user_variations)) + "/" + str(len(all_variations))}

    completed = []
    missing = []
    for variation in all_variations:
        if variation in user_variations:
            completed.append(variation)
        else:
            missing.append(variation)

    if len(missing) > 0:
        progress["completed"] = completed
        progress["missing"] = missing

    return progress


class SearchItem:
    def __init__(self, item):
        self.item_name = item.get('name')
        self.extension = item.get('url')


def get_all_searchable_items(extension: str, extra_args: str) -> List[SearchItem]:
    search_items = []  # type: List[SearchItem]

    # Will be updated to actual value on the first iteration
    total_pages = 1000

    # Go through each page to check each item
    page_num = 1
    while page_num <= total_pages:
        # Ex: https://villagerdb.com/search/page/1?game=nh&q=poster
        # Ex: https://villagerdb.com/items/furniture/page/1?game=nh&tag=Not%20Craftable
        page = requests.get('https://villagerdb.com/' + extension
                            + 'page/' + str(page_num) + '?game=nh' + extra_args)
        tree = html.fromstring(page.text)
        entity_browser = tree.xpath("//div[@id='entity-browser']")[0]
        page_data = json.loads(entity_browser.get('data-initial-state'))

        # Update total_pages to actual value
        total_pages = page_data.get('totalPages')
        page_num += 1

        items = page_data.get('results')
        for item in items:
            search_items.append(SearchItem(item))

    return search_items


def print_items(title: str, item_list: List[str]):
    if len(item_list) > 0:
        print(title + ":")
        for item_name in item_list:
            print("\t", item_name)
        print()


def check_items(user: UserList, items_filename: str, progress_filename: str, get_variations):
    # Load the variations map so don't need to look up every time
    item_map = read_json_file(items_filename)

    # Holds the variations of items the user has
    user_items = get_user_variations(user)  # type: Dict[str, Item]

    for item_name in user_items:
        # If item not in map yet, load all possible variations of it and store
        if item_name not in item_map:
            item = user_items[item_name]
            item_map[item_name] = get_variations(item.extension, item.variations)

    # Output any new items to same file
    write_input_json_file(items_filename, item_map)

    progress_map = {}
    for item_name in user_items:
        all_variations = item_map[item_name]
        user_variations = user_items[item_name].variations
        progress_map[item_name] = get_item_progress(all_variations, user_variations)

    prev_progress_map = read_json_file(progress_filename, file_path=out_file_path)

    just_added = []
    just_completed = []
    just_updated = []
    for item_name in progress_map:
        item_progress = progress_map[item_name]
        current_total = item_progress["total"]

        if item_name not in prev_progress_map:
            just_added.append(item_name + " " + current_total)
            continue

        prev_progress = prev_progress_map[item_name]
        if "missing" in prev_progress and "missing" not in item_progress:
            just_completed.append(item_name + " " + current_total)
        elif "completed" in prev_progress and prev_progress["completed"] != item_progress["completed"]:
            just_updated.append(item_name + ": " + prev_progress["total"] + "->" + current_total)

    print_items("Just added!", just_added)
    print_items("Just completed!", just_completed)
    print_items("Newly updated!", just_updated)

    # Write all completed items to separate file
    write_json_file(progress_filename, progress_map)
