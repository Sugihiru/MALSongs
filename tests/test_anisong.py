import os
import unittest

import env  # noqa
from anisong import Anisong


TEST_XML_FILE = os.path.dirname(__file__) + '/samples/animelist.xml'


class AnisongEmptyInit(Anisong):
    """A class inheriting from anisong but with an empty init
    Used for tests cases only"""

    def __init__(self, anisong_text, anisong_type):
        pass


class TestAnisong(unittest.TestCase):
    def test_get_anisong_type(self):
        song = AnisongEmptyInit('', '')
        self.assertEqual(song.get_anisong_type('opnening'),
                         'OP')
        self.assertEqual(song.get_anisong_type('ending'),
                         'ED')

    def test_get_song_number(self):
        song = AnisongEmptyInit('', '')
        songname = '#1: "Answer" by BUMP OF CHICKEN (eps 1-11)'
        self.assertEqual(song.get_song_number(songname), "01")
        songname = '#2: "Sayonara Bystander" by YUKI (eps 12-22)'
        self.assertEqual(song.get_song_number(songname), "02")
        songname = '#02: "Sayonara Bystander" by YUKI (eps 12-22)'
        self.assertEqual(song.get_song_number(songname), "02")
        songname = '#12: "Tenohira" by HERO (eps 138-150)'
        self.assertEqual(song.get_song_number(songname), "12")
        songname = '#R1: "Circle Game" by Galileo Galilei (eps 1-10)'
        self.assertEqual(song.get_song_number(songname), "R1")

    def test_get_title(self):
        song = AnisongEmptyInit('', '')
        song.apparition_eps = 'eps 1-11'
        songname = '#1: "Answer" by BUMP OF CHICKEN (eps 1-11)'
        self.assertEqual(song.get_title(songname),
                         '"Answer" by BUMP OF CHICKEN')
        song.apparition_eps = 'ep 2'
        songname = '"Uzu to Uzu" by NICO Touches the Walls (ep 2)'
        self.assertEqual(song.get_title(songname),
                         '"Uzu to Uzu" by NICO Touches the Walls')
        songname = '#1: "Gunjou Survival" by Mikako Komatsu (eps 1-7, 9-12)'
        song.apparition_eps = 'eps 1-7, 9-12'
        self.assertEqual(song.get_title(songname),
                         '"Gunjou Survival" by Mikako Komatsu')

    def test_get_apparition_eps(self):
        song = AnisongEmptyInit('', '')
        songname = '#1: "Answer" by BUMP OF CHICKEN (eps 1-11)'
        self.assertEqual(song.get_apparition_eps(songname),
                         "eps 1-11")
        songname = '"Uzu to Uzu" by NICO Touches the Walls (ep 2)'
        self.assertEqual(song.get_apparition_eps(songname),
                         "ep 2")
        songname = '#1: "Gunjou Survival" by Mikako Komatsu (eps 1-7, 9-12)'
        self.assertEqual(song.get_apparition_eps(songname),
                         "eps 1-7, 9-12")


if __name__ == '__main__':
    unittest.main()
