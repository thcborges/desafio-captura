# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import sqlite3
import time


class Connect:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print('Error. It was not possible open database: {}'.format(e))
            exit(1)

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()


class Database:
    def __init__(self, db_name):
        self.table = 'new_link'
        self.db = Connect(db_name)
        self.cursor = self.db.cursor

    @property
    def total(self):
        try:
            query = self.cursor.execute('SELECT COUNT(*) FROM new_link')
        except sqlite3.Error as e:
            print(e)
            return ''
        else:
            total = query.fetchone()
            return total[0]

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

    def insert_new_url(self, url):
        if self.__is_new(url):
            try:
                self.cursor.execute('INSERT INTO new_link (url) VALUES (?);', (url, ))
                self.db.commit_db()
            except sqlite3.Error as e:
                print(e, url)

    def __is_new(self, url):
        try:
            query = self.cursor.execute('SELECT COUNT(*) FROM new_link WHERE url = ?;', (url, ))
        except sqlite3.Error as e:
            print(e, url)
            return self.__is_new(url)
        else:
            result = query.fetchone()
            if result:
                return True if result[0] == 0 else False
            return False

    def insert_url_list(self, url_list):
        for url in url_list:
            self.insert_new_url(url)

    def set_visited(self, url):
        try:
            self.cursor.execute('UPDATE new_link SET visited = 1 WHERE url = ?;', (url, ))
            self.db.commit_db()
        except sqlite3.Error as e:
            print(e, url)

    def get_unvisited_url(self):
        try:
            query = self.cursor.execute('SELECT url FROM new_link WHERE visited = 0 LIMIT 1;')
        except sqlite3.Error as e:
            print(e)
            return ''
        else:
            result = query.fetchone()
            url = result[0] if result else ''
            return url

    def unvisited(self):
        try:
            query = self.cursor.execute('SELECT COUNT(*) FROM new_link WHERE visited = 0')
        except sqlite3.Error as e:
            print(e)
        else:
            result = query.fetchone()
            amount = result[0]
            return amount

    def has_unvisited(self):
        return True if self.unvisited() > 0 else False
