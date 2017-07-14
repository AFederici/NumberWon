import numpy as np
import librosa
from pathlib import Path
import microphone

class Audio:
    """The Audio Class"""

    def read_files(self, *song):
        """ Reads a string, either a song path or a directory, and appends it to a list of songs paths
            leading to songs the user wants to load eventually

                Parameters
                ----------
                song : song paths or folder full of songs (mp3)

                Returns
                -------
                song_array: 2d Numpy array of str, each a path to a song """

        song_names = np.array([])
        for i in range(len(song)):
            stri = song[i]
            if stri[-3:] == 'mp3':
                song_names = np.append(song_names, stri)

            else:
                p = Path(song[i])
                songs = sorted(p.glob('*.mp3'))
                for s in range(len(songs)):
                    song_names = np.append(song_names, songs[s].name)
        return song_names

    def load_files(self, filename, sampling_rate=44100):
        """ Reads a string as a song path and converts it to samples
                Parameters
                ----------
                filename : song path
                sampling_rate : int

                Returns
                -------
                samples:  Numpy array of samples"""

        samples, fs = librosa.load(filename, sr=sampling_rate, mono=True)
        return samples

    def mic_input(self, time):
        """ Listens with mic and returns sampled np array of input
                Parameters
                ----------
                time : time in seconds to record

                Returns
                -------
                sampled_input: Numpy array """
        byte_encoded_signal, sampling_rate = record_audio(time)
        sampled_input = np.array([])
        for i in range(len(byte_encoded_signal)):
            byte_string = np.fromstring(byte_encoded_signal[i], dtype=np.int16)
            sampled_input = np.hstack((sampled_input, byte_string))
        return sampled_input