#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import animelist


def main(username=None):
    if not username:
        username = input("Enter MAL username: ")
    user_animelist = animelist.AnimeList(username)
    animes = user_animelist.get_list_of_animes()
    print(animes)
    # print(user_animelist.content)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        main()
