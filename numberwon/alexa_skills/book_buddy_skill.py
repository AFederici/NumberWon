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

#TO DO:
#check if site is bad
#incorporate links/book covers?
#document

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
        title, desc, link, img = find_genres(book_pref[ind])
    if title == "":
        msg = "I'm sorry. I couldn't find anything. Please try again."
        return statement(msg)
    else:
        msg = "I found a book titled {} based on your preference of {}.".format(title, book_pref[ind])
        print(img)
        return statement(msg).simple_card(title=title, context=desc)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "My apologies."
    return statement(msg)

def find_genres(term):
    """ """
    #get site
    term = term.strip()
    term = term.lower()
    site = "https://www.goodreads.com/genres/" + term
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    #check if site is bad
    #soup.find_all('div')
    url = []
    #get random book
    for link in soup.find_all('a'):
        if link.get('href')[:11] == "/book/show/": 
            url.append("https://www.goodreads.com"+ str(link.get('href')))
    ind = np.random.randint(0, len(url)-1)
    req2 = Request(url[ind], headers=hdr)
    #get title of book
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
    #description     
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
    #buy link
    button = soup2.find(id="buyButton")
    if not button is None:
        button = button.get('href')
        button = "https://www.goodreads.com" + str(button)
    #cover images
    cover_imgs = str(soup2.find_all(id='topcol'))
    cover_img = ""
    src_found = False
    for imgs in range(len(cover_imgs)):
        if imgs+2 <= (len(cover_imgs) - 1):
            check = str(cover_imgs[imgs-5:imgs])
        else:
            break
        if check == "src=\"":
            src_found = True     
        if src_found and cover_imgs[imgs] == "\"":
            break
        if src_found:
            cover_img += cover_imgs[imgs]
    print(button)
    print(cover_img)
    return title_str.replace("\n", "").strip(), desc_str_2, button, cover_img


if __name__ == '__main__':
    app.run(debug=True)