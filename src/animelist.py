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

    def __init__(self, xml_animelist, include_ptw=False,
                 exclude_animes_from_file=None):
        self.parser = AnimeListXmlParser()
        with open(xml_animelist, 'r') as f:
            self.content = f.read()
        self.anime_data = self.get_anime_data(include_ptw,
                                              exclude_animes_from_file)

    def get_anime_data(self, include_ptw, exclude_animes_from_file):
        """Get basic data concerning the animes in the animelist

        Returns a dict containing anime_title, anime_id,
        anime_url, anime_status
        """
        self.parser.feed(self.content)
        if not include_ptw:
            self.exclude_animes_by_status(MalStatusNamespace.ptw)

        if exclude_animes_from_file:
            animes_to_exclude = set()
            with open(exclude_animes_from_file, 'r',
                      encoding='utf-8') as f:
                for line in f:
                    animes_to_exclude.add(line.split('\t')[1])
            self.exclude_animes_by_titles(animes_to_exclude)
        return self.parser.anime_data

    def get_list_of_animes(self):
        """Returns a list of Anime
        extracted from the content of the animelist"""
        animes = list()
        for data in self.anime_data:
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

    def exclude_animes_by_titles(self, animes_title_to_exclude):
        """Exclude animes from self.parser.anime_data that are in
        animes_title_to_exclude
        """
        self.parser.anime_data = list(
            filter(lambda x: x['anime_title'] not in animes_title_to_exclude,
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
