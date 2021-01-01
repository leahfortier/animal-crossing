from typing import List

from scripts.analysis.config import check_items, FreqConfig
from scripts.analysis.data import DataRow
from scripts.util.sheets import Data, item_tabs
from scripts.progress.furniture import items_progress_filename


# Represents a single row of data from any of the furniture sheets
from scripts.util.user import furniture_user


class FurnitureRow(DataRow):
    def __init__(self, data: Data, row: List[str]):
        super().__init__(True, data, row)
        self.catalog = data.get('Catalog', row)  # type: str

    def condition(self):
        # Set to be filtered to only orderable items
        return self.catalog == 'For sale'


if __name__ == '__main__':
    check_items(furniture_user, item_tabs, FurnitureRow, FreqConfig(items_progress_filename))

    # Other examples
    # Prints all items that you can change clothing at
    # print_grouping(item_tabs, "Interact", "Wardrobe")

    # All DIY stations or musical instruments
    # print_grouping(item_tabs, "Tag", "Work Bench")
    # print_grouping(item_tabs, "Tag", "Musical Instrument")

    # Items that play music
    # print_condition(floor_item_tabs, lambda data, row: data.get("Speaker Type", row) != "Does not play music")