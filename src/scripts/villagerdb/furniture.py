from typing import List

from scripts.villagerdb.user import furniture_user
from scripts.villagerdb.util import get_all_variations, check_items

items_filename = "items.txt"
completed_filename = "completed.txt"
missing_filename = "missing.txt"
progress_filename = "item_progress.txt"


# Returns a list of the possible variations the item can have
# Filters out irrelevant variations using the user's variation as the default point of reference
# Ex: Beach Towel -> []
# Ex: Electric Guitar -> ["Cherry", "Chic white", ..., "Sunburst"]
def get_variations(extension: str, user_variations: List[str]) -> List[str]:
    # Just use the first variation for the format
    user_variation = user_variations[0]

    # Note: An item that has no orderable variations can still have several data variations, due to customization
    # Not sure of a good way to determine this without user input, so relies on user value having no variation
    if len(user_variations) == 1 and user_variation == '':
        return [""]

    # List of all variations
    variations = get_all_variations(extension)  # type: List[str]

    # Make sure each user variation is valid
    for variation in user_variations:
        assert variation in variations

    # Items that have a default variation -> get all matching variations
    # Ex: 'Baby Chair (Black / Bear)' -> get all other variations that include bear
    if '/' in user_variation:
        # If user includes a slash, then every single variation must include one as well
        assert len([variation for variation in variations if '/' not in variation]) == 0

        # Start from slash and remove ending parenthesis
        # Ex: '/ Bear'
        default_variant = user_variation[user_variation.find('/'):-1]
        variations = [variation for variation in variations if default_variant in variation]
    # Some items may include additional variations of a base color but only use the base in this case
    # Ex: 'Electric Guitar (Cherry)' -> ignore variations such as 'Electric Guitar (Cherry / Chic logo)'
    else:
        variations = [variation for variation in variations if '/' not in variation]

    return variations


def check_furniture():
    check_items(furniture_user, items_filename, progress_filename, get_variations)
