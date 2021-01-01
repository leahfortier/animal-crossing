from typing import List

from scripts.villagerdb.util import get_written_name


class NookazonItem:
    def __init__(self, line: str):
        # Ex: '1 X Black Accessories Stand'
        self.full_item_name: str = line

        self.is_diy: bool = False
        self.quantity: int = 1

        # Ex: ['1', 'Black Accessories Stand'] or ['Wooden-Block Bench DIY Recipe']
        split = line.split(' X ', 2)

        # Ex: ['Black Accessories Stand', 'Accessories Stand Black', 'Stand Black Accessories']
        # Ex: ['Wooden-Block Bench']
        self.potential_names: List[str] = []

        if len(split) == 1:
            # No quantity for item -- should be a DIY
            self.is_diy = True
            self.potential_names.append(split[0].removesuffix(' DIY Recipe').strip())
        else:
            if split[0] != '1':
                self.quantity = int(split[0])
            self.potential_names = get_rotated_names(split[1], True)

        # Ex: 'Black Accessories Stand' or 'Wooden-Block Bench'
        self.base_name: str = self.potential_names[0]

    # Ex: Accessories Stand (Black) -> accessories stand black
    def get_written_name(self) -> str:
        return get_written_name(self.full_item_name)

    def print_base_name(self):
        base_name = get_written_name(self.base_name)
        if len(self.potential_names) > 1 and not ends_with_any(base_name, "wall", "flooring", "tile", "umbrella"):
            base_name = self.potential_names[1]

        print(get_written_name(base_name))


def read_nookazon_file(file_lines: List[str], username: str) -> List[NookazonItem]:
    items: List[NookazonItem] = []
    prev_line: str = ''
    for line in file_lines:
        if line.strip() == username and not prev_line.endswith('following'):
            items.append(NookazonItem(prev_line))
        prev_line = line.strip()
    return items


# Ex: 'Black Accessories Stand' -> ['Black Accessories Stand', 'Accessories Stand Black', 'Stand Black Accessories']
def get_rotated_names(name: str, front_variation=False) -> List[str]:
    mod_name = get_written_name(name.replace("-", "*"))
    name = get_written_name(name)
    if "mom's" in name:
        index = name.find("mom's")
        return [name[index:] + ' ' + name[:index].strip()]

    names = [name]

    # Join sections that clearly belong together (eg: yellow & red, light blue)
    # '&' is only ever part of a variation name so everything before it is part of the variation
    for common_pair in ['&', 'or', 'berry red', 'light', 'moss green', 'navy blue', 'rose red', 'ruby red']:
        if ' ' + common_pair + ' ' in ' ' + mod_name + ' ':
            mod_name = mod_name.replace(common_pair, common_pair.replace(" ", "*"), 1)
    if front_variation:
        mod_name = replace_before(mod_name, '&', ' ', '*')
        mod_name = replace_before(mod_name, '*or*', ' ', '*')
    mod_name = mod_name.strip(' *')

    index = -1
    while True:
        index = mod_name.find(' ', index + 1)
        if index == -1:
            break
        names.append(name[index:].strip() + ' ' + name[:index].strip())

    return names


def ends_with_any(s: str, *suffixes: str) -> bool:
    for suffix in suffixes:
        if s.endswith(suffix):
            return True
    return False


def starts_with_any(s: str, *prefixes: str) -> bool:
    for prefix in prefixes:
        if s.startswith(prefix):
            return True
    return False


def replace_before(s: str, sub: str, old: str, new: str) -> str:
    if sub in s:
        index = s.find(sub)
        return s[:index].replace(old, new) + s[index:]
    return s


def replace_after(s: str, sub: str, old: str, new: str) -> str:
    if sub in s:
        index = s.find(sub)
        return s[:index] + s[index:].replace(old, new)
    return s