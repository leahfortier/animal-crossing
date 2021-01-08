from typing import List

from scripts.analysis.config import FreqConfig
from scripts.analysis.data import check_items
from scripts.item.sheets_item import DataRow, Options
from scripts.progress.clothing import clothing_progress_filename
from scripts.util.sheets import Data, ables_tabs
from scripts.util.user import clothing_user
from scripts.util.util import Strings


# Represents a single row of data from any of the clothing sheets
class ClothingRow(DataRow):
    def __init__(self, data: Data, row: List[str], options: Options):
        super().__init__(data, row, options)
        self.event: str = data.get('Season/Event', row)
        self.availability: str = data.get("Seasonal Availability", row)
        self.seasonality: str = data.get("Seasonality", row)


# Clothing that can be purchased at ables in the winter
def winter_ables(clothing: ClothingRow) -> bool:
    if clothing.source != 'Able Sisters':
        return False

    return clothing.availability == "All Year" or clothing.availability == "Winter"


# Prints missing items and frequencies from the specified tabs that meet the condition
def check_ables(tabs: Strings) -> None:
    options = Options().with_condition(winter_ables)
    config = FreqConfig(clothing_progress_filename)
    check_items(clothing_user, tabs, options, ClothingRow, config)


if __name__ == '__main__':
    check_ables(ables_tabs)
    # check_ables('Tops')
    # check_ables('Bottoms')
    # check_ables('Dress-Up')
    # check_ables('Headwear')
    # check_ables('Accessories')
    # check_ables('Socks')
    # check_ables('Shoes')
