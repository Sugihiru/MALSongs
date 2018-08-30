#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

import html_utils


MAL_BASE_URL = "https://myanimelist.net"


class Anime():
    """Holds anime informations
    """

    def __init__(self, anime_name, mal_id, anime_page):
        self.anime_name = anime_name
        self.mal_id = mal_id
        self.url = anime_page
        self.get_infos_from_anime_page()

    @classmethod
    def from_dict(cls, data_dict):
        """Creates an Anime obj from the data_dict extracted from anime list"""
        anime_obj = cls(data_dict['anime_title'],
                        data_dict['anime_id'],
                        data_dict['anime_url'])
        anime_obj.get_infos_from_anime_page()
        return anime_obj

    def get_infos_from_anime_page(self):
        """Get additional informations like openings and endings list
            from the anime's MAL page"""
        content = html_utils.get_content_from_url(MAL_BASE_URL + self.url)
        parsed_html = BeautifulSoup(content, "lxml")
        openings_html = parsed_html.body.find('div',
                                              attrs={'class': 'opnening'})
        endings_html = parsed_html.body.find('div',
                                             attrs={'class': 'ending'})

        def add_song_to_list(songs_list, songs_html):
            for song_html in songs_html.find_all('span'):
                songs_list.append(song_html.text)

        self.openings = list()
        add_song_to_list(self.openings, openings_html)
        self.endings = list()
        add_song_to_list(self.endings, endings_html)

    def __repr__(self):
        """<MAL ID, anime name>"""
        return "Anime <{0}, {1}>".format(self.mal_id, self.anime_name)
