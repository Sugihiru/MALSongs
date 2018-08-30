#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import animelist
import anime


def main(username=None):
    if not username:
        username = input("Enter MAL username: ")
    user_animelist = animelist.AnimeList(username)
    print("Getting animes from MAL anime list...")
    user_animes = user_animelist.get_list_of_animes()
    print("Animes processed: {0}".format(len(user_animes)))
    anime.dump_to_csv('anisongs.csv', user_animes)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        main()
