from typing import List

from scripts.googlesheets.data import DataRow, get_all_items
from scripts.googlesheets.sheets import Data, ables_tabs
from scripts.googlesheets.config import check_items, Strings, FreqConfig
from scripts.villagerdb.clothing import clothing_progress_filename
from scripts.villagerdb.user import clothing_user


# Represents a single row of data from any of the clothing sheets
class ClothingRow(DataRow):
    def __init__(self, data: Data, row: List[str]):
        super().__init__(True, data, row)
        self.event = data.get('Season/Event', row)  # type: str
        self.availability = data.get("Seasonal Availability", row)  # type: str
        self.seasonality = data.get("Seasonality", row)  # type: str

    def condition(self):
        if self.source != 'Able Sisters':
            return False

        # Change this line as needed
        # Example query checking against all winter clothing for sale at ables
        return self.availability == "All Year" or self.availability == "Winter"


# Prints missing items and frequencies from the specified tabs that meet the condition
def check_ables(tabs: Strings) -> None:
    check_items(clothing_user, tabs, ClothingRow, FreqConfig(clothing_progress_filename))


if __name__ == '__main__':
    check_ables(ables_tabs)
    # check_ables('Tops')
    # check_ables('Bottoms')
    # check_ables('Dress-Up')
    # check_ables('Headwear')
    # check_ables('Accessories')
    # check_ables('Socks')
    # check_ables('Shoes')
