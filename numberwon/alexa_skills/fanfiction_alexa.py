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
    msg = "Hi. What kind of fanfiction would you like to view?"
    return question(msg)
