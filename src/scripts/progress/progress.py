from typing import List, Dict

from scripts.item.villagerdb import get_user_variations, Item
from scripts.util.io import write_json_file, read_json_file, write_input_json_file, read_json_out_file
from scripts.util.user import UserList
from scripts.util.util import print_items


def get_item_progress(all_variations: List[str], user_variations: List[str]):
    progress = {"total": str(len(user_variations)) + "/" + str(len(all_variations))}

    completed = []
    missing = []
    for variation in all_variations:
        if variation in user_variations:
            completed.append(variation)
        else:
            missing.append(variation)

    if len(missing) > 0:
        progress["completed"] = completed
        progress["missing"] = missing

    return progress


def update_progress(user: UserList, items_filename: str, progress_filename: str, get_variations):
    # Load the variations map so don't need to look up every time
    item_map: Dict[str, List[str]] = read_json_file(items_filename)

    # Holds the variations of items the user has
    user_items: Dict[str, Item] = get_user_variations(user)

    for item_name in user_items:
        # If item not in map yet, load all possible variations of it and store
        if item_name not in item_map:
            item: Item = user_items[item_name]
            item_map[item_name] = get_variations(item.extension, item.variations)

    # Output any new items to same file
    write_input_json_file(items_filename, item_map)

    progress_map = {}
    for item_name in user_items:
        all_variations = item_map[item_name]
        user_variations = user_items[item_name].variations
        progress_map[item_name] = get_item_progress(all_variations, user_variations)

    prev_progress_map = read_json_out_file(progress_filename)

    just_added = []
    just_completed = []
    just_updated = []
    for item_name in progress_map:
        item_progress = progress_map[item_name]
        current_total = item_progress["total"]

        if item_name not in prev_progress_map:
            just_added.append(item_name + " " + current_total)
            continue

        prev_progress = prev_progress_map[item_name]
        if "missing" in prev_progress and "missing" not in item_progress:
            just_completed.append(item_name + " " + current_total)
        elif "completed" in prev_progress and prev_progress["completed"] != item_progress["completed"]:
            just_updated.append(item_name + ": " + prev_progress["total"] + "->" + current_total)

    print_items("Just added!", just_added)
    print_items("Just completed!", just_completed)
    print_items("Newly updated!", just_updated)

    # Write all completed items to separate file
    write_json_file(progress_filename, progress_map)
