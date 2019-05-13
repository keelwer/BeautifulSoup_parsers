import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='pagination')
    pages = divs.find_all('a', class_='pagination-item')[-2].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


def write_csv(data):
    with open('psychology_books.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['author'],
                         data['price'],
                         data['url']))


def page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='container_cards')
    ads = divs.find_all('div', class_='product-card')
    for ad in ads:
        try:
            div = ad.find('div', class_='product-card__info').find('a', class_='product-card__link').find('div', class_='product-card__title')
            title = div.text.strip()
        except:
            title = ''
        try:
            div = ad.find('div', class_='product-card__info').find('a', class_='product-card__link').find('div', class_='product-card__author')
            author = div.text.strip()
        except:
            author = ''
        try:
            div = ad.find('div', class_='product-card__info')
            url = "https://www.chitai-gorod.ru" + div.find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='product-card__info').find('div', class_='product-card__footer').find('div', class_='product-card__price').find('span', class_='product-price__value').text.strip()
        except:
            price = ''
        data = {'title': title,
                'author': author,
                'price': price,
                'url': url}
        write_csv(data)


def main():
    url = 'https://www.chitai-gorod.ru/catalog/books/psikhologiya-9530/?page=1'
    base_url = "https://www.chitai-gorod.ru/catalog/books/psikhologiya-9530/?"
    page_part = "p="

    total_pages_site = total_pages(get_html(url))

    for i in range(1, 4):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        page_data(html)


if __name__ == '__main__':
    main()
