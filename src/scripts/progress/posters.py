from typing import List

from scripts.item.villagerdb import get_all_user_items
from scripts.util.io import write_input_json_file, read_json_file
from scripts.util.user import posters_user, wishlist_user

posters_filename = "all-posters.txt"


# TODO: removed search stuff -- use sheet instead
def get_all_villagers() -> List[str]:
    # villagers = get_all_searchable_items('villagers/', '')  # type: List[SearchItem]
    # return [villager.item_name for villager in villagers]
    return []


# TODO see above
def get_all_searchable_items(param, param1):
    return [param, param1]


def get_missing_npcs():
    all_posters = get_all_posters()

    # Get a list of all villagers and remove their posters from list -- only NPCs should remain
    villagers = get_all_villagers()
    for villager in villagers:
        if villager == "O'Hare":
            villager = "O'hare"
        if villager == "T-Bone":
            villager = "T-bone"

        poster_name = villager + "'s Poster"
        assert poster_name in all_posters
        all_posters.remove(poster_name)

    # Only NPC posters remain
    all_posters.sort()
    write_input_json_file("npc-posters.txt", all_posters)

    # Get a list of all posters the user already has and remove any on the npc posters list
    user_posters = get_all_user_items(posters_user)
    for poster in user_posters:
        if poster.item_name in all_posters:
            all_posters.remove(poster.item_name)

    if len(all_posters) > 0:
        print("Missing NPCs:", all_posters)


def get_all_posters() -> List[str]:
    # Try to read posters from previous lookup
    all_posters = read_json_file(posters_filename, default=[])

    # Otherwise, get all poster via search (ignore Study Poster because no...)
    if len(all_posters) == 0:
        search_items = get_all_searchable_items('search/', '&q=poster')
        for item in search_items:
            if item.item_name != "Study Poster":
                all_posters.append(item.item_name)

        all_posters.sort()
        write_input_json_file(posters_filename, all_posters)

    return all_posters


# Posters and wishlist lists should be mutually exclusive and have all the posters between them
def check_posters():
    all_posters = get_all_posters()

    user_posters = get_all_user_items(posters_user)
    wishlist_posters = get_all_user_items(wishlist_user)

    num_obtained = len(user_posters)
    num_needed = len(wishlist_posters)
    total_posters = len(all_posters)

    print("Posters:", num_obtained, num_needed, total_posters, "\n")
    assert num_obtained + num_needed == total_posters

    for poster in user_posters:
        assert poster.item_name in all_posters
        all_posters.remove(poster.item_name)

    assert len(all_posters) == len(wishlist_posters)
    for poster in wishlist_posters:
        assert poster.item_name in all_posters
        all_posters.remove(poster.item_name)

    assert len(all_posters) == 0
