#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Anime():
    """Holds anime informations
    """

    def __init__(self, anime_name, mal_id):
        self.anime_name = anime_name
        self.mal_id = mal_id

    @classmethod
    def from_dict(cls, data_dict):
        """Creates an Anime obj from the data_dict extracted from anime list"""
        anime_obj = cls(data_dict['anime_title'], data_dict['anime_id'])
        return anime_obj

    def __repr__(self):
        """<MAL ID, anime name>"""
        return "Anime <{0}, {1}>".format(self.mal_id, self.anime_name)
