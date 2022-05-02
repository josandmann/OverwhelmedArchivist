# -*- coding:utf-8

import json
from pathlib import Path
import cards_in_each_set
import logging
import argparse
import time
import os

parser = argparse.ArgumentParser(
    description='List scrapable sets in cathegory')
parser.add_argument('-y', '--year', help='year from which to extract sets', required=True)
parser.add_argument('-t', '--settype', help='card_sets, special, or other', default='card_sets')
args = vars(parser.parse_args())

for s in os.listdir('data/{}/{}/'.format(args.get('year'), args.get('settype'))):
    print(s)