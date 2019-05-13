import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='pagination-pages clearfix')
    pages = divs.find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def write_csv(data):
    with open('avito_krvartiry.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['url']))


def page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='catalog-list')
    ads = divs.find_all('div', class_='item_table')
    for ad in ads:
        try:
            div = ad.find('div', class_='item_table-wrapper').find('div', class_='description').find('h3')
            if '1-к квартира' not in div.text.lower():
                continue
            else:
                title = div.text.strip()
        except:
            title = ''
        try:
            div = ad.find('div', class_='item_table-wrapper').find('div', class_='description').find('h3')
            url = "https://avito.ru" + div.find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='item_table-wrapper').find('div', class_='description').find('div', class_='about').find('span', class_='price').text.strip()
        except:
            price = ''
        data = {'title': title,
                'price': price,
                'url': url}
        write_csv(data)


def main():
    url = 'https://www.avito.ru/moskva/kvartiry?p=1&metro=1'
    base_url = "https://www.avito.ru/moskva/kvartiry?"
    page_part = "p="
    part_query = "&metro=1"

    total_pages_site = total_pages(get_html(url))

    for i in range(1, total_pages_site):
        url_gen = base_url + page_part + str(i) + part_query
        html = get_html(url_gen)
        page_data(html)


if __name__ == '__main__':
    main()
