import numpy as np
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from collections import defaultdict, Counter
#import html2text


def find_fanfiction(terms, top=1):
    """ samples "top" fanfictions from Wattpad and stores them in a dictionary.
    #warning: runs really slow

        Parameters
        -----------
        term: String
        relevant term, category, or genre of which you sample off Wattpad

        optional- top: int
        specifics the number of fanfictions you sample, up to 15

        Returns
        -------
        Dict[String, String] of raw texts
        key: term (i.e. "harry potter")
        value: raw text of all fanfictions sampled

        """
    search = ""
    for i in terms:
        i = i.strip()
        i = i.lower()
        i = i.replace(" ", "+")
        print(i)
        search += "+" + str(i)
    site = "http://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search%5Bquery%5D=" + search
    '''hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    for link in soup.find_all('a', 'on-result')[:top]:  # if too slow just take 1st or second link'''
    '''

        
            url = "https://www.wattpad.com" + link["href"] + "/parts"
            req = Request(url, headers=hdr)
            page = urlopen(req)
            soup2 = BeautifulSoup(page, "lxml")
            for link2 in soup2.find_all('ul', 'table-of-contents'):
                z = link2.find_all('a', href=True)
                listing = [ele["href"] for ele in z]
                d = defaultdict(BeautifulSoup)
                for x in listing:
                    list2 = BeautifulSoup(urlopen(Request("https://www.wattpad.com" + x, headers=hdr)),
                                          "lxml").find_all('p')

                    paragraph = [str(j)[str(j).index('>') + 1:str(j).rfind('<')] for j in list2 if
                                 "data-p-id" in str(j)]
                    final[term] += "<p>"
                    final[term] += "</p> <p>".join(paragraph)
        return final'''
    return site