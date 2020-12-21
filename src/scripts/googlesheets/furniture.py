from typing import List

from scripts.googlesheets.config import check_items, FreqConfig
from scripts.googlesheets.data import DataRow
from scripts.googlesheets.sheets import Data, item_tabs, floor_item_tabs
from scripts.googlesheets.util import print_grouping, print_condition
from scripts.villagerdb.furniture import items_progress_filename
from scripts.villagerdb.user import furniture_user


# Represents a single row of data from any of the furniture sheets
class FurnitureRow(DataRow):
    def __init__(self, data: Data, row: List[str]):
        super().__init__(True, data, row)
        self.catalog = data.get('Catalog', row)  # type: str

    def condition(self):
        # Set to be filtered to only orderable items
        return self.catalog == 'For sale'


if __name__ == '__main__':
    check_items(furniture_user, item_tabs, FurnitureRow, FreqConfig(items_progress_filename))

    # Other examples like all items you can change clothing at or play music at
    # Prints all items that you can change clothing at
    # print_grouping(item_tabs, "Interact", "Wardrobe")
    # print_condition(floor_item_tabs, lambda data, row: data.get("Speaker Type", row) != "Does not play music")
