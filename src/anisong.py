#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Anisong():
    """Holds infos about an anime song"""

    def __init__(self, anisong_text, anisong_type):
        self._full_text = anisong_text
        self.type = self.get_anisong_type(anisong_type)
        self.number = self.get_song_number(anisong_text)
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
            int: Number of the song
                Note: If the song has no number, it is set to 1 by default
        """
        if anisong_text.startswith('#') and ':' in anisong_text:
            song_nb = anisong_text.split(':')[0]
            song_nb = song_nb.strip('#')
            return int(song_nb)
        return 1

    def get_title(self, anisong_text):
        """Get the song title without additional infos
            like its number or its episode apparitions

        Args:
            anisong_text (str): Anisong text (from MAL anime page)

        Returns:
            str: Stripped and cleaned title of the anisong
        """
        if ':' in anisong_text:
            title = anisong_text.split(':', 1)[1]
        else:
            title = anisong_text
        # Avoid CSV problems, maybe a better solution should be found later
        title = title.replace(',', ';')
        return title.strip()
