from json import JSONEncoder

from typing import List, Set, Dict

from scripts.analysis.data import get_all_items
from scripts.item.sheets_item import DataRow
from scripts.util.io import write_json_file, read_json_file, in_file_path
from scripts.util.sheets import item_tabs, clothing_tabs
from scripts.util.util import get_if, get_written_name, Strings

BASE_NAME = "__base__"
variations_filename = "variations.txt"


class ItemVariations(JSONEncoder):
    def __init__(self, skipkeys=False, ensure_ascii=True,
                 check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                         check_circular=check_circular, allow_nan=allow_nan, indent=indent,
                         separators=separators,
                         default=default, sort_keys=sort_keys)
        self.variations: Set[str] = set()
        self.customizations: Set[str] = set()
        self.diy: bool = False

    def default(self, o):
        return {
            "variations": list(o.variations),
            "customizations": list(o.customizations),
            "diy": o.diy,
        }

    def decode(self, value: Dict):
        self.variations = set(get_if(value, "variations", []))
        self.customizations = set(get_if(value, "customizations", []))
        self.diy = get_if(value, "diy", False)

    def add(self, item: DataRow):
        self.diy = item.diy
        variation = item.variation
        pattern = item.pattern

        if item.body_customize:
            if pattern != "":
                pattern = " / " + pattern
            pattern = variation + pattern
            variation = ""

        if variation:
            self.variations.add(variation)
        if pattern:
            self.customizations.add(pattern)

    def print(self, item_name: str):
        print(item_name, self.encode(self))


def decoder(value: Dict):
    if BASE_NAME in value:
        return value
    variations = ItemVariations()
    variations.decode(value)
    return variations


item_map: Dict[str, ItemVariations] = {}


def read_variations() -> Dict[str, ItemVariations]:
    global item_map
    if len(item_map) == 0:
        item_map = read_json_file(variations_filename, object_hook=decoder)
        del item_map[BASE_NAME]
    return item_map


# Only returns then the item_name is in the map
def get_item_variations(item_name: str) -> ItemVariations:
    item_map = read_variations()
    item_name = get_written_name(item_name)
    if item_name in item_map:
        return item_map[item_name]


# Only returns then the item_name is in the map
def get_item_variation(item_name: str) -> (str, str):
    item_map: Dict[str, ItemVariations] = read_variations()
    key_name: str = get_written_name(item_name)

    while key_name != "":
        if key_name in item_map:
            break
        key_name = key_name[:key_name.rfind(" ")].strip()

    if key_name == "":
        print("NO KEY NAME FOUND FOR " + item_name)
        return None

    variations: ItemVariations = item_map[key_name]
    assert variations is not None

    variation_name = item_name.removeprefix(key_name).strip()
    return key_name, variation_name


def get_variations(tabs: Strings) -> Dict[str, ItemVariations]:
    item_map: Dict[str, ItemVariations] = {
        BASE_NAME: True,
    }

    previous_name = ''
    all_items: List[DataRow] = get_all_items(tabs)

    for item in all_items:
        item_name = get_written_name(item.name)
        if item_name != previous_name:
            assert item_name not in item_map or item_name == "butterfly fish model"
            previous_name = item_name
            item_map[item_name] = ItemVariations()
        variations = item_map[item_name]
        variations.add(item)

    return item_map


def write_variations() -> None:
    item_map = get_variations(item_tabs + clothing_tabs)
    write_json_file(variations_filename, item_map, file_path=in_file_path, cls=ItemVariations)
