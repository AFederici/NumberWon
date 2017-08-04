from flask import Flask
from flask_ask import Ask, statement, question, session
from face.FaceRec import Face_Recognition
from face.database import Database
from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from profile_skills import update_current_user

app = Flask(__name__)
ask = Ask(app, '/')

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
        msg = "Hello {}. Would you like a book reccomendaton based on your preferences?".format(session.attributes["Current_User"])
    print("current user: ", session.attributes["Current_User"])
    return question(msg)

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    book_pref = ud.get_preferences_by_user(session.attributes["Current_User"], "book")
    if book_pref is None:
        msg = "Could not find any preferences for books."
        return statement(msg)
    else:
        if len(book_pref)-1 == 0:
            ind = 0
        else:
            ind = np.random.randint(0, len(book_pref)-1)
        title, desc = find_genres(book_pref[ind])
    if title == "":
        msg = "I'm sorry. I couldn't find anything. Please try again."
        return statement(msg)
    else:
        msg = "I found a book titled {} based on your preference of {}.".format(title, book_pref[ind])
        return statement(msg).simple_card(title=title, content=desc)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "My apologies."
    return statement(msg)

def find_genres(term):
    """ """
    term = term.strip()
    term = term.lower()
    site = "https://www.goodreads.com/genres/" + term
    #print(site)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    url = []
    for link in soup.find_all('a'):
        if link.get('href')[:11] == "/book/show/": 
            url.append("https://www.goodreads.com"+ str(link.get('href')))
    ind = np.random.randint(0, len(url)-1)
    req2 = Request(url[ind], headers=hdr)
    page2 = urlopen(req2)
    soup2 = BeautifulSoup(page2, "lxml")
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
        if tags[:18] == "<span id=\"freeText" and tags[18] != "C":
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
    button = soup2.find(id="buyButton")
    if not button is None:
        button = button.get('href')
        button = "https://www.goodreads.com" + str(button)
    print(button)
    return title_str.replace("\n", "").strip(), desc_str_2

#cover_imgs = soup2.find_all('img')
#cover_img = "ci"
#for imgs in cover_imgs:
    # print(str(imgs)[:19])
    #if str(imgs)[:19] == "<img id=\"coverImage":
        #cover_img = imgs.get('src')
        #print(str(cover_img))

if __name__ == '__main__':
    app.run(debug=True)