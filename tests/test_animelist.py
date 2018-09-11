import os
import unittest

from unittest.mock import patch

import env  # noqa
from animelist import AnimeList
from animelist import MalStatusNamespace


TEST_XML_FILE = os.path.dirname(__file__) + '/samples/animelist.xml'


class TestAnimeList(unittest.TestCase):
    def test_exclude_animes_by_status(self):
        TITLE_WATCHING = 'Title watching'
        TITLE_PTW = 'Title plan to watch'
        TEST_ANIME_DICT = {
            'anime_title': TITLE_WATCHING,
            'anime_id': '31',
            'anime_url': '/anime/31',
            'anime_status': MalStatusNamespace.watching
        }

        anime_list_obj = AnimeList(TEST_XML_FILE)
        anime_list_obj.parser.anime_data.append(TEST_ANIME_DICT)

        TEST_ANIME_DICT = dict(TEST_ANIME_DICT)
        TEST_ANIME_DICT['anime_title'] = TITLE_PTW
        TEST_ANIME_DICT['anime_status'] = MalStatusNamespace.ptw
        anime_list_obj.parser.anime_data.append(TEST_ANIME_DICT)

        self.assertEqual(len(anime_list_obj.parser.anime_data), 2)

        anime_list_obj.exclude_animes_by_status(MalStatusNamespace.completed)
        self.assertEqual(len(anime_list_obj.parser.anime_data), 2)

        anime_list_obj.exclude_animes_by_status(MalStatusNamespace.ptw)
        self.assertEqual(len(anime_list_obj.parser.anime_data), 1)
        self.assertEqual(anime_list_obj.parser.anime_data[0]['anime_title'],
                         TITLE_WATCHING)

        anime_list_obj.parser.anime_data.append(TEST_ANIME_DICT)
        self.assertEqual(len(anime_list_obj.parser.anime_data), 2)

        anime_list_obj.exclude_animes_by_status(MalStatusNamespace.watching)
        self.assertEqual(len(anime_list_obj.parser.anime_data), 1)
        self.assertEqual(anime_list_obj.parser.anime_data[0]['anime_title'],
                         TITLE_PTW)


if __name__ == '__main__':
    unittest.main()
