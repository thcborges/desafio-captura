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

    ident = 1
    while ident < database.total:
        link = database.get_url(ident)
        link_list = crawler.get_links_list(link)
        ident += 1
        database.insert_url_list(link_list)
        # show how many urls are missing to be verify
        print(database.total - ident)

    database.close()
    os.remove('database.db')
