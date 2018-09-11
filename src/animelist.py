#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

from anime import Anime


class MalStatusNamespace():
    watching = "Watching"
    completed = "Completed"
    on_hold = "On-Hold"
    dropped = "Dropped"
    ptw = "Plan to Watch"


class AnimeList():
    """Holds info about a user's anime list
    """

    def __init__(self, xml_animelist):
        self.parser = AnimeListXmlParser()
        with open(xml_animelist, 'r') as f:
            self.content = f.read()

    def get_list_of_animes(self, include_ptw=False):
        """Returns a list of Anime
        extracted from the content of the animelist"""
        animes = list()
        self.parser.feed(self.content)
        if not include_ptw:
            self.exclude_animes_by_status(MalStatusNamespace.ptw)

        for data in self.parser.anime_data:
            print(data['anime_title'].encode('utf-8'))
            animes.append(Anime.from_dict(data))
        return animes

    def exclude_animes_by_status(self, excluded_status):
        """Exclude animes from self.parser.anime_data that have the
        status excluded_status
        """
        self.parser.anime_data = list(
            filter(lambda x: x['anime_status'] != excluded_status,
                   self.parser.anime_data))


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
            anime_dict['anime_status'] = anime_xml.find('my_status').text
            self.anime_data.append(anime_dict)
