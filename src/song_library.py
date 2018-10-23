import os
from anisong import Anisong


class SongLibrary():
    def __init__(self, library_dir):
        self.library_dir = library_dir
        self.songs = list()

    def scan_library(self, scan_recursive=False):
        """Scan the library and add songs found in self.songs

        Args:
            scan_recursive (bool, optional):
                Recursively scan directories if set to True
        """
        with os.scandir(self.library_dir) as it:
            for entry in it:
                if scan_recursive and os.path.isdir(entry.path):
                    old_library_dir = self.library_dir
                    self.library_dir = entry.path
                    self.scan_songs(scan_recursive)
                    self.library_dir = old_library_dir
                elif self.is_audio_file(entry.path):
                    song = Anisong.from_file_name(entry.path)
                    self.songs.append(song)

    def is_audio_file(self, filepath):
        """Check whether the file passed as parameter is a valid audio file"""
        MUSIC_FILE_EXT = [".mp3", ".flac", ".ogg", ".wav"]
        _, file_ext = os.path.splitext(filepath)
        return os.path.isfile(filepath) and file_ext in MUSIC_FILE_EXT


def get_all_songs_from_library(song_libraries, scan_recursive=False):
    songs_from_libraries = list()
    for dirpath in song_libraries:
        library = SongLibrary(dirpath)
        library.scan_library(scan_recursive)
        songs_from_libraries += library.songs
    return songs_from_libraries
