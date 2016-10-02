#!/usr/bin/env python3
from requests import get
from textwrap import shorten
from bs4 import BeautifulSoup
from string import whitespace
from collections import OrderedDict

SEARCH_URL = "http://www.duden.de/suchen/dudenonline/{}"
DETAIL_URL = "http://www.duden.de/rechtschreibung/{}"

BS_PARSER = 'lxml'

class Duden:

    def __init__(self):
        pass

    def search(self, keyword):
        """Search for available dictionary entries given a specific keyword."""
        print("Searching for", SEARCH_URL.format(keyword))
        soup = BeautifulSoup(get(SEARCH_URL.format(keyword)).text, 'lxml')
        results = OrderedDict()
        for result in soup.find_all('section', class_="wide"):
            if result.has_attr('style'): continue
            word = result.find('a').get_text().replace(u'\xAD', '')
            desc = shorten(result.find('p').get_text(), width=55)
            results[word] = desc
        return results

    def __get_details(self, word):
        # TODO
        r = get(DETAIL_URL.format(word))
        if r.status_code == 404:
            raise WordNotFoundException()
        soup = BeautifulSoup(r.text, 'lxml')
        titel = soup.select("#block-system-main > h1:nth-child(2)").get_text()
        wortart = soup.select("strong.lexem:nth-child(2)").get_text()

class WordNotFoundException(Exception):
    """Exception that is raised when the requested word was not found."""
    pass
