# -*- coding:utf-8

import json
from pathlib import Path
import price_extractor
import logging
import argparse
import time
import os
import requests
from datetime import date

parser = argparse.ArgumentParser(
    description='Extract card prices from a specific set')
parser.add_argument('-m', '--mode', help='r/run: start scraping sets in queue \ne/edit: edit queue', required=True)
args = vars(parser.parse_args())
print(args)

mode = args.get('mode')
today = str(date.today())

filters= {'seller_country': '7', 'language':'1,3', 'min_condition':'4'}

#queue = []
#with open('queue.json', 'w') as f:
#    json.dump(queue, f)

def scrape_prices(commands):
    if not commands.get('settype') in ['card_sets', 'specials', 'other']:
        print('no set type called {}'.format(commands.get('settype')))
        logging.info('no set type called {}'.format(commands.get('settype')))
    elif not Path('data/' + commands.get('year')).exists():
        print('no info available for {}'.format(commands.get('year')))
        logging.info('no info available for {}'.format(commands.get('year')))
    elif commands.get('setname') != 'all' and not Path(
        'data/{}/{}/{}.json'.format(commands.get('year'), commands.get('settype'), commands.get('setname'))).is_file():
        print('no set named {} of type {} in {}'.format(
            commands.get('setname'),commands.get('settype'),commands.get('year')))
        logging.info('no set named {} of type {} in {}'.format(
            commands.get('setname'),commands.get('settype'),commands.get('year')))
    else:
        if not commands.get('setname') == 'all':
            with open('data/{}/{}/{}.json'.format(
                commands.get('year'), commands.get('settype'), commands.get('setname')), 'r') as f:
                card_set = json.load(f)
            logging.info('scraping {}'.format(commands.get('setname')))
            #print('scraping {}'.format(commands.get('setname')))
            for card in card_set:
                name = card.split('/')[-1]
                rawpath = 'raw/{}/{}/{}/{}/'.format(
                    commands.get('year'), commands.get('settype'), commands.get('setname'), today)
                scrapepath = 'scrapes/{}/{}/{}/{}/'.format(
                    commands.get('year'), commands.get('settype'), commands.get('setname'), today)
                (card, raw) = price_extractor.scrape_card(card, filters, raw=True)
                Path(rawpath).mkdir(parents=True, exist_ok=True)
                if not type(raw)==bool:
                    with open(rawpath+ '{}.txt'.format(name), 'w', encoding='utf-8') as f:
                        f.write(raw)
                Path(scrapepath).mkdir(parents=True, exist_ok=True)
                with open(scrapepath + '{}.json'.format(name), 'w', encoding='utf-8') as f:
                    json.dump(card, f)
        else:
            sets = os.listdir(os.path.join('data', commands.get('year'), commands.get('settype')))
            for card_set in sets:
                setname = card_set[:-5]
                logging.info('scraping {}'.format(setname))
                #print('scraping {}'.format(setname))
                with open('data/{}/{}/{}.json'.format(
                    commands.get('year'), commands.get('settype'), setname), 'r') as f:
                    card_set = json.load(f)
                for card in card_set:
                    name = card.split('/')[-1]
                    rawpath = 'raw/{}/{}/{}/{}/'.format(
                        commands.get('year'), commands.get('settype'), setname, today)
                    scrapepath = 'scrapes/{}/{}/{}/{}/'.format(
                        commands.get('year'), commands.get('settype'), setname, today)
                    (card, raw) = price_extractor.scrape_card(card, filters, raw=True)
                    Path(rawpath).mkdir(parents=True, exist_ok=True)
                    with open(rawpath+ '{}.txt'.format(name), 'w', encoding='utf-8') as f:
                        f.write(raw)
                    Path(scrapepath).mkdir(parents=True, exist_ok=True)
                    with open(scrapepath + '{}.json'.format(name), 'w', encoding='utf-8') as f:
                        json.dump(card, f)

def dialogue():
    print('type "a" to add sets to scrape queue or "drop" to empty the queue')
    inp = input()
    if inp == 'drop':
        print('Are you SURE??? "y" to confirm')
        inp = input()
        if inp == 'y':
            with open('queue.json', 'w') as f:
                json.dump([], f)
            print('queue deleted')
        else:
            print('deletion aborted')
    elif inp == 'a':
        print('type year of set to add to the queue')
        year = input()
        years = os.listdir('data/')
        if not str(year) in years:
            print('year not recognized')
        else:
            print('state settype ("card_sets", "specials", or "other")')
            settype = input()
            if not settype in ['card_sets', 'specials', 'other']:
                print('settype not recognized')
            else:
                print('enter setname or "all" to enqueue all sets of year {} and type {}'.format(
                    year, settype))
                setname = input()
                if setname == 'all':
                    sets = os.listdir('data/{}/{}/'.format(year, settype))
                    with open('queue.json', 'r') as f:
                        queue = json.load(f)
                    for s in sets:
                        queue.append({'year': str(year), 'settype':settype, 'setname':s[:-5]})
                    with open('queue.json', 'w') as f:
                        json.dump(queue, f)
                    print('{} sets enqueued'.format(len(sets)))


if mode == 'e' or mode == 'edit':
    dialogue()
elif mode == 'r' or mode == 'run':
    while True:
        with open('queue.json', 'rb') as f:
            queue = json.load(f)
        if len(queue) <=0:
            print('queue empty')
            break
        else:
            todo = queue[0]
            try:
                print('scraping ' + todo.get('setname'))
                scrape_prices(todo)
                os.system('python scrape_prices.py -y {} -t {} -n {}'.format(
                    todo.get('year'), todo.get('settype'), todo.get('setname')))
                print('successfully scraped ' + todo.get('setname'))
                print('removing from queue')
                with open('queue.json', 'w') as f:
                    json.dump(queue[1:], f)
            except requests.exceptions.Timeout:
                print('connection timeouted. retrying')
                time.sleep(300)
            except requests.exceptions.ConnectionError:
                print('connection error. retrying')
                time.sleep(300)