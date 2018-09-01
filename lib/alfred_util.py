#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Library for alfred utility functions
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
from collections import namedtuple

AlfredItem = namedtuple('AlfredItem', ['arg', 'uid', 'title', 'subtitle', 'icon'])

def get_fuzzy_filter_regex(filter):
     # loose filtering with typed stuff
    pattern = "^.*"
    if filter:
        for c in filter:
            pattern += re.escape(c) + ".*"
    pattern += "$"
    result = re.compile(pattern, re.I)
    return result

def get_icon(name):
    # someday, it would be awesome to have all the clock time images to closely match the current time
    ico = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../images/" + name)
    return ico

def generate_items_xml(alfred_items):
    xml_items = []
    for item in alfred_items:
        x = '<item arg="{}" uid="{}">\n'.format(item.arg, item.uid)
        x += '  <title>{}</title>\n'.format(item.title) if item.title else ""
        x += '  <subtitle>{}</subtitle>\n'.format(item.subtitle) if item.subtitle else ""
        x += '  <icon>{}</icon>\n'.format(item.icon) if item.icon else ""
        x += '</item>\n'
        xml_items.append(x)

    result = (
        '<?xml version="1.0"?>\n'
        '<items>\n' + "\n".join(xml_items) + '\n</items>'
    )
    return result
