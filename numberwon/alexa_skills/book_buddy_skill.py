import numpy as np
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from collections import defaultdict, Counter

def find_genres(term, top=100):
    """ """
    term = term.strip()
    term = term.lower()
    site = "https://www.goodreads.com/genres/" + term
    #hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site)
    page = urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    url = []
    print(soup.find_all('a', 'on-result'))
    for link in soup.find_all('a', 'on-result')[:top]:  # if too slow just take 1st or second link
        print("link " + str(link))
        url.append("https://www.goodreads.com/genres/" + link["href"])
    return url

'''
uses alexa Cards to display something
'''

def find_books_like(book, top=1):
    pass
    