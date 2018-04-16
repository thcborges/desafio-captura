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

    def create_schema(self):
        schema = ('CREATE TABLE IF NOT EXISTS new_link (\n'
                  '    id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                  '    url TEXT NOT NULL UNIQUE);')
        try:
            self.cursor.execute(schema)
        except sqlite3.Error as e:
            print('Warining: table {} may already exists: {}'.format(self.table, e))

    def close(self):
        self.db.close_db()
