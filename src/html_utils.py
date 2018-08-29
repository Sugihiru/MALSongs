#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib.request


def get_content_from_url(url):
    """Get the content of the page from the URL as a string"""
    fp = urllib.request.urlopen(url)
    bytes_content = fp.read()
    fp.close()
    return bytes_content.decode("utf8")
