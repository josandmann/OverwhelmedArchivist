# -*- coding: utf-8

from bs4 import BeautifulSoup
import requests
import logging
import json

def _extract_seller_name(row_element):
    seller = row_element.find('span', attrs={'class':'d-flex has-content-centered mr-1'})
    return seller.a.text

def _extract_seller_country(row_element):
    seller_info = row_element.find('span', attrs={'class':'icon d-flex has-content-centered mr-1'})
    return seller_info.attrs['title'].split()[-1]

def _extract_sales(row_element):
    sales_info = row_element.find('span', attrs={'class':'badge d-none d-sm-inline-flex has-content-centered mr-1 badge-faded sell-count'})
    sales = sales_info['title'].split()
    return [sales[0], sales[3]]

def _extract_card_condition(row_element):
    prod_attrs = row_element.find('div', attrs={'class':'product-attributes col'})
    quality_info = prod_attrs.find('span', attrs={'class':'badge'})
    return quality_info.text

def _extract_card_language(row_element):
    prod_attrs = row_element.find('div', attrs={'class':'product-attributes col'})
    lang = prod_attrs.find('span', attrs={'class':'icon mr-2'})
    return lang.attrs['data-original-title']

def _extract_price(row_element):
    prices = row_element.find('div', attrs={'class':'price-container d-none d-md-flex justify-content-end'})
    return float(prices.text.split()[0].replace('.','').replace(',','.'))

def _extract_stock_amount(row_element):
    available = row_element.find('div', attrs={'class':'amount-container d-none d-md-flex justify-content-end mr-3'})
    return available.text

def _extract_offers(rows):
    offers = [{'seller_info': { 'name':_extract_seller_name(row),
                                'country':_extract_seller_country(row),
                                'total_sales':_extract_sales(row)[0],
                                'cards_in_stock':_extract_sales(row)[1]},
              'card_info': {'condition':_extract_card_condition(row), 'language':_extract_card_language(row)},
              'offer_info': {'price':_extract_price(row), 'amount':_extract_stock_amount(row)}}
             for row in rows]
    return offers

def scrape_card(c_inf, filt, raw=False):
    url = 'https://www.cardmarket.com' + c_inf
    logging.info('card url: {}'.format(url))
    query = '?'
    for key in filt:
        value = filt.get(key)
        if value != '' or value != False:
            if key == 'seller_country':
                query = query + 'sellerCountry={}&'.format(value)
            elif key == 'language':
                query = query + 'language={}&'.format(value)
            elif key == 'min_condition':
                query = query + 'minCondition={}&'.format(value)
            elif key == 'foil' and value == 'Y':
                query = query + 'isFoil={}'.format(value)
    logging.info('extracting data from '+ url + query)
    page = requests.get(url+query)
    logging.info(page.status_code)
    if not page.ok:
        logging.info('invalid url. Skipping...')
        return (False, False)
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        table_rows = soup.find_all('div', attrs={'class': 'row no-gutters article-row'})
        offers = _extract_offers(table_rows)
        if raw:
            return (offers, page.text)
        else:
            return (offers, False)