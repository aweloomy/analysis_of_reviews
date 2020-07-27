import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

from urllib3.connection import log
a = []
b = []
c = []
URL = 'https://www.banki.ru/services/responses/bank/rshb/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
           'accept': '*/*'}

def get_html(url, params = None):
    while True:
        try:
            r = requests.get(url, headers=HEADERS, params=params)
            if r.status_code != 200:
                log.info("Ошибка, Код ответа: %s", r.status)
                time.sleep(1)

                continue
            return r
        except ConnectionError:
            log.exception("Ошибка ConnectionError")
            time.sleep(1)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='responses__item')
    reviews = []

    for item in items:
        reviews.append({
            'rating': item.find('div', class_='margin-top-xx-small color-gray-burn').get_text(strip=True),
            'title': item.find('div', class_='flexbox').get_text(strip=True),
            'text': item.find('div', class_='responses__item__message markup-inside-small markup-inside-small--bullet')
        })
        a.append(item.find('div', class_='margin-top-xx-small color-gray-burn').get_text(strip=True))
        b.append(item.find('div', class_='flexbox').get_text(strip=True))
        c.append(item.find('div', class_='responses__item__message markup-inside-small markup-inside-small--bullet'))
    return reviews

def parse():
    html = get_html(URL)
    #print(html.status_code)
        #get_content(html.text)
    reviews = []
    for page in range(1, 101):
        print(f'Парсинг страницы {page}...')
        html = get_html(URL, params={'page': page})
        reviews.append(get_content(html.text))
        #print(b)


d={'rating' : a, 'header' : b,'review' : c}

# df = pd.DataFrame(data = d)
parse()
df = pd.DataFrame(data=d)
print(df.shape)
#df.to_csv('Reviews_0.csv', sep='|', encoding = 'utf-8')

