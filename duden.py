#!/usr/bin/env python3
from requests import get
from textwrap import shorten
from bs4 import BeautifulSoup
from string import whitespace
from collections import OrderedDict

DETAIL_URL = "http://www.duden.de/rechtschreibung/{}"
SEARCH_URL = "http://www.duden.de/suchen/dudenonline/{}"

class Duden:

    def __init__(self):
        pass

    def search(self, keyword):
        """Search for available dictionary entries given a specific keyword."""
        soup = BeautifulSoup(get(SEARCH_URL.format(keyword)).text, 'lxml')
        # OrderedDict because entries are sorted by relevance
        results = OrderedDict()
        for result in soup.find_all('section', class_="wide"):
            # if encountered 'style' attribute result, it's an ad - skip
            if result.has_attr('style'): continue
            # replace &shy; (which highlights syllables) with empty string
            word = result.find('a').get_text().replace(u'\xAD', str())
            desc = shorten(result.find('p').get_text(), width=55)
            results[word] = desc
        return results

    def __get_details(self, word):
        # TODO
        r = get(DETAIL_URL.format(word))
        # if word is not found in dictionary, status code 404 is returned
        if r.status_code == 404:
            raise WordNotFoundException()
        soup = BeautifulSoup(r.text, 'lxml')
        titel = soup.select("#block-system-main > h1:nth-child(2)").get_text()
        wortart = soup.select("strong.lexem:nth-child(2)").get_text()

class WordNotFoundException(Exception):
    """Exception that is raised when the requested word was not found."""
    pass
