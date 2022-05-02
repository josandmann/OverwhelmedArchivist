# -*- coding:utf-8

import json
from pathlib import Path
import cards_in_each_set
import logging
import argparse
import time
import os
from datetime import date
import price_extractor

logging.basicConfig(filename='logs/price_scraper.log', level=logging.INFO)

#parser = argparse.ArgumentParser(
#    description='Extract card prices from a specific set')
#parser.add_argument('-y', '--year', help='year from which to extract sets', default='2021')
#parser.add_argument('-t', '--settype', help='card_sets, special, or other', default='card_sets')
#parser.add_argument('-n', '--setname', help='name of the set to extract', default='all')
#args = vars(parser.parse_args())

#logging.debug(args)
#logging.info(Path('data/'+ args.get('year')).exists())

today = str(date.today())

filters= {'seller_country': '7', 'language':'1,3', 'min_condition':'4'}
logging.info('using default filter {}'.format(filters))

# TODO: add metrics to card info
#def metrics(card):
#    prices = [row.get('offer_info').get('price').astype('float32') for row in card]
#    mets = {}
#    mets[

def scrape_prices(args):
    if not args.get('settype') in ['card_sets', 'specials', 'other']:
        print('no set type called {}'.format(args.get('settype')))
        logging.info('no set type called {}'.format(args.get('settype')))
    elif not Path('data/' + args.get('year')).exists():
        print('no info available for {}'.format(args.get('year')))
        logging.info('no info available for {}'.format(args.get('year')))
    elif args.get('setname') != 'all' and not Path(
        'data/{}/{}/{}.json'.format(args.get('year'), args.get('settype'), args.get('setname'))).is_file():
        print('no set named {} of type {} in {}'.format(
            args.get('setname'),args.get('settype'),args.get('year')))
        logging.info('no set named {} of type {} in {}'.format(
            args.get('setname'),args.get('settype'),args.get('year')))
    else:
        if not args.get('setname') == 'all':
            with open('data/{}/{}/{}.json'.format(
                args.get('year'), args.get('settype'), args.get('setname')), 'r') as f:
                card_set = json.load(f)
            logging.info('scraping {}'.format(args.get('setname')))
            print('scraping {}'.format(args.get('setname')))
            for card in card_set:
                name = card.split('/')[-1]
                rawpath = 'raw/{}/{}/{}/{}/'.format(
                    args.get('year'), args.get('settype'), args.get('setname'), today)
                scrapepath = 'scrapes/{}/{}/{}/{}/'.format(
                    args.get('year'), args.get('settype'), args.get('setname'), today)
                (card, raw) = price_extractor.scrape_card(card, filters, raw=True)
                Path(rawpath).mkdir(parents=True, exist_ok=True)
                with open(rawpath+ '{}.txt'.format(name), 'w', encoding='utf-8') as f:
                    f.write(raw)
                Path(scrapepath).mkdir(parents=True, exist_ok=True)
                with open(scrapepath + '{}.json'.format(name), 'w', encoding='utf-8') as f:
                    json.dump(card, f)
        else:
            sets = os.listdir(os.path.join('data', args.get('year'), args.get('settype')))
            for card_set in sets:
                setname = card_set[:-5]
                logging.info('scraping {}'.format(setname))
                print('scraping {}'.format(setname))
                with open('data/{}/{}/{}.json'.format(
                    args.get('year'), args.get('settype'), setname), 'r') as f:
                    card_set = json.load(f)
                for card in card_set:
                    name = card.split('/')[-1]
                    rawpath = 'raw/{}/{}/{}/{}/'.format(
                        args.get('year'), args.get('settype'), setname, today)
                    scrapepath = 'scrapes/{}/{}/{}/{}/'.format(
                        args.get('year'), args.get('settype'), setname, today)
                    (card, raw) = price_extractor.scrape_card(card, filters, raw=True)
                    Path(rawpath).mkdir(parents=True, exist_ok=True)
                    with open(rawpath+ '{}.txt'.format(name), 'w', encoding='utf-8') as f:
                        f.write(raw)
                    Path(scrapepath).mkdir(parents=True, exist_ok=True)
                    with open(scrapepath + '{}.json'.format(name), 'w', encoding='utf-8') as f:
                        json.dump(card, f)
                        
#scrape_prices(args)
