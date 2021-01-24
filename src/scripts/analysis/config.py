from abc import ABC

from typing import Dict

from scripts.item.sheets_item import DataRow
from scripts.util.io import read_json_out_file
from scripts.util.util import get_written_name


class MissingFreq:
    def __init__(self):
        self.map: Dict[str, int] = {}

    def add(self, name: str):
        name = get_written_name(name)
        if name not in self.map:
            self.map[name] = 0
        self.map[name] += 1

    def get(self, name: str):
        return self.map[name]

    def print_totals(self, progress_filename: str):
        user_totals: Dict[str, str] = read_totals_map(progress_filename)

        for item in self.map:
            num_missing: int = self.map[item]
            total: int = num_missing
            if item in user_totals:
                total_split: [str] = user_totals[item].split('/')
                total = int(total_split[1])
            if num_missing > 0:
                print(item + " " + str(total - num_missing) + "/" + str(total))


# user_totals is a map from written item name to user totals in the form "4/5"
def read_totals_map(progress_filename: str) -> Dict[str, str]:
    full_map = read_json_out_file(progress_filename)
    user_totals: Dict[str, str] = {}
    for item_name in full_map:
        clothing_name = get_written_name(item_name)
        clothing_item = full_map[item_name]
        user_totals[clothing_name] = clothing_item["total"]
    return user_totals


class Config(ABC):
    def on_missing(self, item: DataRow) -> None:
        pass

    def finish(self) -> None:
        pass


class PrintConfig(Config):
    def on_missing(self, item: DataRow) -> None:
        print(item.get_written_name())


class FreqConfig(Config):
    def __init__(self, progress_filename):
        self.missing_freq = MissingFreq()
        self.progress_filename = progress_filename

    def on_missing(self, item: DataRow) -> None:
        self.missing_freq.add(item.name)

    def finish(self) -> None:
        self.missing_freq.print_totals(self.progress_filename)
