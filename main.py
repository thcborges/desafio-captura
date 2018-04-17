# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import os

from crawler import Crawler
from database import Database


MAIN = 'https://www.epocacosmeticos.com.br'


class Main:
    def __init__(self, main_url, database_file):
        self.main_url = main_url
        self.crawler = Crawler(self.main_url, self.main_url.replace('https://www.', '').replace('.', '-'))
        self.database_file = database_file
        self.database = Database(self.database_file)
        self.database.create_schema()
        self.database.insert_new_url(self.main_url)

    def search_for_products(self):
        while self.database.has_unvisited():
            if self.database.has_unvisited_product():
                self.__search_in_product_url()
            else:
                self.__search_in_not_product_url()

    def __search_in_product_url(self):
        url = self.database.get_unvisited_product()
        page = self.crawler.get_page(url)
        self.crawler.save_data(page, url)
        url_list = self.crawler.get_product_urls(page)
        self.database.set_visited(url)
        self.database.insert_url_list(url_list)

    def __search_in_not_product_url(self):
        url = self.database.get_unvisited_url()
        url_list = self.crawler.get_links_list(url)
        self.database.set_visited(url)
        self.database.insert_url_list(url_list)

    def close_database(self):
        self.database.close()
        self.__delete_database()

    def __delete_database(self):
        if self.__confirmation('Would you want to delete the database [Y/N]? '):
            os.remove(self.database_file)

    def __confirmation(self, message):
        answer = input(message)
        if answer.upper() != 'Y' or answer.upper() != 'N':
            print('It was not possible understand your answer, please try again.')
            return self.__confirmation(message)
        elif answer.upper() == 'Y':
            return True
        return False


if __name__ == '__main__':
    main = Main(MAIN, 'database.db')
    try:
        main.search_for_products()
    except KeyboardInterrupt:
        print('Stopping search.')
    finally:
        main.close_database()
