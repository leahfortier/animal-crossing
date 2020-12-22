from scripts.villagerdb.clothing import check_clothing
from scripts.villagerdb.furniture import check_furniture
from scripts.villagerdb.mouse import compare_free_stuff
from scripts.villagerdb.posters import check_posters


def check_all():
    check_posters()
    check_furniture()
    check_clothing()


if __name__ == '__main__':
    check_all()
