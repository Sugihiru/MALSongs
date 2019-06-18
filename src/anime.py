#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from bs4 import BeautifulSoup

import html_utils
import anisong


MAL_BASE_URL = "https://myanimelist.net"


class Anime():
    """Holds anime informations
    """

    def __init__(self, anime_name, mal_id=None, anime_url=None, season=None):
        self.anime_name = anime_name
        self.mal_id = mal_id
        self.url = anime_url
        self.season = season
        if self.url:
            self.get_infos_from_anime_page()
        else:
            self.songs = None

    @classmethod
    def from_dict(cls, data_dict):
        """Creates an Anime obj from the data_dict extracted from anime list"""
        anime_obj = cls(data_dict['anime_title'],
                        data_dict['anime_id'],
                        data_dict['anime_url'])
        return anime_obj

    def get_infos_from_anime_page(self):
        """Get additional informations like openings and endings list,
        season informations, from the anime's MAL page"""
        self.songs = list()
        content = html_utils.get_content_from_url(MAL_BASE_URL + self.url)
        parsed_html = BeautifulSoup(content, "lxml")
        while "Too Many Requests" in parsed_html.body.text:
            print("WARNING: Too many requests. Retrying in 3s...")
            time.sleep(3)
            content = html_utils.get_content_from_url(MAL_BASE_URL + self.url)
            parsed_html = BeautifulSoup(content, "lxml")

        season_html = parsed_html.body.find(
            "span", attrs={"class": "information season"})
        if not season_html:
            self.season = None
        else:
            self.season = season_html.text

        for song_class in ['opnening', 'ending']:
            songs_html = parsed_html.body.find('div',
                                               attrs={'class': song_class})
            if not songs_html:
                print("No {0} for {1}".format(song_class,
                                              self.anime_name.encode('utf-8')))
            else:
                for song_html in songs_html.find_all('span'):
                    song = anisong.Anisong.from_mal(song_html.text,
                                                    song_class)
                    song.anime = self
                    self.songs.append(song)

    def __repr__(self):
        """<MAL ID, anime name>"""
        return "Anime <{0}, {1}>".format(self.mal_id, self.anime_name)
