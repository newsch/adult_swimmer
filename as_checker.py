#!/usr/bin/env python3
"""asseenonadultswim.com feed
Compares a cashed list of items to the current list and sends an alert with IFTTT if there are any changes.
"""
from bs4 import BeautifulSoup
import os.path
import pickle
import requests
import yaml
import re
import logging
import pdb


def get_config(config_file_path='config.yaml'):
    with open(config_file_path, 'r') as config_file:
        config_data = yaml.load(config_file)
    return config_data

def send_ifttt_post(first, second, third, event_name, maker_key):
    contents = {}
    contents['value1'] = first
    contents['value2'] = second
    contents['value3'] = third
    requests.post("https://maker.ifttt.com/trigger/{}/with/key/{}".format(event_name, maker_key), data=contents)
    logging.debug('alert sent with contents value1: {} value2:{} value3:{}'.format(first, second, third))

def get_html():
    # TODO: check for bad result
    result = requests.get('http://www.asseenonadultswim.com')
    return BeautifulSoup(result.content, 'html.parser')

class Item(object):
    def __init__(self, title, price, link, sold_out=False):
        self.title = title
        self.price = price
        self.sold_out = sold_out
        self.link = link

    def __str__(self):
        text = '{title}: ${price:,.2f}, Sold Out={sold_out}\n{link}'
        return(text.format(**self.__dict__))

    def __eq__(self, other):
        return self.title == other.title

def get_items(page):
    """Return a list of items from the page"""
    # get featured product
    featured_product_patterns = {
        'title': ['div.featured-product h2'],
        'price': ['span.price'],
        'sold_out': ['span.price'],
        'link': ['a.btn']
        }
    processes = {
        'title': lambda a: a.get_text(),
        'price': lambda a: float(re.search('([\d.]+)', a.get_text(), re.MULTILINE).group(1)),
        'sold_out': lambda a: 'Sold Out' in a.get_text(),
        'link': lambda a: 'http://www.asseenonadultswim.com' + a['href']
        }
    # get raw html for attributes
    raw_feat_attributes = {}
    for attribute, pattern in featured_product_patterns.items():
        raw_feat_attributes[attribute] = page.select_one(*pattern)
    # process raw html into important bits
    # TODO: combine these into a single for loop
    feat_item_attributes = {}
    for attribute, post_process in processes.items():
        feat_item_attributes[attribute] = post_process(raw_feat_attributes[attribute])
    # instantiate list of items and add featured item
    page_items = []
    page_items.append(Item(**feat_item_attributes))
    # get other items
    raw_items = page.find_all('div', {'class': 'product'})
    patterns = {
        'title': ['div.details a .title'],
        'price': ['div.details a span.price'],
        'sold_out': ['div.details a span.price'],
        'link': ['div.details a']
    }
    for raw_item in raw_items:
        # do the same as before but with the rest of the page
        # TODO: combine the below into a single for loop
        raw_item_attributes = {}
        for attribute, pattern in patterns.items():
            raw_item_attributes[attribute] = raw_item.select_one(*pattern)
        item_attributes = {}
        for attribute, post_process in processes.items():
            item_attributes[attribute] = post_process(raw_item_attributes[attribute])
        page_items.append(Item(**item_attributes))
    return page_items

def save_list(data, file_path='list.obj'):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def read_list(file_path='list.obj'):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


# logging
logging.basicConfig(filename='as_checker.log', format='%(asctime)-15s %(levelname)s: %(message)s', level=logging.DEBUG)

# read webhook settings from config file
webhook_config = get_config()['maker_webhook']
send_alert = lambda a: send_ifttt_post(a, '', '', **webhook_config)
# send_ifttt_post('test1', 'test2', 'test3', **webhook_config)
# [print(item) for item in get_items(get_html())]

current_items = get_items(get_html())
added_items = []
removed_items = []

if os.path.isfile('list.obj'):
    logging.info('Old list found')
    old_items = read_list()
    # check for new and updated items
    for item in current_items:
        if item not in old_items:
            logging.debug('New item found')
            logging.debug(item)
            added_items.append(item)
            print(item)
        else:  # find old item and look for changes
            for old_item in old_items:
                if item.title == old_item.title:  # if item already in list
                    if item.price != old_item.price:
                        logging.info('Price changed for item')
                        logging.debug(item)
                    if item.sold_out != old_item.sold_out:
                        if item.sold_out:
                            logging.info('Item sold out!')
                            logging.debug(item)
                        else:
                            logging.info('Item available again!')
                            logging.debug(item)
    # check for removed items
    for item in old_items:
        if item not in current_items:
            logging.debug('Item removed')
            logging.debug(item)
            removed_items.append(item)
    logging.info('{} new item(s) found'.format(len(added_items)))
    logging.info('{} items removed'.format(len(removed_items)))
    # alerts
    if len(added_items) > 0:
        for item in added_items:
            send_alert('New item: {}'.format(item.title))
        if len(added_items) > 3:
            send_alert('{} new item(s) found'.format(len(added_items)))
    logging.info('Saving current list')
else:
    logging.info('No old list found, saving current list')
    send_alert('Started watching, {} items currently available'.format(len(current_items)))
save_list(current_items)
