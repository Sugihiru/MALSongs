#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

from PySide2 import QtWidgets

# import animelist
# import anime
# import song_library
from ui import main_window


def parse_args():
    parser = argparse.ArgumentParser(description="Get the list of"
                                     " anime OP and ED from"
                                     " exported XML extracted from MAL.")

    parser.add_argument("--xml",
                        required=True,
                        help="Get data from XML exported MyAnimeList list")
    parser.add_argument("--include-ptw",
                        action="store_true",
                        help="Include Plan To Watch animes")
    parser.add_argument("--update",
                        help="Update the .tsv passed as argument"
                        " instead of creating a new one")
    parser.add_argument("--song-library",
                        action="append",
                        help="Scan the directory passed as parameter and"
                        " set Checked to True if a song is present in"
                        " the directory passed as parameter")
    args = parser.parse_args()

    return args


def main(username=None):
    # args = parse_args()
    # songs_from_library = \
    #     song_library.get_all_songs_from_library(args.song_library)

    # user_animelist = animelist.AnimeList(args.xml,
    #                                      include_ptw=args.include_ptw,
    #                                      exclude_animes_from_file=args.update)
    # print("Animes to process: {0}".format(len(user_animelist.anime_data)))
    # user_animes = user_animelist.get_list_of_animes()

    # anisongs = list()
    # for user_anime in user_animes:
    #     anisongs += user_anime.songs

    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    main_widget = main_window.MainWindow()
    main_widget.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())

    # anime.dump_to_tsv('anisongs.tsv', user_animes,
    #                   args.update,
    #                   songs_from_library=songs_from_library)


if __name__ == '__main__':
    main()
