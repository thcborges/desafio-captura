# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import sqlite3
import time


class Connect:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
        except sqlite3.Error as e:
            print('Error. It was not possible open database: {}'.format(e))
            exit(1)
        else:
            self.cursor = self.conn.cursor()

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()


class Database:
    def __init__(self, db_name, product_pattern):
        self.table = 'new_link'
        self.db = Connect(db_name)
        self.cursor = self.db.cursor
        self.product_pattern = product_pattern

    def create_schema(self):
        schema = ('CREATE TABLE IF NOT EXISTS new_link (\n'
                  '    url TEXT NOT NULL PRIMARY KEY,'
                  '    visited INTEGER DEFAULT 0);')
        try:
            self.cursor.execute(schema)
        except sqlite3.Error as e:
            print('Warning: table {} may already exists: {}'.format(self.table, e))

    def close(self):
        self.db.close_db()

    def __read_database(self, query, values):
        try:
            answer = self.cursor.execute(query, values)
        except sqlite3.Error as e:
            print(e)
            time.sleep(0.5)
            return self.__read_database(query, values)
        return answer

    def __fetchone(self, query, values):
        data = self.__read_database(query, values)
        answer = data.fetchone()
        if answer:
            return answer[0]
        return None

    def total(self):
        query = 'SELECT COUNT(*) FROM new_link'
        result = self.__fetchone(query, ())
        return result if result is not None else self.total()

    def __is_new(self, url):
        query = 'SELECT COUNT(*) FROM new_link WHERE url = ?;'
        result = self.__fetchone(query, (url, ))
        return True if result == 0 else False

    def get_unvisited_url(self):
        query = 'SELECT url FROM new_link WHERE visited = 0 LIMIT 1;'
        result = self.__fetchone(query, ())
        return result if result else self.get_unvisited_url()

    def get_unvisited_product(self):
        query = 'SELECT url FROM new_link WHERE visited = 0 AND url like ? LIMIT 1;'
        result = self.__fetchone(query, (self.product_pattern, ))
        return result if result else self.get_unvisited_product()

    def unvisited(self):
        query = 'SELECT COUNT(*) FROM new_link WHERE visited = 0'
        result = self.__fetchone(query, ())
        return result if result is not None else self.unvisited()

    def unvisited_product(self):
        query = 'SELECT COUNT(*) FROM new_link WHERE visited = 0 AND url LIKE ?'
        result = self.__fetchone(query, (self.product_pattern, ))
        return result if result is not None else self.unvisited_product()

    def has_unvisited(self):
        return True if self.unvisited() > 0 else False

    def has_unvisited_product(self):
        return True if self.unvisited_product() > 0 else False

    def total_products(self):
        query = 'SELECT COUNT(*) FROM new_link WHERE url LIKE ?'
        result = self.__fetchone(query, (self.product_pattern, ))
        return result if result is not None else self.total_products()

    def __write_database(self, statement, values):
        try:
            self.cursor.execute(statement, values)
            self.db.commit_db()
        except sqlite3.Error as e:
            print('Error writing in the database.')
            print(e)
            if str(e) == 'database is locked':
                time.sleep(0.5)
                self.__write_database(statement, values)

    def insert_new_url(self, url):
        if self.__is_new(url):
            statement = 'INSERT INTO new_link (url) VALUES (?);'
            self.__write_database(statement, (url, ))

    def insert_url_list(self, url_list):
        for url in url_list:
            self.insert_new_url(url)

    def set_visited(self, url):
        statement = 'UPDATE new_link SET visited = 1 WHERE url = ?;'
        self.__write_database(statement, (url, ))
