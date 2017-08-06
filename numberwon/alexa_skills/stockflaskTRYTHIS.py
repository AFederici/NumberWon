from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json
import numpy as np
#from profiles.Profiles.Profile import Profile
#from profiles.Profiles.UserDatabase import UserDatabase
#from face.FaceRec import Face_Recognition
#from profile_skills import update_current_user
#from face.database import Database

app = Flask(__name__)
ask = Ask(app, '/')
#ud = UserDatabase("profiles/profiles_test_database.npy")

from stock_final import Stocks 
s = Stocks()
s.fill()

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    #if not "Current_User" in session.attributes:
    #    session.attributes["Current_User"] = None
    #update_current_user()
    #if session.attributes["Current_User"] is None:
    #    msg = "I could not find a user I recognize."
    #    return statement(msg)
    #else:
    #    msg = "Hi " + session.attributes["Current_User"] + ". Are you interested in reading some fanfiction made just for you?"
    #print("current user: ", session.attributes["Current_User"])
    msg = "Are you interested in hearing about Stocks"
    
    ############## NEW #######################
    l = ['apple','google','raytheon']
    s.set_my_stocks(l)
    ##########################################
    return question(msg)

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    msg = "Okay, which companies from the S and P 500 would you like to hear about"
    return question(msg)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "No problem. Have a nice day."
    return statement(msg)

@ask.intent("StockIntent")
def get_stock(stocks):
    if stocks == "my stocks":
        session.attributes['company_names'] = s.get_my_stocks()
        print('hello')
        numbs = s.my_companies()
        comp_closes = zip(session.attributes['company_names'], numbs)
        msg = ""
        for a,b in comp_closes:
            msg += "{} closed at ${}. ".format(a,b[0])
        msg += " What else would you like to hear about? Ask for help if you want some ideas"
    else:
        numbs = s.search(stocks)
        session.attributes['company_names'] = stocks
        msg = "The recent close for {} was ${}. What else would you like to hear about? Ask for help if you want some ideas".format(session.attributes['company_names'] , numbs[0])
    return question(msg)

@ask.intent("InformationIntent")
def get_info(information):
    
 #############################################################################################
    msg = ""
    company_to_work_with = [session.attributes['company_names']]
    s.set_my_stocks(company_to_work_with[0])
    if information == "simple moving average":
        #if len(company_to_work_with[0]) > 1:
        #    s.set_my_stocks(company_to_work_with[0])
        #    numbs = s.my_companies()
        #    for i in range(len(company_to_work_with)):
        for i in s.get_my_stocks():
            numbs = s.search(i)
            msg += "In the past {} days, the high for {} was ${}, with a 100 day moving average of ${}. ".format(numbs[2], i, numbs[1], numbs[3][-1][-1])  #[2],[],[1] 
                
    if information == 'performance':
        for i in s.get_my_stocks():
            numbs = s.search(i)
            msg += "{} has been {}".format(i, numbs[5])
            
        msg += " This is based off of the derivative of the 50 day simple moving average."
    if information == 'trends':
        for i in s.get_my_stocks():
            numbs = s.search(i)
            msg += "By analyzing {}, I conclude that it has been {} based off of the smoothed data. ".format(i, numbs[4])
            
            
  #############################################################################################
        #else:
        #    numbs = s.search(company_to_work_with[0])
        #    msg += "In the past {} days, the high for {} was ${}. also, moving average of ${} as of {}. ".format(numbs[2], company_to_work_with[0], numbs[1], numbs[3][-1][-1], numbs[3][-1].keys()[-1].date())   
    return statement(msg)

@ask.intent("HelpIntent")
def retreive_options(ask):
    msg = "I know the simple moving average for 5, 10, 20, 50, and 100 days.  I can also tell you about general trends or statistics that I have been trained to find. If you want to have fun, I can tell you my investment recommendations, hehe!"
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)