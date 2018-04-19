# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import sqlite3
import time


class Connect:
    def __init__(self, db_name):
        """
        Class connect represents the database connection.
        It opens a connection with a database file.

        :param db_name: name of the database file.
        """
        try:
            # Connects with the database
            self.conn = sqlite3.connect(db_name)
        except sqlite3.Error as e:
            print('Error. It was not possible open database: {}'.format(e))
            exit(1)
        else:
            # short cut to the database cursor
            self.cursor = self.conn.cursor()

    def commit_db(self):
        """
        Writes in the database the data given.
        """
        # Check if the connection with database is active
        if self.conn:
            self.conn.commit()

    def close_db(self):
        """
        Closes the connection with the database.
        """
        # Check if the connections with database is active
        if self.conn:
            self.conn.close()


class URLDatabase:
    def __init__(self, db_name, product_pattern):
        """
        Class that manager the links table of a sqlite database.
        This class will allow to insert one or a list of given urls,
        set visited one url, consult if a url is in the table and
        discriminate a product url.

        :param db_name: database file name.

        :type db_name: str

        :param product_pattern: pattern of product urls that will use to access
        this links.

        :type product_pattern: str
        """
        self.connection = Connect(db_name)
        self.cursor = self.connection.cursor
        self.product_pattern = product_pattern

    def create_schema(self):
        """
        Method responsible to create the table links in the database file.

        The 'IF NOT EXISTS' parameter in the schema will allow the use of
        the database even the program is interrupted.

        The url column saves urls.

        The visited column is set to default 0 when a url is inserted and
        set to 1, so it will be possible to know if a given url has already
        been visited or not.
        """
        schema = ('CREATE TABLE IF NOT EXISTS links (\n'
                  '    url TEXT NOT NULL PRIMARY KEY,'
                  '    visited INTEGER DEFAULT 0);')
        try:
            self.cursor.execute(schema)
        except sqlite3.Error as e:
            print('It was not possible create a table in the data base:\n{}'.format(e))
            exit(1)

    def close(self):
        """
        Close the conection with the database file.
        """
        self.connection.close_db()

    def __read_database(self, query, values):
        """
        This method is responsible to read a query in the database
        with a tuple of values given.

        :param query: has a query that reads some information in the database

        :type query: str

        :param values: has a tuple of values to read in the database

        :type values: tuple

        :return: the executed query from the database

        :rtype: sqlite3.Cursor
        """
        try:
            answer = self.cursor.execute(query, values)
        except sqlite3.Error as e:
            print(e)
            time.sleep(0.5)
            # if gets some error from de database, does the same query.
            return self.__read_database(query, values)
        return answer

    def __fetchone(self, query, values):
        """
        Returns the first value of a query with its values given

        :param query: query that will be make to the database

        :type query: str

        :param values: has a tuple of values to read in the database

        :return: the value got from the database
        """
        # read from the database
        data = self.__read_database(query, values)
        # get the first line of the answer from the database
        answer = data.fetchone()
        # check if there is a line in the answer
        if answer:
            # returns the first value of the line
            return answer[0]
        return None

    def total(self):
        """
        Get the total of urls in the database
        :return: the total of urls in the database
        :rtype: int
        """
        query = 'SELECT COUNT(*) FROM links'
        result = self.__fetchone(query, ())
        # check if result is different of None, if is, does again the same query
        return result if result is not None else self.total()

    def __is_new(self, url):
        """
        Check if there is a given url in the database.

        :param url: a url that will be conferred if is in the database

        :type url: str

        :return: True if there is not this url in the database and False if do not exist

        :rtype: bool
        """
        query = 'SELECT COUNT(*) FROM links WHERE url = ?;'
        result = self.__fetchone(query, (url, ))
        return True if result == 0 else False

    def get_unvisited_url(self):
        """
        Get a unvisited url from the database

        :return: a url unvisited

        :rtype: str
        """
        query = 'SELECT url FROM links WHERE visited = 0 LIMIT 1;'
        result = self.__fetchone(query, ())
        return result if result else self.get_unvisited_url()

    def get_unvisited_product(self):
        """
        Get a unvisited product url from the database.

        :return: a unvisited product url

        :rtype: str
        """
        query = 'SELECT url FROM links WHERE visited = 0 AND url like ? LIMIT 1;'
        result = self.__fetchone(query, (self.product_pattern, ))
        # check if result is different of None, if is, does again the same query
        return result if result else self.get_unvisited_product()

    def unvisited(self):
        """
        Get the amount of unvisited url in the database.

        :return: the amount of unvisited url

        :rtype: int
        """
        query = 'SELECT COUNT(*) FROM links WHERE visited = 0'
        result = self.__fetchone(query, ())
        # check if result is different of None, if is, does again the same query
        return result if result is not None else self.unvisited()

    def unvisited_product(self):
        """
        Get the amount of product urls in the database

        :return: amount of product urls

        :rtype: int
        """
        query = 'SELECT COUNT(*) FROM links WHERE visited = 0 AND url LIKE ?'
        result = self.__fetchone(query, (self.product_pattern, ))
        # check if result is different of None, if is, does again the same query
        return result if result is not None else self.unvisited_product()

    def has_unvisited(self):
        """
        Check if has unvisited urls in the database.

        :return: True if there is unvisited urls and false if not

        :rtype: bool
        """
        return True if self.unvisited() > 0 else False

    def has_unvisited_product(self):
        """
        Check if there is unvisited products in the database.

        :return: True if there is unvisited product urls and False if not

        :rtype: bool
        """
        return True if self.unvisited_product() > 0 else False

    def total_products(self):
        """
        Get the amount of product urls in the database

        :return: amount of product urls

        :rtype: int
        """
        query = 'SELECT COUNT(*) FROM links WHERE url LIKE ?'
        result = self.__fetchone(query, (self.product_pattern, ))
        # check if result is different of None, if is, does again the same query
        return result if result is not None else self.total_products()

    def __write_database(self, statement, values):
        """
        This method is responsible for doing all the writes in the database.

        :param statement: Statement that will be done to the database

        :type statement: str

        :param values: tuple of values to the statement

        :type values: tuple
        """
        try:
            self.cursor.execute(statement, values)
            self.connection.commit_db()
        except sqlite3.Error as e:
            print('Error writing in the database.')
            print(e)
            # if the database is locked, wait 0.5 seconds and try
            # to write again in the database
            if str(e) == 'database is locked':
                time.sleep(0.5)
                self.__write_database(statement, values)

    def insert_new_url(self, url):
        """
        Insert a new url to the database, if this url is not in the database yet.

        :param url: a url to be written in the database

        :type url: str
        """
        # check if there is the url given in the database
        if self.__is_new(url):
            statement = 'INSERT INTO links (url) VALUES (?);'
            self.__write_database(statement, (url, ))

    def insert_url_list(self, url_list):
        """
        Insert a list of urls in the database.

        :param url_list: list of urls

        :type url_list: list
        """
        for url in url_list:
            self.insert_new_url(url)

    def set_visited(self, url):
        """
        Changes the state of a url to visited.

        :param url: a url

        :type url: str
        """
        statement = 'UPDATE links SET visited = 1 WHERE url = ?;'
        self.__write_database(statement, (url, ))
