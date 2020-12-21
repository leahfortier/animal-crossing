from abc import ABC
from typing import List, Type

from scripts.googlesheets.sheets import Data, read_item_sheet
from scripts.villagerdb.util import get_written_name


class DataRow(ABC):
    def __init__(self, has_variation: bool, data: Data, row: List[str]):
        self.name = data.get('Name', row)  # type: str
        self.source = data.get("Source", row)  # type: str

        self.variation = ''  # type: str
        if has_variation:
            self.variation = data.get('Variation', row)
            if self.variation == 'NA':
                self.variation = ''

    # Returns the written name with its variation
    # Ex: 'acid washed jacket black'
    def get_written_name(self) -> str:
        return get_written_name(self.name + " " + self.variation)

    # No condition by default
    def condition(self):
        return True


# Filters out all rows which do not match the source filter
class SourceRow(DataRow):
    def __init__(self, source_filter: str, data: Data, row: List[str]):
        super().__init__(False, data, row)
        self.filtered = self.source == source_filter

    def condition(self):
        return self.filtered


# Parses each sheet tab and converts into a combined list of data_type
# Ex: data_type: ClothingItem -> return type: List[ClothingItem]
def get_all_items(data_type: Type, tabs: List[str]) -> List:
    items = []
    for tab_name in tabs:
        data = read_item_sheet(tab_name)
        for row in data.rows:
            items.append(data_type(data, row))
    return items
