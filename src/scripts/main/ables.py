from scripts.analysis.config import FreqConfig
from scripts.analysis.data import check_items
from scripts.item.sheets_item import DataRow, Condition
from scripts.progress.clothing import clothing_progress_filename
from scripts.util.sheets import ables_tabs, clothing_tabs
from scripts.util.user import clothing_user
from scripts.util.util import Strings


def nook_shopping(clothing: DataRow) -> bool:
    return clothing.source == 'Nook Shopping Daily Selection'


# Clothing that can be purchased at ables in the winter
def winter_ables(clothing: DataRow) -> bool:
    if clothing.source != 'Able Sisters':
        return False

    return clothing.availability == "All Year"# or clothing.availability == "Winter"


# Prints missing items and frequencies from the specified tabs that meet the condition
def check_ables(tabs: Strings) -> None:
    check_clothing(tabs, winter_ables)


def check_clothing(tabs: Strings, condition: Condition) -> None:
    config = FreqConfig(clothing_progress_filename)
    check_items(clothing_user, tabs, condition, config)


if __name__ == '__main__':
    # check_clothing(clothing_tabs, nook_shopping)
    check_ables(ables_tabs)
    # check_ables('Tops')
    # check_ables('Bottoms')
    # check_ables('Dress-Up')
    # check_ables('Headwear')
    # check_ables('Accessories')
    # check_ables('Socks')
    # check_ables('Shoes')
