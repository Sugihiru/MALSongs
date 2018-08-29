#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from html.parser import HTMLParser

from anime import Anime
import html_utils

MAL_ANIMELIST_BASE_URL = "https://myanimelist.net/animelist/"


class AnimeList():
    def __init__(self, username):
        self.username = username
        self.url = MAL_ANIMELIST_BASE_URL + username
        self.parser = AnimeListHtmlParser()

        self.content = html_utils.get_content_from_url(self.url)

    def get_list_of_animes(self):
        animes = list()
        self.parser.feed(self.content)
        for data in self.parser.anime_data:
            animes.append(Anime.from_dict(data))
        return animes


class AnimeListHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anime_data = list()

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            for attr in attrs:
                if attr[0] == 'data-items':
                    json_data = json.loads(attr[1])
                    for anime_user_info in json_data:
                        self.anime_data.append(anime_user_info)
