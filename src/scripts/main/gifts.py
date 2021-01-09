from typing import List, Dict

from scripts.item.variations import get_item_variation
from scripts.util.io import read_file, ac_folder


def print_gift_groups(*gift_names: str):
    gifts_line: List[str] = read_file("gifts.txt", file_path=ac_folder)
    all_gifts: Dict[str, List[str]] = {}
    current_villager = ""
    for line in gifts_line:
        if line.endswith(":"):
            current_villager = line.removesuffix(":").strip()
            assert current_villager not in all_gifts
            all_gifts[current_villager] = []
        elif line != "":
            assert line.startswith("-") or line.startswith("+")
            line = line.removeprefix("-").removeprefix("+").strip()
            all_gifts[current_villager].append(line)

    # item_name -> variation_name -> villager_names
    gift_map: Dict[str, Dict[str, List[str]]] = {}
    for villager in all_gifts:
        for gift_name in all_gifts[villager]:
            key_pair: (str, str) = get_item_variation(gift_name)
            if not key_pair:
                print("COULD NOT FIND A KEY PAIR VARIATION FOR " + gift_name + " (" + villager + ")")
                continue
            item_name = key_pair[0]
            variation_name = key_pair[1]
            if item_name not in gift_map:
                gift_map[item_name] = {}

            variation_map = gift_map[item_name]
            if variation_name not in variation_map:
                variation_map[variation_name] = []
            variation_map[variation_name].append(villager)

    if len(gift_names) == 0:
        gift_names = gift_map.keys()

    for gift_name in gift_names:
        if gift_name in gift_map:
            print(gift_name)
            variation_map = gift_map[gift_name]
            for variation in variation_map:
                villagers = variation_map[variation]
                print("\t", variation, "-", len(villagers), villagers)
        else:
            print("No matches found for " + gift_name)


if __name__ == '__main__':
    print_gift_groups()
