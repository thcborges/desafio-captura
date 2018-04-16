# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import sqlite3


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
            self.commit_db()

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
                  '    id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                  '    url TEXT NOT NULL UNIQUE);')
        try:
            self.cursor.execute(schema)
        except sqlite3.Error as e:
            print('Warning: table {} may already exists: {}'.format(self.table, e))

    def close(self):
        self.db.close_db()

    def insert_new_url(self, url):
        try:
            self.cursor.execute('INSERT INTO new_link (url) VALUES (?)', (url, ))
            self.db.commit_db()
        except sqlite3.Error as e:
            print(e, url)

    def __is_new(self, url):
        try:
            query = self.cursor.execute('SELECT COUNT(url) FROM new_link WHERE url = ?', (url, ))
        except sqlite3.Error as e:
            print(e, url)
            return self.__is_new(url)
        else:
            result = query.fetchone()
            return True if result[0] == 0 else False

    def insert_url_list(self, url_list):
        for url in url_list:
            if self.__is_new(url):
                self.insert_new_url(url)

    def get_url(self, label):
        try:
            query = self.cursor.execute('SELECT url FROM new_link WHERE id = ?', (label, ))
        except sqlite3.Error as e:
            print(e, label)
            return ''
        else:
            result = query.fetchone()
            url = result[0] if result else ''
            return url
