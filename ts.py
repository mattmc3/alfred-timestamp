#!/usr/bin/env python

"""
Script that supports outputting a timestamp in the specified format.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys
import os
import re
from datetime import datetime
from dateutil.tz import *
from ts_formats import TIMESTAMP_FORMATS

def item_xml(**kwargs):
    xml = (
        '<item arg="{}" uid="{}">\n'
        '  <title>{}</title>\n'
        '  <subtitle>{}</subtitle>\n'
        '  <icon>{}</icon>'
        '</item>\n'
    ).format(
        kwargs['arg'],
        kwargs['uid'],
        kwargs['title'],
        kwargs['subtitle'],
        kwargs['path'],
    )
    return xml


def get_icon_path():
    # someday, it would be awesome to have all the clock time images to closely match the current time
    ico = os.path.dirname(os.path.abspath(__file__)) + "/images/clock-face-three-oclock_emoji.png"
    return ico

def ts_now(now, query):
    items = []

    # loose filtering with typed stuff
    pattern = "^.*"
    if query:
        for c in query:
            pattern += re.escape(c) + ".*"
    pattern += "$"
    re_query = re.compile(pattern, re.I)

    formats = { k:v for k,v in TIMESTAMP_FORMATS.items()
                if re_query.search(k) }

    for name, timeformat in formats.items():
        timestamp = now.strftime(timeformat)
        title = "{} ({})".format(name, timestamp)
        x = item_xml(uid=name, arg=timestamp,
                     title=title,
                     subtitle="Copy \"{}\" to clipboard".format(timestamp),
                     path=get_icon_path())
        items.append(x)

    xml_items = "\n".join(items)
    output = (
        '<?xml version="1.0"?>\n'
        '<items>\n' + xml_items + '\n</items>'
    )
    print(output)


def main(args):
    if not args.mode:
        if not args.timezone:
            now = datetime.now().replace(tzinfo=tzlocal())
        else:
            # TODO other time zones
            now = datetime.utcnow().replace(tzinfo=tzutc())
        ts_now(now, args.query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="the mode to run the app")
    parser.add_argument("-z", "--timezone", help="the time zone")
    parser.add_argument("-q", "--query", help="filters the alfred results")
    args = parser.parse_args()

    main(args)
