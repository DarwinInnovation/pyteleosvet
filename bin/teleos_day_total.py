#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'richardm'

import logging
import sys
import pyteleosvet
import datetime
import argparse
import dateutil.parser

parser = argparse.ArgumentParser(description="Day totals from Teleos")
parser.add_argument('-c', '--config', default='teleos.json', help='Path to JSON file containing database information')
parser.add_argument('--delta', default=0, type=int, help='Difference from stated date (so -1 for yesterday')
parser.add_argument('-d', '--date', help='Date to total')
args = parser.parse_args()

logging.basicConfig(level=logging.WARN)


def teleos_day_total():
    pyteleosvet.init(args.config)

    if args.date is not None:
        date = dateutil.parser.parse(args.date, dayfirst=True).date()
    else:
        date = datetime.date.today()

    date = date + datetime.timedelta(days=args.delta)

    figures = pyteleosvet.DayFigures(date).get()

    print(figures)

    return 0


if __name__ == '__main__':
    retval = 0

    try:
        retval = teleos_day_total()
    except Exception:
        logging.exception("Critical exception raised")

        retval = 1

    sys.exit(retval)
