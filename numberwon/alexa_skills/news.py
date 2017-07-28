from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. What would you like to hear about the news?"
    return question(msg)

def get_headlines():
    return "Newsy news, blah blah weather news news."

@ask.intent("AMAZON.YesIntent")
def share_headlines():
    return question("What would you like to know more about?")

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

@ask.intent("NewsIntent")
def news_intent(NewsTitle):
    headline  = get_headlines(NewsTitle)
    msg = "Tops news on {}: {}".format(NewsTitle,headline)
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
