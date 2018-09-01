# there are zillions of potential date formats. this isn't for all of them,
# this is for the common ones you may want.
# if there's a particular one you use that is not included, feel free to add it

# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
TIMESTAMP_FORMATS = {
    "yyyymmdd": "%Y%m%d",
    "now": "%Y-%m-%dT%H:%M:%S.%f",
    "today": "%Y-%m-%d",
    "ISO8601": "%Y-%m-%dT%H:%M:%S.%f",
    "U.S. date": "%-m/%-d/%Y",
    "U.S. datetime": "%-m/%-d/%Y %-I:%M:%S %p",
    "U.S. datetime with tz": "%-m/%-d/%Y %-I:%M:%S %p %Z",
    "U.S. datetime with offset": "%-m/%-d/%Y %-I:%M:%S %p %z",
    "long": "%A, %B %-d, %Y @ %I:%M:%S %p",
}
