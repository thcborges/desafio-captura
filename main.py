# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import os

from crawler import Crawler
from database import URLDatabase


MAIN = {
    'domain': 'https://www.epocacosmeticos.com.br',
    'product_pattern': 'https://www.epocacosmeticos.com.br%/p'
}


class Main:
    def __init__(self, params):
        """
        Main class, responsible to run the crawler correctly.

        :param params: dict with domain and product pattern

        :type params: dict
        """
        # hold the domain in a attribute
        self.__domain = params['domain']
        # create a name for database and csv file using the domain
        self.__file_name = self.domain.replace('https://www.', '').replace('.', '-')
        # starts the crawler with domain and the csv file name
        self.__crawler = Crawler(self.domain, self.csv_file_name)
        # starts the database with database file name and the product pattern
        self.__database = URLDatabase(self.database_file_name, params['product_pattern'])
        # creates the schema of the database
        self.__database.create_schema()
        # insert the domain in the database
        self.__database.insert_new_url(self.domain)

    @property
    def domain(self):
        """
        Domain of the web site

        :return: the domain of the web site

        :rtype: str
        """
        return self.__domain

    @property
    def database_file_name(self):
        """
        Database file name

        :return: the database file name

        :rtype: srt
        """
        return self.__file_name + '.db'

    @property
    def csv_file_name(self):
        """
        csv file name

        :return: the csv file name

        :rtype: str
        """
        return self.__file_name + '.csv'

    def search_for_products(self):
        """
        Search for products in the web site.
        Every time a product is found his web page will be open.
        """
        # just show search details
        self.show_status()
        # search for urls while has urls unvisited
        while self.__database.has_unvisited():
            # gives preferences to product urls
            if self.__database.has_unvisited_product():
                self.__search_in_product_url()
            else:
                self.__search_in_not_product_url()
                # show search details
                self.show_status()

    def __search_in_product_url(self):
        """
        Search for urls in product urls and save
        its title, name and url in the csv file.
        """
        # get a unvisited product url from database
        url = self.__database.get_unvisited_product()
        # get the open page with crawler
        page = self.__crawler.get_page(url)
        # save the data of file in the csv
        self.__crawler.save_data(page, url)
        # get the url list of the opened web page
        url_list = self.__crawler.get_product_urls(page)
        # inserts the url list in the database
        self.__database.insert_url_list(url_list)
        # sets the url as visited
        self.__database.set_visited(url)

    def __search_in_not_product_url(self):
        """
        Does the search for urls in a not product url.
        """
        # get one unvisited url from the database
        url = self.__database.get_unvisited_url()
        # get a list of urls presents in the web page
        url_list = self.__crawler.get_links_list(url)
        # inserts the url list in the database
        self.__database.insert_url_list(url_list)
        # sets url as visited
        self.__database.set_visited(url)

    def close_database(self):
        """
        Closes the database.
        """
        self.__database.close()

    def delete_database(self):
        """
        Ask user if he wants to delete the database file
        and delete it or not.
        """
        self.close_database()
        if self.__confirmation('Would you want to delete the database [Y/N]? '):
            try:
                # Delete the database file.
                os.remove(self.database_file_name)
            except os.error as e:
                print('It was not possible delete database file.')
                print(e)

    def __confirmation(self, message):
        """
        Makes a confirmation with user wants to do something.

        :param message: A message to show to user.

        :type message: str

        :return: True if the user wants to do something or false if not

        :rtype: bool
        """
        answer = input(message)
        if answer.upper() != 'Y' and answer.upper() != 'N':
            print('It was not possible understand your answer, please try again.')
            return self.__confirmation(message)
        elif answer.upper() == 'Y':
            return True
        return False

    def show_status(self):
        """
        Show to user the status of the search.
        """
        # gets the total of urls from the database
        total = self.__database.total()
        # gets the amount of unvisited urls in the database
        total_unvisited = self.__database.unvisited()
        # gets the amount of product urls in the database
        products = self.__database.total_products()
        # gets the amount of unvisited product urls in the database
        products_unvisted = self.__database.unvisited_product()
        # calculates the percentage of visited urls avoiding the division by zero
        percent_total = (total - total_unvisited) / total * 100 if total != 0 else 0
        # calculates the percentage of visited product urls avoiding the division by zero
        percent_products = (products - products_unvisted) / products * 100 if products != 0 else 0
        # creates the message
        message = '{}| {} |{}\n'.format('=#' * 18, self.domain, '#=' * 18)
        message += 'Found URLs:\t\t{}\t'.format(total)
        message += 'Unvisited URLs:\t\t\t{}\t'.format(total_unvisited)
        message += 'Percent visited:\t\t{:.1f}%\n'.format(percent_total)
        message += 'Found products URLs:\t{}\t'.format(products)
        message += 'Unvisited products URLs:\t{}\t'.format(products_unvisted)
        message += 'Percent visited products:\t{:.1f}%\n'.format(percent_products)
        message += '{}=\n'.format('=#' * 55)
        # clean the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # shows the message created
        print(message)


if __name__ == '__main__':
    # creates the Main class object
    main = Main(MAIN)
    try:
        # does the search for product urls
        main.search_for_products()
        print('SEARCH COMPLETED')
    # allow search to be stopped at any time and can be resumed later
    except KeyboardInterrupt:
        print('Keyboard Interrupt received.')
        print('Stopping search.')
        input('Press ENTER to finish')
        # closes the database
        main.close_database()
    except Exception as error:
        # forces the database to be closed in case of some error
        print(error)
        print('It was not possible read all url found. Please, try again.')
        print('The program is able to resume where it stopped. Please, try again.')
        input('Press ENTER to finish')
        main.close_database()
    else:
        # closes and delete the database
        main.delete_database()
