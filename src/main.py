#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

from PySide2 import QtWidgets

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
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    main_widget = main_window.MainWindow()
    main_widget.setupUi(mw)
    main_widget.model.loadFromDatabase()

    mw.showMaximized()
    return_value = app.exec_()
    main_widget.saveToDatabase()
    sys.exit(return_value)


if __name__ == '__main__':
    main()
