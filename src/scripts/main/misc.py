from typing import List

from scripts.googlesheets.config import check_items
from scripts.googlesheets.data import DataRow, SourceRow
from scripts.googlesheets.sheets import Data
from scripts.user import clothing_user, craftable_user, walls_floors_user, rugs_user


class NooksRow(SourceRow):
    def __init__(self, data: Data, row: List[str]):
        super().__init__("Nook's Cranny", data, row)


def check_umbrellas() -> None:
    check_items(clothing_user, "Umbrellas", NooksRow)


def check_walls_and_floors() -> None:
    check_items(walls_floors_user, ["Wallpaper", "Floors"], NooksRow)


class RugRow(SourceRow):
    def __init__(self, data: Data, row: List[str]):
        super().__init__("Saharah", data, row)


def check_rugs() -> None:
    check_items(rugs_user, "Rugs", RugRow)


class RecipeRow(DataRow):
    def __init__(self, data: Data, row: List[str]):
        super().__init__(False, data, row)

    def condition(self):
        return self.name not in ["bridge construction kit", "campsite construction kit"]


def check_recipes() -> None:
    check_items(craftable_user, "Recipes", RecipeRow)


if __name__ == '__main__':
    # check_recipes()
    check_umbrellas()
    # check_walls_and_floors()
    # check_rugs()
