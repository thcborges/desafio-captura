# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import os
from unittest import TestCase
from database import Database


class MyTest(TestCase):

    def test_database(self):
        db_name = 'testsDb1.db'
        url = 'https://www.epocacosmeticos.com.br'
        db = Database(db_name, 'https://www.epocacosmeticos.com.br%/p')
        db.create_schema()

        # checking if database is empty
        self.assertEqual(0, db.total(), 'total before insertion')
        self.assertFalse(db.has_unvisited(), 'has unvisited before insertion')

        # inserting main url in data base
        db.insert_new_url(url)
        self.assertTrue(db.has_unvisited(), 'has unvisited')
        self.assertFalse(db.has_unvisited_product(), 'has not unvisited products')
        self.assertEqual(1, db.total(), 'has 1 url in database')

        # setting main url visited
        db.set_visited(url)
        self.assertFalse(db.has_unvisited(), 'has not unvisited')
        self.assertEqual(1, db.total(), 'total after set main url visited')

        # inserting product url
        product_url = 'https://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-perfume-feminino/p'
        db.insert_new_url(product_url)
        self.assertTrue(db.has_unvisited(), 'has unvisited')
        self.assertTrue(db.has_unvisited_product(), 'has unvisited products')
        self.assertEqual(2, db.total(), 'has 2 urls in database')
        self.assertEqual(product_url, db.get_unvisited_url(), 'first url added')
        self.assertEqual(product_url, db.get_unvisited_product(), 'product url')

        # setting product url visited
        db.set_visited(product_url)
        self.assertFalse(db.has_unvisited_product(), 'all products urls are visited')
        self.assertFalse(db.has_unvisited(), 'all urls are visited')

        # closing and deleting database
        db.close()
        os.remove(db_name)


if __name__ == '__main__':
    tests = MyTest
