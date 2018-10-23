#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os


class Anisong():
    """Holds infos about an anime song"""

    # Lazy loaded in Anisong.get_re_apparition_eps()
    re_used_in_eps = None

    def __init__(self):
        self.type = None
        self.number = None
        self.used_in_eps = None
        self.artist = None
        self.title = None

    def __repr__(self):
        """Example : "'God Knows' by 'Aya Hirano'". """
        return "'{songname}' by '{artist}'".format(songname=self.title,
                                                   artist=self.artist)

    def __eq__(self, other):
        """Returns True if the song has the same title
        and is sung by the same artist
        """
        return self.artist == other.artist and self.title == other.title

    @classmethod
    def from_mal(cls, anisong_text, anisong_type):
        """Creates an Anisong from MAL informations"""
        obj = cls()
        obj._mal_full_text = anisong_text
        obj.type = obj.get_anisong_type(anisong_type)
        obj.number = obj.get_song_number(anisong_text)
        obj.used_in_eps = obj.get_used_in_eps(anisong_text)
        obj.artist = obj.get_artist(anisong_text)
        obj.title = obj.get_title(anisong_text)
        return obj

    @classmethod
    def from_file_name(cls, filepath):
        """Creates an Anisong from a file name
        By default, it assumes the format '%artist% - %songname%'
        """
        sep = ' - '
        obj = cls()
        filepath = os.path.basename(filepath)
        if sep in filepath:
            split_filepath = filepath.split(sep)
            obj.artist = split_filepath[0]
            obj.title = os.path.splitext(split_filepath[1])[0]
        return obj

    def get_anisong_type(self, anisong_type):
        """Get the shortened type of the anisong.

        Args:
            anisong_type (str): Anisong type (from CSS class)

        Returns:
            str: 'OP' or 'ED'
        """
        songs_types = {'opnening': 'OP',
                       'ending': 'ED'}
        return songs_types[anisong_type]

    def get_song_number(self, anisong_text):
        """Get the song number of the OP/ED

        Args:
            anisong_text (str): Anisong text (from MAL anime page)

        Returns:
            str: Number of the song
                Note: If the song has no number, it is set to "1" by default
        """
        if anisong_text.startswith('#') and ':' in anisong_text:
            song_nb = anisong_text.split(':')[0]
            song_nb = song_nb.strip('#')
            if song_nb.isdigit():
                song_nb = song_nb.zfill(2)
            return song_nb
        return '1'

    def get_title(self, anisong_text):
        """Get the song title without additional infos
            like its number or its episode apparitions

        Args:
            anisong_text (str): Anisong text (from MAL anime page)

        Returns:
            str: Stripped and cleaned title of the anisong
        """

        # Clean anisong number
        if anisong_text.startswith('#') and ':' in anisong_text:
            title = anisong_text.split(':', 1)[1]
        else:
            title = anisong_text

        title = self._clean_eps_number(title)

        # Clean artist
        if self.artist:
            title = title.replace(" by " + self.artist, '')

        return title.strip()

    def get_used_in_eps(self, anisong_text):
        """Get the episodes where the anisong appeared

        Args:
            anisong_text (str): Anisong text (from MAL anime page)

        Returns:
            str: Episodes of apparition. Note that the returned value
                doesn't have a specific format since MAL doesn't format it.
                See the tests for concrete examples.
        """
        re_used_in_eps = self.get_re_apparition_eps()
        match = re_used_in_eps.search(anisong_text)
        if match:
            return match.group(0).strip('()')
        return None

    def get_artist(self, anisong_text):
        """Get the artist or group performing the song

        Args:
            anisong_text (str): Anisong text (from MAL anime page)

        Returns:
            str: Performer of the song, or None if not found/ambiguous case
        """
        separator = " by "
        if anisong_text.count(separator) == 1:
            artist = anisong_text.split(separator)[1]
            return self._clean_eps_number(artist).strip()
        return None

    def _clean_eps_number(self, text):
        """Remove the "used in eps" of the anime from the text

        Args:
            text (str): Text to clean

        Returns:
            str: Clean text without the episodes in which it was used
        """
        if self.used_in_eps:
            return text.replace('({})'.format(self.used_in_eps), '')
        return text

    def get_re_apparition_eps(self):
        """Checks if Anisong.re_used_in_eps is initialized.
        If not, initialize it, then return it
        """
        if not Anisong.re_used_in_eps:
            Anisong.re_used_in_eps = re.compile(
                r"\([^\(\)]*eps* \d+(-\d+)*.*\)")
        return Anisong.re_used_in_eps
