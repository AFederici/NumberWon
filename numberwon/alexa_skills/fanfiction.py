import numpy as np
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from collections import defaultdict, Counter
import html2text

class Fanfiction:
    def __init__(self):
        s = None
    def ultimate_function(self, term, fanfiction_dict):
        for key, value in fanfiction_dict.items():
            lm = self.train_lm(value, 10)
            self.text = html2text.html2text(self.generate_text(lm, 10, n_letters=200))
            a = open(term + '.txt', 'w')
            a.write(self.text)
            a.close()
    def find_fanfiction(self, term, top=1):
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
        site = "https://www.wattpad.com/search/" + term
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        final = defaultdict(str)

        for link in soup.find_all('a', 'on-result')[:top]:  # if too slow just take 1st or second link
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
        return final

    def unzip(self, pairs):
        """Splits list of pairs (tuples) into separate lists.

        Example: pairs = [("a", 1), ("b", 2)] --> ["a", "b"] and [1, 2]

        This should look familiar from our review back at the beginning of week 1
        :)
        """
        return tuple(zip(*pairs))

    def normalize(self, counter):
        """ Convert counter to a list of (letter, frequency) pairs, sorted in descending order of frequency.

            Parameters
            -----------
            counter: A Counter-instance

            Returns
            -------
            A list of tuples - (letter, frequency) pairs.

            For example, if counter had the counts:

                {'a': 1, 'b': 3}

            `normalize(counter)` will return:

                [('b', 0.75), ('a', 0.25)]
        """
        total = sum(counter.values())
        return [(char, cnt / total) for char, cnt in counter.most_common()]

    def train_lm(self, text, n):
        """ Train character-based n-gram language model.

            This will learn: given a sequence of n-1 characters, what the probability
            distribution is for the n-th character in the sequence.

            For example if we train on the text:
                text = "cacao"

            Using a n-gram size of n=3, then the following dict would be returned:

                {'ac': [('a', 1.0)],
                 'ca': [('c', 0.5), ('o', 0.5)],
                 '~c': [('a', 1.0)],
                 '~~': [('c', 1.0)]}

            Tildas ("~") are used for padding the history when necessary, so that it's
            possible to estimate the probability of a seeing a character when there
            aren't (n - 1) previous characters of history available.

            So, according to this text we trained on, if you see the sequence 'ac',
            our model predicts that the next character should be 'a' 100% of the time.

           For generatiing the padding, recall that Python allows you to generate
            repeated sequences easily:
               `"p" * 4` returns `"pppp"`

            Parameters
            -----------
            text: str
                A string (doesn't need to be lowercased).
            n: int
                The length of n-gram to analyze.

            Returns
            -------
            A dict that maps histories (strings of length (n-1)) to lists of (char, prob)
            pairs, where prob is the probability (i.e frequency) of char appearing after
            that specific history. For example, if

        """
        raw_lm = defaultdict(Counter)

        history = "~" * (n - 1)

        # count number of times characters appear following different histories
        for x in text:
            raw_lm[history][x] += 1
            history = history[1:] + x
            #print(history)

        # create final dictionary by normalizing
        lm = {history: self.normalize(counter) for history, counter in raw_lm.items()}

        return lm

    def generate_letter(self, lm, history):
        """ Randomly picks letter according to probability distribution associated with
            the specified history.

            Note: returns dummy character "~" if history not found in model.

            Parameters
            ----------
            lm: Dict[str, Tuple[str, float]]
                The n-gram language model. I.e. the dictionary: history -> (char, freq)

            history: str
                A string of length (n-1) to use as context/history for generating
                the next character.

            Returns
            -------
            str
                The predicted character. '~' if history is not in language model.
        """
        if not history in lm:
            return "~"
        letters, probs = self.unzip(lm[history])
        i = np.random.choice(letters, p=probs)
        return i

    def generate_text(self, lm, n, nletters=100):
        """ Randomly generates nletters of text with n-gram language model lm.

            Parameters
            ----------
            lm: Dict[str, Tuple[str, float]]
                The n-gram language model. I.e. the dictionary: history -> (char, freq)
            n: int
                Order of n-gram model.
            nletters: int
                Number of letters to randomly generate.

            Returns
            -------
            str
                Model-generated text.
        """
        history = "~" * (n - 1)
        text = []
        for i in range(nletters):
            c = self.generate_letter(lm, history)
            text.append(c)
            history = history[1:] + c
        return "".join(text)