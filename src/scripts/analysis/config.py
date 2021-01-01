from abc import ABC

from typing import Dict, Type, List, Set

from scripts.analysis.data import DataRow, get_all_items
from scripts.util.io import read_json_out_file
from scripts.util.user import UserList
from scripts.util.util import get_written_name, Strings, get_strs, print_totals


class MissingFreq:
    def __init__(self):
        self.map = {}  # type: Dict[str, int]

    def add(self, name: str):
        name = get_written_name(name)
        if name not in self.map:
            self.map[name] = 0
        self.map[name] += 1

    def get(self, name: str):
        return self.map[name]

    def print_totals(self, progress_filename: str):
        user_totals = read_totals_map(progress_filename)  # type: Dict[str, str]

        for item in self.map:
            num_missing = self.map[item]  # type: int
            total = num_missing  # type: int
            if item in user_totals:
                total_split = user_totals[item].split('/')  # type: [str]
                total = int(total_split[1])
            if num_missing > 0:
                print(item + " " + str(total - num_missing) + "/" + str(total))


# user_totals is a map from written item name to user totals in the form "4/5"
def read_totals_map(progress_filename: str) -> Dict[str, str]:
    full_map = read_json_out_file(progress_filename)
    user_totals = {}  # type: Dict[str, str]
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


# Compares the items in each tab sheet with the items in the specified user list (on villagerdb)
# Each row of the sheet should be of type data_type and filtering conditions should occur there as well
# Config objects handle extra things that can be happening if you want but honestly they're dumb
def check_items(user_list: UserList, tabs: Strings, data_type: Type, config: Config = PrintConfig()) -> None:
    user_items: Set[str] = set(user_list.get_all_written_items())
    all_items: List[DataRow] = get_all_items(data_type, get_strs(tabs))

    total_missing = 0
    total_items = 0
    for item in all_items:
        if not item.condition():
            continue
        total_items += 1

        name = item.get_written_name()
        if name not in user_items:
            total_missing += 1
            config.on_missing(item)

    config.finish()
    print_totals(total_missing, total_items)
