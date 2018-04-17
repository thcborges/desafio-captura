# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import os

from crawler import Crawler
from database import Database


MAIN = 'https://www.epocacosmeticos.com.br'


if __name__ == '__main__':
    crawler = Crawler(MAIN)
    database = Database('database.db')
    database.create_schema()
    database.insert_new_url(crawler.main_url)

    while database.has_unvisited():
        if database.has_unvisited_product():
            url = database.get_unvisited_product()
        else:
            url = database.get_unvisited_url()
        link_list = crawler.get_links_list(url)
        database.insert_url_list(link_list)
        database.set_visited(url)
        # show how many urls are missing to be verify
        print('Total unvisited:', database.unvisited())
        print('Products unvisited:', database.unvisited_product())

    database.close()
    os.remove('database.db')
