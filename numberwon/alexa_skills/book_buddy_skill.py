from flask import Flask
from flask_ask import Ask, statement, question, session
from face.FaceRec import Face_Recognition
from face.database import Database
from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

ud = UserDatabase("profiles/profiles_test_database.npy")

@app.route('/')
def homepage():
    return "book buddy"

@ask.launch
def start_skill():
    if not "Current_User" in session.attributes:
        session.attributes["Current_User"] = None
    update_current_user()
    if session.attributes["Current_User"] is None:
        msg = "I could not find a user I recognize. Please add a user or try again."
        return statement(msg)
    else:
        msg = "Would you like a book reccomendaton based on your preferences?"
    print("current user: ", session.attributes["Current_User"])
    return question(msg)

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    #gets pref catagories in current user
    #sees if books is one of them
    #if not, ends
    #if yes, finds genres and gets random
        #checks for incorrect term
    #has a card as well that has the complete description (and cover???)
    #also maybe asks "would you like to order"???

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "My apologies."
    return statement(msg)

def find_genres(term):
    """ """
    term = term.strip()
    term = term.lower()
    site = "https://www.goodreads.com/genres/" + term
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html5lib")
    url = []
    for link in soup.find_all('a'):
        if link.get('href')[:11] == "/book/show/": 
            url.append("https://www.goodreads.com"+ str(link.get('href')))
    ind = np.random.randint(0, len(url)-1)
    req2 = Request(url[ind], headers=hdr)
    page2 = urlopen(req2)
    soup2 = BeautifulSoup(page2, "html5lib")
    title = str(soup2.find(id="bookTitle"))
    foundclose = False
    title_str = ""
    for i in range(len(title)):
        if foundclose and title[i] == "<" and i > 0:
            break
        if foundclose:
            title_str += title[i]
        if title[i] == ">" and not foundclose:
            foundclose = True
    desc = soup2.find_all("span")
    desc_str = ""
    for tags in desc:
        tags = str(tags)
        if tags[:18] == "<span id=\"freeText" and tags[18] != "C": #and tags['id'][:8] == "freeText" and tags['id'][8] != "C"
            desc_str = tags
            break
            
    foundclose = False
    desc_str = desc_str.replace("<br>", "")
    desc_str = desc_str.replace("<br/>", "")
    desc_str = desc_str.replace("<i/>", "")
    desc_str = desc_str.replace("<i>", "")
    desc_str_2 = ""
    for x in range(len(desc_str)):
        if foundclose and desc_str[x] == "<" and i > 0:
            break
        if foundclose:
            desc_str_2 += desc_str[x]
        if desc_str[x] == ">" and not foundclose:
            foundclose = True
    return title_str.replace("\n", "").strip(), desc_str_2

'''
uses alexa Cards to display something
'''