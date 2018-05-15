import requests
import csv
import os
import json
from bs4 import BeautifulSoup

def main(url):
    html = requests.get(url).text
    ajax_json = json.loads(html)
    company_all_list = list()
    for i in ajax_json:
        company_list = list()
        try:
            company_list.append(i['position'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['rank'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['name'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['uri'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['imageUri'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['industry'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['country'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['revenue'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['marketValue'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['headquarters'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['state'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['ceo'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['thumbnail'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['profits'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['assets'])
        except:
            company_list.append(None)
        try:
            company_list.append(i['squareImage'])
        except:
            company_list.append(None)
        company_all_list.append(company_list)
    with open('forbes.csv', 'w') as csvfile:
        fieldnames = ['position', 'rank', 'name', 'uri', 'imageUri', 'industry', 'country', 'revenue', 'marketValue', 'headquarters', 'state', 'ceo', 'thumbnail', 'profits', 'assets', 'squareImage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in company_all_list:
            writer.writerow({                
                'position': i[0],
                'rank': i[1],
                'name': i[2], 
                'uri':i[3],
                'imageUri':i[4],
                'industry':i[5], 
                'country':i[6],
                'revenue':i[7], 
                'marketValue':i[8], 
                'headquarters':i[9], 
                'state':i[10], 
                'ceo':i[11], 
                'thumbnail':i[12], 
                'profits':i[13], 
                'assets':i[14], 
                'squareImage':i[15],
            })

def rank_company(company_all_list):
    company_all_rank_list = list()
    compare_rank = 0
    for i, j in enumerate(company_all_list):
        
        if int(j[0]) < compare_rank:




if __name__ == '__main__':
    main('https://www.forbes.com/ajax/list/data?year=2017&uri=global2000&type=organization')