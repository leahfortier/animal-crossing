from typing import List, Dict, Type, Callable

from scripts.util.sheets import Data
from scripts.util.util import get_written_name


class Options:
    def __init__(self):
        self.condition: Condition = lambda row: True
        self.options: Dict[str, any] = {}

    def with_condition(self, condition):
        self.condition = condition
        return self

    def with_option(self, key: str, value: any):
        self.options[key] = value
        return self

    def get(self, key: str):
        return self.options[key]


class DataRow:
    def __init__(self, data: Data, row: List[str], options: Options):
        self.options: Options = options
        self.name: str = data.get('Name', row)

        self.source: str = data.get_if("Source", row)
        self.variation: str = data.get_if("Variation", row)
        if self.variation == 'NA':
            self.variation = ''

        self.diy: bool = data.get_bool_if("DIY", row)

        self.body_customize: bool = False
        self.pattern_customize: bool = False
        self.pattern: str = ''

    # Returns the written name with its variation
    # Ex: 'acid washed jacket black'
    def get_written_name(self) -> str:
        return get_written_name(self.name + " " + self.variation)

    # No condition by default
    def condition(self) -> bool:
        return self.options.condition(self)


Condition: Type = Callable[[DataRow], bool]
