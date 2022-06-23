import requests
from bs4 import BeautifulSoup as BS
import csv
import io
CSV = 'cards.csv'
HOST = 'https://kaspi.kz/'
URL = 'https://kaspi.kz/shop/c/categories/'


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers= HEADERS, params= params)
    return r

def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('div', class_='item-card__info')
    cards = []
    for item in items:
        cards.append(
            {
                'Название товара': item.find('a', class_='item-card__name').get_text(strip=True),
                'LinkProduct': HOST + item.find('a', class_='item-card__name').get('href'),
                'Отзывы': item.find('div', class_='item-card__rating').find('a').get_text(strip=True),
                'Цена': item.find('span', class_='item-card__prices-price').get_text(strip=True)

            }
        )
    return cards


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта', 'Ссылка продукта', 'Кол-во отзывов продукта'])
        for item in items:
            writer.writerow([item['Название товара'], item['LinkProduct'], item['Отзывы']])

def parser():
   PAGENATION = input('Укажите количество страниц для парсинга:')
   PAGENATION = int(PAGENATION.strip())
   html = get_html(URL)
   if html.status_code==200:
       cards = []
       for page in range(1, PAGENATION+1):
           print(f'Парсим страницу: {page}')
           html = get_html(URL, params = {'page': page})
           cards.extend(get_content(html.text))
           save_doc(cards, CSV)
       print(f'Парсинг закончился!')
       print(cards)
   else:
        print('Error')
parser()
#html = get_html(URL)
#print(get_content(html.text))