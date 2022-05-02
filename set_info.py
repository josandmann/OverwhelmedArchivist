# -*- coding:utf-8

from bs4 import BeautifulSoup
from pathlib import Path
import requests
import json
import logging

def extract_all_sets():
    sets_info={}
    url = 'https://www.cardmarket.com/de/Magic/Expansions'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    years = soup.find_all('section', attrs={'class':'expansion-group mb-3'})
    for year in years:
        year_list = []
        yrstr = year.find('h2', attrs={'class':'d-flex justify-content-between mb-0'}).contents[0]
        sets = year.find_all('div', attrs={'class':'set-as-link expansion-row row no-gutters align-items-center py-2'})
        for s in sets:
            set_url = s.attrs['data-url']
            set_name = set_url.split('/')[-1]
            year_list.append({'name':set_name, 'url':set_url})
        sets_info[yrstr] = year_list
    Path('./data/').mkdir(parents=True, exist_ok=True)
    with open('./data/all_sets.json', 'w') as f:
        json.dump(sets_info, f)
        
extract_all_sets()