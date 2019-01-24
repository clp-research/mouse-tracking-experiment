'''slurk link generator'''

import random
import configparser
import webbrowser
import time
import requests
import lxml.html

CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
FIREFOX_PATH = 'open -a /Applications/Firefox.app %s'

LINKS_LIST = []

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

# generate random name based on noun and adjective files

#with open('nouns.txt', 'r') as nouns_file:
#    NOUNS = nouns_file.read().splitlines()
#with open('adj.txt', 'r') as adj_file:
#    ADJ = adj_file.read().splitlines()

def insert_names_and_tokens(n_hits):
    '''take html webpage source and generate slurk tokens for players'''
    for item in range(n_hits):
        #full_name = random.choice(ADJ)+"_"+random.choice(NOUNS)
        full_name = "Dr. John A. Zoidberg"
        url = CONFIG['link_generator']['url']
        session = requests.session()
        read_webpage = session.get(url)
        source = lxml.html.document_fromstring(read_webpage.content)
        token = source.xpath('//input[@name="csrf_token"]/@value')[0]
        headers = {'Referer': CONFIG['link_generator']['url']}
        data = {'csrf_token': token, 'room': '1', 'task': '1', 'reuseable': 'y',\
                'source': '{}'.format(full_name)}
        login_token = session.post(url, data=data, headers=headers).text
        if login_token.endswith('<br />'):
            login_token = login_token[:-6]
        uris = CONFIG['login']['url']+'/?name={}&token={}'.format(full_name, login_token)
        LINKS_LIST.append(uris)
    return LINKS_LIST

if __name__ == '__main__':
    GENER_LINKS = insert_names_and_tokens(2)
    #print(GENER_LINKS)
    #webbrowser.get(CHROME_PATH).open(GENER_LINKS[0], new=2)
    #time.sleep(2)
    #webbrowser.get(FIREFOX_PATH).open(GENER_LINKS[1], new=2)
