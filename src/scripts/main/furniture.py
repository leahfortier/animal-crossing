from typing import List

from scripts.analysis.config import check_items, FreqConfig
from scripts.item.sheets_item import DataRow, Options
from scripts.util.sheets import Data, item_tabs
from scripts.progress.furniture import items_progress_filename


# Represents a single row of data from any of the furniture sheets
from scripts.util.user import furniture_user


class FurnitureRow(DataRow):
    def __init__(self, data: Data, row: List[str], options: Options):
        super().__init__(data, row, options.with_variations())
        self.catalog: str = data.get('Catalog', row)
        self.body_customize: bool = data.get("Body Customize", row) == "Yes"

        if self.body_customize:
            self.variation = ''

    def condition(self):
        # Set to be filtered to only orderable items
        return self.catalog == 'For sale'


def is_orderable(furniture: FurnitureRow) -> bool:
    return furniture.catalog == 'For sale'


if __name__ == '__main__':
    # Prints out missing orderable items and frequencies
    options = Options().with_condition(is_orderable)
    config = FreqConfig(items_progress_filename)
    check_items(furniture_user, item_tabs, options, FurnitureRow, config)

    # Similar to above but prints out each missing variation instead of totals
    # check_items(furniture_user, item_tabs, options, FurnitureRow)

    # Other examples
    # Prints all items that you can change clothing at
    # print_grouping(item_tabs, "Interact", "Wardrobe")

    # All DIY stations or musical instruments
    # print_grouping(item_tabs, "Tag", "Work Bench")
    # print_grouping(item_tabs, "Tag", "Musical Instrument")

    # Items that play music
    # print_condition(floor_item_tabs, lambda data, row: data.get("Speaker Type", row) != "Does not play music")
