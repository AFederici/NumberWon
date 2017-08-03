from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from flask import Flask
from flask_ask import Ask, statement, session, question

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. Would you like to generate a random name?"
    return question(msg)

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    msg = "What gender would you like your random name to be?"
    return question(msg)

@ask.intent("AMAZON.NoIntent")
