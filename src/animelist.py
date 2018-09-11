#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

from anime import Anime


class AnimeList():
    """Holds info about a user's anime list
    """

    def __init__(self, xml_animelist):
        self.parser = AnimeListXmlParser()
        self.content = open(xml_animelist, 'r').read()

    def get_list_of_animes(self):
        """Returns a list of Anime
        extracted from the content of the animelist"""
        animes = list()
        self.parser.feed(self.content)
        for data in self.parser.anime_data:
            print(data['anime_title'].encode('utf-8'))
            animes.append(Anime.from_dict(data))
        return animes


class AnimeListXmlParser():
    def __init__(self):
        super().__init__()
        self.anime_data = list()

    def feed(self, content):
        parsed_xml = BeautifulSoup(content, "lxml-xml")
        animes_xml = parsed_xml.find_all('anime')
        for anime_xml in animes_xml:
            anime_dict = dict()
            anime_dict['anime_title'] = anime_xml.find('series_title').text
            anime_dict['anime_id'] = anime_xml.find('series_animedb_id').text
            anime_dict['anime_url'] = ('/anime/' + anime_dict['anime_id'])
            self.anime_data.append(anime_dict)
