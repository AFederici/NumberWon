import logging
import os
from flask import Flask
from flask_ask import Ask, statement, question
from audio.audio import Audio
from audio.fingerprint import FingerPrint
from audio.database import Database

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
a = Audio()
ff = FingerPrint()
d = Database(file = "audio/dictionary.npy")

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    """starts by asking a question"""
    msg = "Hello. Would you like me to identify a song?"
    return question(msg)

def get_song():
    """Listens to the microphone recording and compares to the database of songs, returning highest match or none if below threshold"""
    # Don't worry about this implementation yet. Just return a string.
    S1,f1 = a.load_spectrogram(a.mic_input(5))
    return ff.compare(d,ff.find_peaks(S1,f1))

@ask.intent("AMAZON.YesIntent")
def share_headlines():
    """runs if the user says yes"""
    song = get_song()
    song_msg = "The current song is: {}".format(song)
    return statement(song_msg)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    """runs if the user says no"""
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
