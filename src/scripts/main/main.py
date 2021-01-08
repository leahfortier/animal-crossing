from scripts.item.variations import write_variations, read_variations
from scripts.progress.clothing import check_clothing
from scripts.progress.furniture import check_furniture
from scripts.progress.posters import check_posters


def check_all():
    check_posters()
    check_furniture()
    check_clothing()


if __name__ == '__main__':
    check_all()
    # write_variations()
