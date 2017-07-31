
from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json
from search.entityDatabase import entityDatabase

edatb = entityDatabase()
edatb.add_Folder_Database(self, "C:/Users/User/Desktop/beaver/NumberWon/numberwon/alexa_skills/search/*.pickle")
#get links off a page: remove all that contain video
#add all the links as pickle files
