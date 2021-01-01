import json

import requests
from lxml import html
from typing import List


class SearchItem:
    def __init__(self, item):
        self.item_name = item.get('name')
        self.extension = item.get('url')


def get_all_searchable_items(extension: str, extra_args: str) -> List[SearchItem]:
    search_items = []  # type: List[SearchItem]

    # Will be updated to actual value on the first iteration
    total_pages = 1000

    # Go through each page to check each item
    page_num = 1
    while page_num <= total_pages:
        # Ex: https://villagerdb.com/search/page/1?game=nh&q=poster
        # Ex: https://villagerdb.com/items/furniture/page/1?game=nh&tag=Not%20Craftable
        page = requests.get('https://villagerdb.com/' + extension
                            + 'page/' + str(page_num) + '?game=nh' + extra_args)
        tree = html.fromstring(page.text)
        entity_browser = tree.xpath("//div[@id='entity-browser']")[0]
        page_data = json.loads(entity_browser.get('data-initial-state'))

        # Update total_pages to actual value
        total_pages = page_data.get('totalPages')
        page_num += 1

        items = page_data.get('results')
        for item in items:
            search_items.append(SearchItem(item))

    return search_items
