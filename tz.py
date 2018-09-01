#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script that outputs timezones for selection
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
from datetime import datetime
from dateutil.zoneinfo import get_zonefile_instance
from dateutil import tz
from lib.alfred_util import (AlfredItem, get_icon, generate_items_xml,
                             get_fuzzy_filter_regex)

DEPRECATED_TZS = [
    'Australia/ACT',
    'Australia/LHI',
    'Australia/North',
    'Australia/NSW',
    'Australia/Queensland',
    'Australia/South',
    'Australia/Tasmania',
    'Australia/Victoria',
    'Australia/West',
    'Brazil/Acre',
    'Brazil/DeNoronha',
    'Brazil/East',
    'Brazil/West',
    'Canada/Atlantic',
    'Canada/Central',
    'Canada/Eastern',
    'Canada/Mountain',
    'Canada/Newfoundland',
    'Canada/Pacific',
    'Canada/Saskatchewan',
    'Canada/Yukon',
    'CET',
    'Chile/Continental',
    'Chile/EasterIsland',
    'CST6CDT',
    'Cuba',
    'EET',
    'Egypt',
    'Eire',
    'EST',
    'EST5EDT',
    'Etc/Greenwich',
    'Etc/UCT',
    'Etc/Universal',
    'Etc/Zulu',
    'GB',
    'GB-Eire',
    'GMT+0',
    'GMT0',
    'GMT−0',
    'Greenwich',
    'Hongkong',
    'HST',
    'Iceland',
    'Iran',
    'Israel',
    'Jamaica',
    'Japan',
    'Kwajalein',
    'Libya',
    'MET',
    'Mexico/BajaNorte',
    'Mexico/BajaSur',
    'Mexico/General',
    'MST',
    'MST7MDT',
    'Navajo',
    'NZ',
    'NZ-CHAT',
    'Poland',
    'Portugal',
    'PRC',
    'PST8PDT',
    'ROC',
    'ROK',
    'Singapore',
    'Turkey',
    'UCT',
    'Universal',
    # 'US/Alaska',
    # 'US/Aleutian',
    # 'US/Arizona',
    # 'US/Central',
    # 'US/Eastern',
    # 'US/East-Indiana',
    # 'US/Hawaii',
    # 'US/Indiana-Starke',
    # 'US/Michigan',
    # 'US/Mountain',
    # 'US/Pacific',
    # 'US/Pacific-New',
    # 'US/Samoa',
    'WET',
    'W-SU',
    'Zulu',
]


def main(args):
    re_filter = get_fuzzy_filter_regex(args.query)

    utcnow = datetime.now(tz.tzutc())
    zonenames = [z for z in sorted(list(get_zonefile_instance().zones))
                 if z not in DEPRECATED_TZS and re_filter.search(z)]
    items = [AlfredItem(z, z, get_text(utcnow, z),
                        'Select "{}"'.format(z),
                        get_icon("globe-with-meridians_emoji.png"))
             for z in zonenames]
    alfred_xml = generate_items_xml(items)
    # print is how we get the results back to alfred
    print(alfred_xml)


def get_text(utcnow, tzname):
    regional_time = switch_time_zone_from_utc(utcnow, tzname)
    abbr = regional_time.strftime("%Z")
    offset = regional_time.strftime("%z")

    formatted_offset = offset
    if offset.startswith(('+', '-')) and len(offset) == 5:
        formatted_offset = offset[:3] + ':' + offset[3:]
    if offset.startswith(abbr):
        suffix = "({})".format(formatted_offset)
    else:
        suffix = "({} {})".format(formatted_offset, abbr)
    formatted_tzname = tzname.split('/', 1)[1] if '/' in tzname else tzname
    formatted_tzname = formatted_tzname.replace('-', ' ').replace('_', ' ')

    result = regional_time.strftime("%H:%M {} {}").format(formatted_tzname, suffix)
    return result


def switch_time_zone_from_utc(utcnow, tzname):
    regional_time = utcnow.astimezone(tz.gettz(tzname))
    return regional_time


def get_local_time_from_utc(utcnow):
    local = utcnow.astimezone(tz.tzlocal())
    return local


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="filters the alfred results")
    args = parser.parse_args()
    main(args)
