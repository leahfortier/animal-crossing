from typing import List

from scripts.villagerdb.util import get_all_variations, UserList, check_items

clothing_filename = "clothing.txt"
progress_filename = "clothing_progress.txt"

user = UserList('dragonair', 'clothing')


def get_variations(extension: str, user_variations: List[str]) -> List[str]:
    # List of all variations
    variations = get_all_variations(extension)  # type: List[str]

    if len(variations) <= 1:
        assert user_variations == [""]
        return [""]

    # Make sure each user variation is valid
    for variation in user_variations:
        assert variation in variations

    return variations


def check_clothing():
    check_items(user, clothing_filename, progress_filename, get_variations)
