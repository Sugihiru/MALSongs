#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib.request


def get_content_from_url(url):
    fp = urllib.request.urlopen(url)
    bytes_content = fp.read()
    fp.close()
    return bytes_content.decode("utf8")
