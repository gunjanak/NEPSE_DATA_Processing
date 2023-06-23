#this file will scrape merolagani site and scrape the symbols of all the stocks listed in NEPSE
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re

#opening the annapurna express

def nepse_symbols():
    path = 'https://merolagani.com/LatestMarket.aspx'
    r = requests.get(path,headers={'User-Agent': 'Chrome/108.0.0.0'})
    print(r.status_code)
    #Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36

    #creating a beautiful soup object
    bs = BeautifulSoup(r.content,'html.parser')
    tables = bs.find_all('table',attrs={'class': 'table table-hover live-trading sortable'})
    clean_string = re.sub('[0-9.]', '', tables[0].text)
    lines =clean_string.split('\n')


    # Remove empty lines
    lines = [line for line in lines if line.strip()]

    # Extract the alphabets between '\n' and '\n' and store them in a list
    results = [line.strip() for line in lines[1:]]
    modified_list = [element.replace('-', '') for element in results]
    stock_symbols = [element.replace(',','') for element in modified_list]

    return stock_symbols