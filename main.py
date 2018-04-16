# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import os

from crawler import Crawler
from database import Database


if __name__ == '__main__':
    crawler = Crawler('https://www.epocacosmeticos.com.br')
    database = Database('database.db')
    database.create_schema()
    database.insert_new_url(crawler.main_url)

    while database.has_unvisited():
        url = database.get_unvisited_url()
        link_list = crawler.get_links_list(url)
        database.insert_url_list(link_list)
        database.set_visited(url)
        # show how many urls are missing to be verify
        print(database.unvisited())

    database.close()
    os.remove('database.db')
