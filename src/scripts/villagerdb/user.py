# Holds the username and name of the user's list
# Gives the appropriate url for the item's list
class UserList:
    def __init__(self, username: str, list_name: str):
        self.username = username
        self.list_name = list_name

    def get_url(self) -> str:
        return 'https://villagerdb.com/user/' + self.username + '/list/' + self.list_name


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
