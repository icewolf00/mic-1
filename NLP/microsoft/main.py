import requests
import csv
import os
from bs4 import BeautifulSoup

def get_link(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    with open('link.csv', 'a') as csvfile:
        fieldnames = ['title', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        for i in soup.find_all('article'):
            title = i.find('h3').find('a').text
            link = i.find('h3').find('a')['href']
            writer.writerow({'title': title, 'link': link})

def get_text(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")
    title = (soup.find('h1').text).replace('/', '')
    path = 'article/' + title + '.txt'
    with open(path, 'w') as textfile:
        for i in soup.find_all('p'):
            textfile.write(i.text)

def get_stage(now, end):
    percent = now / end
    if percent < 0.1:
        percent = str(percent)
        percent = percent[3]
    elif percent == 1.0:
        percent = str(100)
    else:
        percent = str(percent)
        percent = percent[2:4]
        while len(percent) < 2:
            percent += '0'
    return percent + '%'

def main():
    j = 0
    for i in range(1, 81):
        url = 'https://blogs.microsoft.com/ai/page/' + str(i)
        get_link(url)
        j += 1
        print('stage1: %s' % get_stage(j, 80))
    with open('link.csv', 'r') as csvfile:
        t = 0
        for i in csvfile:
            t += 1
    with open('link.csv', 'r') as csvfile:
        k = 0
        spamreader = csv.reader(csvfile)
        for i in spamreader:
            try:
                get_text(i[1])
                k += 1
                print('stage2: %s' % get_stage(k, t))
            except:
                pass

if __name__ == '__main__':
    main()