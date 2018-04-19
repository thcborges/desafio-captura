# -*- coding: utf-8 -*-
# author: Thiago da Cunha Borges


import csv
import time
from urllib import request, parse
from bs4 import BeautifulSoup


class PageValues:
    def __init__(self, product_name, title, url, csv_file_name):
        """
        PageValues is started with values that will be saved in csv file.

        :param product_name: product name in the web page
        :param title: web page title
        :param url: product url
        :param csv_file_name: file name where will be saved the other parameters

        :type csv_file_name: str
        :type url: str
        :type title: str
        :type product_name: str
        """
        # this dictionary will be used to save data in csv file
        self.__values = {'product_name': product_name, 'title': title, 'url': url}
        # __csv_fields make save_data() method writes correctly in csv file.
        self.__csv_fields = self.__values.keys()
        self.__csv_file_name = csv_file_name

    @property
    def url(self):
        """
        Returns the url of a product
        :rtype: str
        """
        return self.__values['url']

    @property
    def title(self):
        """
        Returns the product web page title
        :rtype: str
        """
        return self.__values['title']

    @property
    def product(self):
        """
        Returns the product name
        :rtype: str
        """
        return self.__values['product_name']

    def __is_csv(self):
        """
        Checks if the csv file already exists.
        Returns true if there is the csv file, and false if not.
        :rtype: bool
        """
        try:
            # just open to check if there is the file
            with open(self.__csv_file_name, 'r') as file:
                file.close()
            return True
        # if it do not exists the exception will returns false
        except IOError:
            return False

    def __create_csv(self):
        """
        Creates a csv file.
        Writes in the file the fields of each attributes.
        """
        with open(self.__csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.__csv_fields, delimiter=';')
            writer.writeheader()

    def save_csv(self):
        """
        Checks if the csv file already exists to write in it the
        product name, his title web page and his url.
        """
        if not self.__is_csv():
            # creates the csv file if it did not exist.
            self.__create_csv()
        try:
            with open(self.__csv_file_name, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.__csv_fields, delimiter=';')
                writer.writerow(self.__values)
        except IOError:  # this exception avoid a product does not have saved in csv file
            time.sleep(0.5)
            self.save_csv()
        # display on the screen what is being record on csv
        for key, value in self.__values.items():
            print('{}: {}'.format(key, value), end='; ' if key != 'url' else '\n')


class Crawler:
    def __init__(self, main_url, file_name):
        """
        Crawler is a class responsible to look for every links in a given main_url
        It is able to localize and distinguish if each link in a url page passed
        have links that belong to the same domain.

        :param main_url: must be the main page of a web site.
        :param file_name: is the file name where the products will have his
        parameters saves

        :type main_url: str
        :type file_name: str
        """
        self.main_url = main_url
        self.__csv_file_name = file_name

    def __verify(self, href):
        """
        Checks if a reference in a link belong to the same domain of main url

        :param href: is a reference to another web page in a 'a' tag.

        :type href: str

        :rtype: bool
        """
        # change main url to avoid mistakes with http ou https
        main = self.main_url.replace('https://', '').replace('http://', '')
        forbiden = {"#", 'None'}  # forbidden possible urls
        if (href is None) or (href in forbiden):
            return False
        for item in ['tel:', 'mailto:', 'javascript:']:
            if item in href:  # verify if is a link to telephone, e-mail or javascript
                return False
        if main in href and ("/checkout/cart/add" in href or "/checkout/#/cart" in href):
            return False  # prevents a purchase from being made
        elif main in href or (main not in href and href[:4] != "http"):
            return True  # possible case of a valid link
        else:
            return False  # any other link is not valid

    def __add_main_site(self, href):
        """
        Check if the href has the main url in it

        :param href: is a reference to another web page in a 'a' tag.

        :type href: str
        """
        if self.main_url[8:] not in href:
            return self.main_url + href
        else:
            return href

    def __open_page(self, url):
        """
        Opens a web page and returns a bytearray.

        :param url: is a given url

        :type url: str

        :return: a open web page

        :rtype: bytearray
        """
        try:
            # Opens the url
            page = request.urlopen(url)
        except Exception as e:
            print(e, url)
            return ''
        else:
            # Avoid that None will be returned to that, try to open the web page again.
            return page if page is not None else self.__open_page(url)

    def __url_list(self, page):
            """
            Finds all the links to the main url in a given page.

            :param page: is a processed web page with BeautifulSoup class

            :type page: BeautifulSoup

            :rtype: list
            """
            url_list = []
            for tag_a in page.find_all('a'):
                href = str(tag_a.get('href'))
                if self.__verify(href):
                    url = parse.quote(self.__add_main_site(href), '/:#')
                    url_list.append(url)
            return url_list

    def get_links_list(self, url):
        """
        Looks for another links in a url given.

        :param url: is a url that will be looked for another url in in

        :type url: str

        :rtype: list
        """
        page = self.get_page(url)
        return self.__url_list(page)

    def get_page(self, url):
        """
        Opens a url and returns his processed page by BeautifulSoup.

        :param url: is a url to some page.

        :type url: str

        :rtype: BeautifulSoup
        """
        page = self.__open_page(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_product_urls(self, page):
        """
        Get all the url from a given BeautifulSoup object

        :param page: is a processed web page by BeautifulSoup

        :type page: BeautifulSoup

        :return: a list of all urls of the main url

        :rtype: list
        """
        return self.__url_list(page)

    def save_data(self, soup, url):
        """
        Saves the data in a csv file usin PageValues class

        :param soup: is a processed web page with BeautifulSoup class

        :type soup: BeautifulSoup

        :param url: is a url of a product
        """
        # get the web page title
        title = soup.find('title').string
        # get the h1 tag of the page
        h1 = soup.find('h1')
        # checks if there is a h1 tag in the page
        # because is possible that a product url redirects to
        # another page.
        # In this way, only a valid product will be save.
        if h1:
            product_name = h1.contents[0].string
            page_values = PageValues(product_name, title, url, self.__csv_file_name)
            page_values.save_csv()
        else:
            # Shows the web page that have some problem.
            print('It was not possible to open {}'.format(url))
