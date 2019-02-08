#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from bs4 import BeautifulSoup

import html_utils
from anisong import Anisong


MAL_BASE_URL = "https://myanimelist.net"


class Anime():
    """Holds anime informations
    """

    def __init__(self, anime_name, mal_id, anime_page):
        self.anime_name = anime_name
        self.mal_id = mal_id
        self.url = anime_page
        self.get_anisongs_from_anime_page()

    @classmethod
    def from_dict(cls, data_dict):
        """Creates an Anime obj from the data_dict extracted from anime list"""
        anime_obj = cls(data_dict['anime_title'],
                        data_dict['anime_id'],
                        data_dict['anime_url'])
        return anime_obj

    def get_anisongs_from_anime_page(self):
        """Get additional informations like openings and endings list
            from the anime's MAL page"""
        self.songs = list()
        content = html_utils.get_content_from_url(MAL_BASE_URL + self.url)
        parsed_html = BeautifulSoup(content, "lxml")
        while "Too Many Requests" in parsed_html.body.text:
            print("WARNING: Too many requests. Retrying in 3s...")
            time.sleep(3)
            content = html_utils.get_content_from_url(MAL_BASE_URL + self.url)
            parsed_html = BeautifulSoup(content, "lxml")

        for song_class in ['opnening', 'ending']:
            songs_html = parsed_html.body.find('div',
                                               attrs={'class': song_class})
            if not songs_html:
                print("No {0} for {1}".format(song_class,
                                              self.anime_name.encode('utf-8')))
            else:
                for song_html in songs_html.find_all('span'):
                    song = Anisong.from_mal(song_html.text, song_class)
                    song.anime = self
                    self.songs.append(song)

    def __repr__(self):
        """<MAL ID, anime name>"""
        return "Anime <{0}, {1}>".format(self.mal_id, self.anime_name)


def dump_to_tsv(output_file, animes, file_to_update=None,
                songs_from_library=None):
    """Dump the informations of animes into an exportable TSV file

    Args:
        output_file (str): Output file
        animes (list of Anime): Anime from which to get infos
        file_to_update (str): File processed by a previous
            instance of this program. If set, this function will add
            the content of file_to_update at the beginning of
            output_file without its headers
    """
    content = ["Checked\tAnime title\tSong type\tSong number\t"
               "Song\tArtist/Group\tUsed in"]

    # Add the content of file_to_update to content if the header is valid
    if file_to_update:
        with open(file_to_update) as f:
            file_content = f.readlines()
        if file_content[0].strip() != content[0]:
            print("WARNING: Headers from the file to update are different"
                  " from the actual one."
                  " Program won't add the content of the file to update.")
        else:
            file_content = [x.strip() for x in file_content]
            content += file_content[1:]
            if songs_from_library:
                for i, tsv_entry in enumerate(content[1:]):
                    song_from_tsv = Anisong.from_tsv_entry(tsv_entry)
                    if song_from_tsv in songs_from_library:
                        tsv_entry = tsv_entry.replace('FALSE', 'TRUE', 1)
                        content[i + 1] = tsv_entry

    for anime_obj in animes:
        for song in anime_obj.songs:
            song_data = {'title': anime_obj.anime_name,
                         'song_nb': song.number,
                         'song_type': song.type,
                         'songname': song.title,
                         'eps': song.used_in_eps or '-',
                         'artist': song.artist or '?'}
            entry = ("FALSE\t{title}\t{song_type}\t{song_nb}"
                     "\t{songname}\t{artist}\t{eps}".format(**song_data))
            if song in songs_from_library:
                entry = entry.replace('FALSE', 'TRUE', 1)
            content.append(entry)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
