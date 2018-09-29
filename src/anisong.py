#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class Anisong():
    """Holds infos about an anime song"""

    # Lazy loaded in Anisong.get_re_apparition_eps()
    re_apparition_eps = None

    def __init__(self, anisong_text, anisong_type):
        self._full_text = anisong_text
        self.type = self.get_anisong_type(anisong_type)
        self.number = self.get_song_number(anisong_text)
        self.apparition_eps = self.get_apparition_eps(anisong_text)
        self.title = self.get_title(anisong_text)

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
        if ':' in anisong_text:
            title = anisong_text.split(':', 1)[1]
        else:
            title = anisong_text

        # Clean episode of apparition of anisong
        if self.apparition_eps:
            title = title.replace('({})'.format(self.apparition_eps), '')

        return title.strip()

    def get_apparition_eps(self, anisong_text):
        """Get the episodes where the anisong appeared

        Args:
            anisong_text (str): Anisong text (from MAL anime page)

        Returns:
            str: Episodes of apparition. Note that the returned value
                doesn't have a specific format since MAL doesn't format it.
                See the tests for concrete examples.
        """
        re_apparition_eps = self.get_re_apparition_eps()
        match = re_apparition_eps.search(anisong_text)
        if match:
            return match.group(0).strip('()')
        return None

    def get_re_apparition_eps(self):
        """Checks if Anisong.re_apparition_eps is initialized.
        If not, initialize it, then return it
        """
        if not Anisong.re_apparition_eps:
            Anisong.re_apparition_eps = re.compile(
                r"\([^\(\)]*eps* \d+(-\d+)*.*\)")
        return Anisong.re_apparition_eps
