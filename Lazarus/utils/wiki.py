# -*- coding: utf-8 -*-
from typing import Optional

from requests import get


class WikiPagePreview:
    def __init__(self, title: str, page_id: int, snippet: str=None):
        self.title = title
        self.page_id = page_id
        self.snippet = snippet

    def __repr__(self):
        return f'{self.title} ({self.page_id})'

    def __str__(self):
        return self.title


def get_wiki_snippet(page_id: int) -> Optional[str]:
    req = get(
        'https://witcher.fandom.com/api.php'
        '?action=query'
        '&format=json'
        '&assert=anon'
        '&prop=articlesnippet'
        '&list='
        '&meta='
        '&pageids={}'
        '&artchars=120'.format(str(page_id))
    )
    if req.status_code != 200:
        return None
    res = req.json()
    return res['query']['pages'][str(page_id)]['extract']
