# -*- coding:utf-8

import json
from pathlib import Path
import cards_in_each_set
import logging
import argparse

logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

parser = argparse.ArgumentParser(description='extract cards from all sets in specified years')
parser.add_argument('-y', '--years', nargs='+', help='one or more years to extract card info from', required=True)
args = vars(parser.parse_args())
print(args)

with open('data/all_sets.json') as f:
    sets_db = json.load(f)
    
#print(sets_db.get('2021'))
for year in args['years']:
    if year in sets_db.keys():
        logging.info('extracting {} sets from {}'.format(len(sets_db.get(year)), year))
        for s in sets_db.get(year):
            set_name = s.get('name')
            print('from {} extracting {}'.format(year, set_name))
            logging.info('from {} extracting {}'.format(year, set_name))
            path = 'data/{}'.format(year)
            Path(path).mkdir(parents=True, exist_ok=True)
            cards = cards_in_each_set.scrape_set_contents(set_name)
            with open(path + '/' + set_name + '.json', 'w') as f:
                json.dump(cards, f)

