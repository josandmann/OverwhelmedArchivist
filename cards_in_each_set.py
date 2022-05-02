# -*- coding:utf-8

from bs4 import BeautifulSoup
import requests
import time
import logging

# TODO: deal with empty sets (contents not yet announced)
def scrape_set_contents(setname):
    cards = []
    url = 'https://www.cardmarket.com/de/Magic/Products/Singles/{}'.format(setname)
    logging.debug('extracting data from url {}'.format(url))
    page = requests.get(url)
    logging.info('request for set {} has status code {}'.format(setname, page.status_code))
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('div', attrs={'class':'table table-striped mb-3'})
    if table == None:
        logging.info('could not extract product Table from {}. Skipping'.format(setname))
        return cards
    body = table.find('div', attrs={'class':'table-body'})
    rows = body.find_all('div', attrs={'class':'col-10 col-md-8 px-2 flex-column align-items-start justify-content-center'})
    for row in rows:
        cards.append(row.a.attrs['href'])
    logging.debug('cards on page 1: {}'.format(len(rows)))
    time.sleep(2)
    i = 2
    while True:
        logging.debug('continuing on page {}'.format(i))
        logging.debug(url + '?site={}'.format(i))
        page = requests.get(url + '?site={}'.format(i))
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('div', attrs={'class':'table table-striped mb-3'})
        if table == None:
            logging.info('could not extract product Table from {} page {}. Skipping'.format(setname, i))
            return cards
        body = table.find('div', attrs={'class':'table-body'})
        rows = body.find_all('div', attrs={'class':'col-10 col-md-8 px-2 flex-column align-items-start justify-content-center'})
        logging.debug(len(rows))
        if len(rows) <1 or i>=15:
            logging.info('{} completed'.format(setname))
            return cards
        else:
            for row in rows:
                cards.append(row.a.attrs['href'])
            i = i+1
            time.sleep(2)
