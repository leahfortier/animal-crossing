from typing import List, Dict, Type, Callable

from scripts.util.sheets import Data
from scripts.util.util import get_written_name


class Options:
    def __init__(self):
        self.has_variations: bool = False
        self.has_source: bool = True
        self.condition: Condition = lambda row: True
        self.options: Dict[str, any] = {}

    def with_variations(self):
        self.has_variations = True
        return self

    def without_source(self):
        self.has_source = False
        return self

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

        self.source: str = data.get_if(options.has_source, "Source", row)
        self.variation: str = data.get_if(options.has_variations, "Variation", row)

        if self.variation == 'NA':
            self.variation = ''

    # Returns the written name with its variation
    # Ex: 'acid washed jacket black'
    def get_written_name(self) -> str:
        return get_written_name(self.name + " " + self.variation)

    # No condition by default
    def condition(self) -> bool:
        return self.options.condition(self)


Condition: Type = Callable[[DataRow], bool]
