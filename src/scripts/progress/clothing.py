from typing import List

from scripts.progress.progress import update_progress
from scripts.util.user import clothing_user
from scripts.item.villagerdb import get_all_variations

clothing_filename = "clothing.txt"
clothing_progress_filename = "clothing_progress.txt"


def get_variations(extension: str, user_variations: List[str]) -> List[str]:
    # List of all variations
    variations: List[str] = get_all_variations(extension)

    if len(variations) <= 1:
        assert user_variations == [""]
        return [""]

    # Make sure each user variation is valid
    for variation in user_variations:
        assert variation in variations

    return variations


def check_clothing():
    update_progress(clothing_user, clothing_filename, clothing_progress_filename, get_variations)
