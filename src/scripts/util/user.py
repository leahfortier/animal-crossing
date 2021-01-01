from typing import List


# Holds the username and name of the user's list
# Gives the appropriate url for the item's list
class UserList:
    def __init__(self, username: str, list_name: str):
        self.username = username
        self.list_name = list_name

    def get_url(self) -> str:
        return 'https://villagerdb.com/user/' + self.username + '/list/' + self.list_name

    def get_all_written_items(self) -> List[str]:
        from scripts.item.villagerdb import get_all_user_items
        items = get_all_user_items(self)
        return [item.get_written_name() for item in items]


# Note: Tried to write a parser to read wishlists from nookazon, but it's all behind javascript :/
class NookazonUser(UserList):
    def __init__(self, user_id: str, username: str):
        super().__init__(username, 'wishlist')
        self.user_id = user_id

    def get_url(self) -> str:
        return 'https://nookazon.com/profile/' + self.user_id + '/' + self.list_name

    def get_all_written_items(self) -> List[str]:
        return []


clothing_user = UserList('dragonair', 'clothing')
furniture_user = UserList('dragonair', 'furniture')
craftable_user = UserList('dragonair', 'craftable')
rugs_user = UserList('dragonair', 'rugs')
walls_floors_user = UserList('dragonair', 'walls-and-floors')
posters_user = UserList('dragonair', 'posters')
wishlist_user = UserList('dragonair', 'posters-wishlist')
free_stuff_user = UserList('dragonair', 'free-stuff')

alt_furniture_user = UserList('polygonia', 'owned-furniture')
alt_craftable_user = UserList('polygonia', 'diys-owned')
