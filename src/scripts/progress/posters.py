from typing import List

from scripts.analysis.data import get_all_written_names
from scripts.item.sheets_item import Options
from scripts.util.user import posters_user, wishlist_user


def get_all_villagers() -> List[str]:
    return get_all_written_names(["Villagers"], Options().without_source())


def get_all_posters() -> List[str]:
    return get_all_written_names(["Posters"], Options().without_source())


def check_missing_npcs():
    all_posters = get_all_posters()

    # Get a list of all villagers and remove their posters from list -- only NPCs should remain
    villagers = get_all_villagers()
    for villager in villagers:
        poster_name = villager + "'s poster"
        assert poster_name in all_posters
        all_posters.remove(poster_name)

    # Only NPC posters remain
    # Get a list of all posters the user already has and remove any on the npc posters list
    user_posters = posters_user.get_all_written_items()
    for poster in user_posters:
        if poster in all_posters:
            all_posters.remove(poster)

    if len(all_posters) > 0:
        print("Missing NPCs:", all_posters)


# Posters and wishlist lists should be mutually exclusive and have all the posters between them
def check_posters():
    all_posters: List[str] = get_all_posters()

    user_posters: List[str] = posters_user.get_all_written_items()
    wishlist_posters: List[str] = wishlist_user.get_all_written_items()

    num_obtained: int = len(user_posters)
    num_needed: int = len(wishlist_posters)
    total_posters: int = len(all_posters)

    print("Posters:", num_obtained, num_needed, total_posters, "\n")
    assert num_obtained + num_needed == total_posters

    for poster in user_posters:
        assert poster in all_posters
        all_posters.remove(poster)

    assert len(all_posters) == len(wishlist_posters)
    for poster in wishlist_posters:
        assert poster in all_posters
        all_posters.remove(poster)

    assert len(all_posters) == 0
    check_missing_npcs()
