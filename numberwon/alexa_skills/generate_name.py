from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from flask import Flask
from flask_ask import Ask, statement, session, question

app = Flask(__name__)
ask = Ask(app, '/')

# gender = "female"
# name_set = "us"
# country = "us"
site = "http://www.fakenamegenerator.com"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, "lxml")

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. Would you like to generate a random name?"
    return question(msg)

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    msg = "What gender would you like your random name to be? You can choose one gender from the following: "
    link_option = soup.find("select", {"id": "gen"}).find_all("option")
    #session.attributes["Link Option"] = link_option
    #print(link_option, "link option")
    value = [x.text for x in link_option]
    #print(value)
    ele = str("\n".join(value)) # last two lines form the options to be displayed on the AlexaApp card
    msg += str(", ".join(value))#reads the options to the user

    return question(msg).simple_card(title='Gender Options', content= "You can choose one gender from the following: \n" + ele)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "Okay. Have a nice day."
    return statement(msg)

@ask.intent("GenderIntent")
def gender(gender_name):
    session.attributes["Gender"] = gender_name.lower()
    link_option = soup.find("select", {"id": "gen"}).find_all("option")
    option_value = [opt["value"] for opt in link_option if gender_name.lower() in opt.text.lower()]  # to be inputted into url
    if len(option_value) == 0:
        return statement("Gender option failed. Try again.")
    session.attributes["Gender_ID"] = option_value[0]

    msg = "What name set would you like to have your name originate from? View options in the Alexa App."
    link_option = soup.find("select", {"id": "n"}).find_all("option")

    value = [x.text for x in link_option]
    ele = "\n".join(value)
    return question(msg).simple_card(title='Name Set Options', content="You can choose one name set from the following: \n" + ele)

@ask.intent("NameSetIntent")
def name(name_set):
    session.attributes["Name Set"] = name_set.lower()
    link_option = soup.find("select", {"id": "n"}).find_all("option")
    option_value = [opt["value"] for opt in link_option if name_set.lower() in opt.text.lower()]  # to be inputted into url
    if len(option_value) == 0:
        return statement("Name set option failed. Try again.")
    session.attributes["NameSet_ID"] = option_value[0]

    msg = "What country would you like to have your name originate from? View options in the Alexa App."
    link_option = soup.find("select", {"id": "c"}).find_all("option")

    value = [x.text for x in link_option]
    ele = "\n".join(value)
    return question(msg).simple_card(title='Country Options', content="You can choose one country from the following: \n" + ele)

@ask.intent("CountryIntent")
def country(country_name):
    session.attributes["Country"] = country_name.lower()
    link_option = soup.find("select", {"id": "c"}).find_all("option")
    option_value = [opt["value"] for opt in link_option if
                    country_name.lower() == opt.text.lower()]  # to be inputted into url
    if len(option_value) == 0:
        return statement("Country option failed. Try again.")
    session.attributes["Country_ID"] = option_value[0]

    site = "http://www.fakenamegenerator.com/gen-" + session.attributes["Gender_ID"] + "-" + session.attributes["NameSet_ID"] + "-" + session.attributes["Country_ID"] + ".php"
    req = Request(site, headers=hdr)
    page = urlopen(req)
    s = BeautifulSoup(page, "lxml")

    name = s.find(attrs = {"class": "info", "class": "address"}).find("h3").text
    msg = name
    return statement(msg).simple_card(title='Generated Name', content="Your randomly generated name is: \n" + name)

if __name__ == '__main__':
    app.run(debug=True)
