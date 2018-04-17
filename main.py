# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import os

from crawler import Crawler
from database import Database


MAIN = {'url': 'https://www.epocacosmeticos.com.br', 'product_pattern': '%/p'}


class Main:
    def __init__(self, params):
        self.__main_url = params['url']
        self.__file_name = self.__main_url.replace('https://www.', '').replace('.', '-')
        self.__crawler = Crawler(self.__main_url, self.csv_file_name)
        self.__database = Database(self.database_file_name, params['product_pattern'])
        self.__database.create_schema()
        self.__database.insert_new_url(self.__main_url)

    @property
    def main_url(self):
        return self.__main_url

    @property
    def database_file_name(self):
        return self.__file_name + '.db'

    @property
    def csv_file_name(self):
        return self.__file_name + '.csv'

    def search_for_products(self):
        while self.__database.has_unvisited():
            if self.__database.has_unvisited_product():
                self.__search_in_product_url()
            else:
                self.__search_in_not_product_url()

    def __search_in_product_url(self):
        url = self.__database.get_unvisited_product()
        page = self.__crawler.get_page(url)
        self.__crawler.save_data(page, url)
        url_list = self.__crawler.get_product_urls(page)
        self.__database.set_visited(url)
        self.__database.insert_url_list(url_list)

    def __search_in_not_product_url(self):
        url = self.__database.get_unvisited_url()
        url_list = self.__crawler.get_links_list(url)
        self.__database.set_visited(url)
        self.__database.insert_url_list(url_list)

    def close_database(self):
        self.__database.close()
        self.__delete_database()

    def __delete_database(self):
        if self.__confirmation('Would you want to delete the database [Y/N]? '):
            try:
                os.remove(self.database_file_name)
            except os.error as e:
                print('It was not possible delete database file.')
                print(e)

    def __confirmation(self, message):
        answer = input(message)
        if answer.upper() != 'Y' and answer.upper() != 'N':
            print('It was not possible understand your answer, please try again.')
            return self.__confirmation(message)
        elif answer.upper() == 'Y':
            return True
        return False


if __name__ == '__main__':
    main = Main(MAIN)
    try:
        main.search_for_products()
    except KeyboardInterrupt:
        print('Stopping search.')
    finally:
        main.close_database()
