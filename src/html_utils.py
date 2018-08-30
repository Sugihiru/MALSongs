#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests


def get_content_from_url(url):
    """Get the content of the page from the URL as a string"""
    r = requests.get(url)
    return r.text
