#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'richardm'

import logging
import sys
import pyteleosvet
from pyteleosvet.model import *
import datetime
import argparse
import dateutil.parser

parser = argparse.ArgumentParser(description="List the PHPs started on a specific date (today by default).")
parser.add_argument('-d', '--date', help='Date to analyse')
parser.add_argument('-c', '--config', default='teleos.json', help='Path to JSON file containing database information')
parser.add_argument('--delta', default=0, type=int, help='Difference from stated date (so -1 for yesterday')
args = parser.parse_args()

logging.basicConfig(level=logging.WARN)


def teleos_php_today():
    pyteleosvet.init(args.config)

    if args.date is not None:
        date = dateutil.parser.parse(args.date, dayfirst=True).date()
    else:
        date = datetime.date.today()

    date = date + datetime.timedelta(days=args.delta)

    phps = PhpInstance.select(PhpInstance, Animal, Client)\
        .join(Animal)\
        .join(Client)\
        .where(PhpInstance.plan_start_date == date)\
        .order_by(Client.surname)\
        .execute()

    print("PHPs Started on %s"%date)
    for php in phps:
        print("%16s %16s"%(php.client.surname, php.animal.name))

    return 0


if __name__ == '__main__':
    retval = 0

    try:
        retval = teleos_php_today()
    except Exception:
        logging.exception("Critical exception raised")

        retval = 1

    sys.exit(retval)
