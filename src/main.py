#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import animelist
import anime


def parse_args():
    parser = argparse.ArgumentParser(description="Get the list of"
                                     " anime OP and ED from either"
                                     " MAL user list online or"
                                     " exported XML extracted from MAL.")
    parser.add_argument("-u", "--username",
                        help="Username of the owner of the list to scan")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-x", "--xml",
                       help="Get data from XML exported MyAnimeList list")
    group.add_argument("--online",
                       action="store_true",
                       help="Get data from MAL website directly."
                       " May fail if MAL is unaccessible."
                       " Can only compute 300 animes max because"
                       " of MAL website architecture")
    args = parser.parse_args()

    if not args.xml and not args.online:
        parser.error("Provide at least one method by either using"
                     " --xml [file] or --online")

    return args


def main(username=None):
    args = parse_args()
    if not args.username:
        args.username = input("Enter MAL username: ")
    user_animelist = animelist.AnimeList(args.username,
                                         xml_animelist=args.xml)
    print("Getting animes from MAL anime list...")
    user_animes = user_animelist.get_list_of_animes()
    print("Animes processed: {0}".format(len(user_animes)))
    anime.dump_to_csv('anisongs.csv', user_animes)


if __name__ == '__main__':
    main()
