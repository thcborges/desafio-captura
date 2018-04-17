# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import csv
import time
from urllib import request, parse
from bs4 import BeautifulSoup


class PageValues:
    def __init__(self, product_name, title, url, csv_file_name):
        self.__values = {'product_name': product_name, 'title': title, 'url': url}
        self.__csv_fields = self.__values.keys()
        self.__csv_file_name = csv_file_name

    @property
    def url(self):
        return self.__values['url']

    @property
    def title(self):
        return self.__values['title']

    @property
    def product(self):
        return self.__values['product_name']

    def __is_csv(self):
        try:
            with open(self.__csv_file_name, 'r') as file:
                file.close()
                return True
        except IOError:
            return False

    def __create_csv(self):
        with open(self.__csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.__csv_fields, delimiter=';')
            writer.writeheader()

    def save_csv(self):
        if not self.__is_csv():
            self.__create_csv()
        try:
            with open(self.__csv_file_name, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.__csv_fields, delimiter=';')
                writer.writerow(self.__values)
        except IOError:
            time.sleep(0.5)
            self.save_csv()

        # display on the screen what is being record on csv
        print('{} PAGE VALUES {}'.format('=' * 10, '=' * 10))
        for key, value in self.__values.items():
            print('{}: {}'.format(key, value))


class Crawler:
    def __init__(self, main_url, file_name):
        self.main_url = main_url
        self.__csv_file_name = file_name

    def __verify(self, href):
        # TODO
        main = self.main_url.replace('https://', '')

        if href == "#":
            return False
        if href is None:
            return False
        if href == 'None':
            return False
        if 'tel:' in href or 'mailto:' in href:
            return False
        if main in href and ("/checkout/cart/add" in href or "/checkout/#/cart" in href):
            return False
        elif "javascript" in href:
            return False
        elif main in href:
            return True
        elif main not in str(href) and href[:4] != "http":
            return True
        else:
            return False

    def __add_main_site(self, url):
        if self.main_url[8:] not in url:
            return self.main_url + url
        else:
            return url

    @staticmethod
    def __open_page(url):
        try:
            page = request.urlopen(url)
        except Exception as e:
            print(e, url)
            return ''
        else:
            return page

    def __url_list(self, page):
            url_list = []
            for tag_a in page.find_all('a'):
                href = str(tag_a.get('href'))
                if self.__verify(href):
                    url = parse.quote(self.__add_main_site(href), '/:#')
                    url_list.append(url)
            return url_list

    def get_links_list(self, url):
        page = self.get_page(url)
        return self.__url_list(page)

    def get_page(self, url):
        page = self.__open_page(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_product_urls(self, page):
        return self.__url_list(page)

    def save_data(self, soup, url):
        title = soup.find('title').string
        h1 = soup.find('h1')
        if h1:
            product_name = h1.contents[0].string
            page_values = PageValues(product_name, title, url, self.__csv_file_name)
            page_values.save_csv()
        else:
            print('It was not possible to open {}'.format(url))
