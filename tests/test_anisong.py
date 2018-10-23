import os
import unittest

import env  # noqa
from anisong import Anisong


TEST_XML_FILE = os.path.dirname(__file__) + '/samples/animelist.xml'


class TestAnisong(unittest.TestCase):
    def test_repr(self):
        song = Anisong()
        song.artist = "Aya Hirano"
        song.title = "God Knows"
        self.assertEqual(song.__repr__(), "'God Knows' by 'Aya Hirano'")

    def test_eq(self):
        song = Anisong()
        song.artist = "Aya Hirano"
        song.title = "God Knows"
        song2 = Anisong()
        song2.artist = "Aya Hirano"
        song2.title = "God Knows"
        self.assertEqual(song, song2)
        song2.artist = "Haruhi Suzumiya"
        self.assertNotEqual(song, song2)

        song2.artist = "Aya Hirano".lower()
        song2.title = "God Knows".lower()
        self.assertEqual(song, song2)

    def test_from_file_name(self):
        filename = "Aya Hirano - God Knows"
        song = Anisong.from_file_name(filename)
        self.assertEqual(song.title, "God Knows")
        self.assertEqual(song.artist, "Aya Hirano")

        filename = "/some/path/YUKI - Flag wo Tateru"
        song = Anisong.from_file_name(filename)
        self.assertEqual(song.title, "Flag wo Tateru")
        self.assertEqual(song.artist, "YUKI")

    def test_from_tsv_entry(self):
        tsv_entry = ('FALSE\tSuzumiya Haruhi no Yuuutsu (2009)\tOP\t'
                     '1\t"Super Driver"\tAya Hirano\t-')
        song = Anisong.from_tsv_entry(tsv_entry)
        self.assertEqual(song.type, "OP")
        self.assertEqual(song.number, "1")
        self.assertEqual(song.title, "Super Driver")
        self.assertEqual(song.artist, "Aya Hirano")
        self.assertEqual(song.used_in_eps, None)

    def test_get_anisong_type(self):
        song = Anisong()
        self.assertEqual(song.get_anisong_type('opnening'),
                         'OP')
        self.assertEqual(song.get_anisong_type('ending'),
                         'ED')

    def test_get_song_number(self):
        song = Anisong()
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
        song = Anisong()
        song.used_in_eps = 'eps 1-11'
        song.artist = 'BUMP OF CHICKEN'
        songname = '#1: "Answer" by BUMP OF CHICKEN (eps 1-11)'
        self.assertEqual(song.get_title(songname),
                         '"Answer"')

        song.used_in_eps = 'ep 2'
        song.artist = 'NICO Touches the Walls'
        songname = '"Uzu to Uzu" by NICO Touches the Walls (ep 2)'
        self.assertEqual(song.get_title(songname),
                         '"Uzu to Uzu"')

        songname = '#1: "Gunjou Survival" by Mikako Komatsu (eps 1-7, 9-12)'
        song.used_in_eps = 'eps 1-7, 9-12'
        song.artist = 'Mikako Komatsu'
        self.assertEqual(song.get_title(songname),
                         '"Gunjou Survival"')

        songname = '"Menimeni Manimani" by Nasuno Takamiya (CV: Kyoko Narumi)'
        song.artist = 'Nasuno Takamiya (CV: Kyoko Narumi)'
        self.assertEqual(song.get_title(songname),
                         '"Menimeni Manimani"')

    def test_get_used_in_eps(self):
        song = Anisong()
        songname = '#1: "Answer" by BUMP OF CHICKEN (eps 1-11)'
        self.assertEqual(song.get_used_in_eps(songname),
                         "eps 1-11")
        songname = '"Uzu to Uzu" by NICO Touches the Walls (ep 2)'
        self.assertEqual(song.get_used_in_eps(songname),
                         "ep 2")
        songname = '#1: "Gunjou Survival" by Mikako Komatsu (eps 1-7, 9-12)'
        self.assertEqual(song.get_used_in_eps(songname),
                         "eps 1-7, 9-12")

    def test_get_artist(self):
        song = Anisong()
        song.used_in_eps = 'eps 1-11'
        songname = '#1: "Answer" by BUMP OF CHICKEN (eps 1-11)'
        self.assertEqual(song.get_artist(songname),
                         "BUMP OF CHICKEN")

        song.used_in_eps = 'ep 2'
        songname = '"Uzu to Uzu" by NICO Touches the Walls (ep 2)'
        self.assertEqual(song.get_artist(songname),
                         'NICO Touches the Walls')

        songname = '#1: "Gunjou Survival" by Mikako Komatsu (eps 1-7, 9-12)'
        song.used_in_eps = 'eps 1-7, 9-12'
        self.assertEqual(song.get_artist(songname),
                         'Mikako Komatsu')

        # Ambiguous
        songname = 'My Dearest by supercell; performed by Koeda'
        self.assertEqual(song.get_artist(songname), None)

        # Unknown
        songname = 'DREAM SOLISTER (Wind Orchestra Ver.)'
        self.assertEqual(song.get_artist(songname), None)

    def test__clean_eps_number(self):
        song = Anisong()
        song.used_in_eps = 'eps 1-11'
        songname = '#1: "Answer" by BUMP OF CHICKEN (eps 1-11)'
        self.assertEqual(song._clean_eps_number(songname),
                         '#1: "Answer" by BUMP OF CHICKEN ')

        song.used_in_eps = 'ep 2'
        songname = '"Uzu to Uzu" by NICO Touches the Walls (ep 2)'
        self.assertEqual(song._clean_eps_number(songname),
                         '"Uzu to Uzu" by NICO Touches the Walls ')

        songname = '#1: "Gunjou Survival" by Mikako Komatsu (eps 1-7, 9-12)'
        song.used_in_eps = 'eps 1-7, 9-12'
        self.assertEqual(song._clean_eps_number(songname),
                         '#1: "Gunjou Survival" by Mikako Komatsu ')


if __name__ == '__main__':
    unittest.main()
