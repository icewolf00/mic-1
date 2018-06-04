import requests
import pandas as pd
import numpy as np
import datetime
import csv
import os
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates

def get_html(company_name):
    url = 'https://www.google.com.tw/search'
    keyword = {'q': company_name + ' stock'}
    html = requests.get(url, params=keyword).text
    print(html)
    return html

def get_market_cap(html):
    soup = BeautifulSoup(html, 'html.parser')
    market_cap = soup.findAll("td", {"align": "right"})[-1].text
    place = soup.findAll("h3", {"class": "r"})[0].find('span').text
    print(place)
    return market_cap, place

def get_currency_rate(x, y):
    if x == '':
        x = y
    c = CurrencyRates()
    r = c.get_rate(x, y)
    print(r)
    return r

def get_currency_rate2(x, y):
    try:
        api_key = '14ee46c12ed9a7f8d68e7e92/'
        url = 'https://v3.exchangerate-api.com/bulk/' + api_key + x
        response = requests.get(url)
        data = response.json()
        r = data['rates'][y]
        print(r)
        return r
    except:
        return ''

def market_cap_format(market_cap_str):
    market_cap_str = market_cap_str.replace('.', '')
    market_cap_str = market_cap_str.replace('億', '0'*8)
    market_cap_str = market_cap_str.replace('兆', '0'*12)
    market_cap_int = int(market_cap_str)
    print(market_cap_int)
    return market_cap_int

def get_lift(i):
    if i > 0:
        return '+ ' + str(i)
    elif i < 0:
        return '- ' + str(i)
    else:
        return '+ ' + str(i)

company = pd.read_csv('company.csv')
company_name_list = company['name']
company_market_cap_list = list()
currency = pd.read_csv('currency.csv')
currency_name = currency['name']
currency_symbol = currency['symbol']

for i in company_name_list:
    try:
        name = i
        html = get_html(name)
        market_cap, place = get_market_cap(html)
        company_market_cap_list.append([name, market_cap, place])
    except:
        company_market_cap_list.append([name, '', ''])

for i, j in enumerate(company_market_cap_list):
    company_market_cap_list[i].append('')
    for k, l in enumerate(currency_name):
        if l in j[-2]:
            company_market_cap_list[i][-1] = currency_symbol[k]
            break

for i, j in enumerate(company_market_cap_list):
    try:
        company_market_cap_list[i].append(get_currency_rate(j[-1], 'USD'))
    except:
        company_market_cap_list[i].append(get_currency_rate2(j[-1], 'USD'))

for i, j in enumerate(company_market_cap_list):
    try:
        company_market_cap_list[i].append(market_cap_format(j[1]))
    except:
        company_market_cap_list[i].append('')

for i, j in enumerate(company_market_cap_list):
    try:
        company_market_cap_list[i].append(int(j[-1] * j[-2]))
    except:
        company_market_cap_list[i].append('')


path = 'datasets/'
last = max(os.listdir(path))
path = path + last
df_last = pd.read_csv(path)

df = pd.DataFrame(columns=['rank', 'lift', 'name', 'exchange', 'code', 'rate', 'market_cap'])
for i in company_market_cap_list:
    df = df.append({'name': i[0],
                    'exchange': i[2],
                    'code': i[3],
                    'rate': i[4],
                    'market_cap': i[6],
                   }, ignore_index=True)

df = df.replace('', np.nan, regex=True)
df = df.sort_values(by=['market_cap'], ascending=False)
df = df.reset_index(drop=True)

df['rank'] = df.index + 1
df['lift'] = df['rank'] - df_last['rank']
lift_list = df['lift'].tolist()
for i, j in enumerate(lift_list):
    lift_list[i] = get_lift(j)
lift_series = pd.Series(lift_list)
df['lift'] = lift_series
df = df.replace(np.nan, '')

now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
path = 'datasets/' + now + '.csv'
df.to_csv(path, index=False)