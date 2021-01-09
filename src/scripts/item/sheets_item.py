from typing import List, Type, Callable

from scripts.util.sheets import Data
from scripts.util.util import get_written_name


class DataRow:
    def __init__(self, data: Data, row: List[str]):
        self.name: str = data.get('Name', row)

        self.source: str = data.get_if("Source", row)
        self.variation: str = data.get_if("Variation", row, True)
        self.diy: bool = data.get_bool_if("DIY", row)
        self.catalog: str = data.get_if('Catalog', row)

        self.body_customize: bool = data.get_bool_if("Body Customize", row)
        self.pattern_customize: bool = data.get_bool_if("Pattern Customize", row)
        self.pattern: str = data.get_if("Pattern", row, True)

        self.event: str = data.get_if('Season/Event', row)
        self.availability: str = data.get_if("Seasonal Availability", row)
        self.seasonality: str = data.get_if("Seasonality", row)

        # Can only customize a pattern if it exists
        # Patterns only exist to be customized so these cannot exist without the other
        assert self.pattern_customize == (self.pattern != "")

        # If you can customize the body, then there MUST be separate variations for the body
        # However, unlike pattern, body variations CAN exist without customization
        assert not (self.body_customize and self.variation == "")

    # Returns the written name with its variation
    # Ex: 'acid washed jacket black'
    def get_written_name(self) -> str:
        return get_written_name(self.name + " " + self.variation)


Condition: Type = Callable[[DataRow], bool]
accept_all: Condition = lambda row: True
