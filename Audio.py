import numpy as np
import librosa
from pathlib import Path
import microphone
import matplotlib.mlab as mlab


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
                song_names: Numpy array of str, each a path to a song """

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

    def load_spectrogram(self, samples, fs):
        """ creates a spectrogram based on the samples and sampling rate WITHOUT the image

                Parameters
                ----------
                samples : np array of samples
                fs : int of sampling rate

                Returns
                -------
                S: 2D array of |c_k| values. Axis-0 (row) is the frequency, axis-1 (col) is the time.
                freqs: an array of frequency values, which allows you to correspond the axis-0 bins to actual frequencies
                times: an array of timevalues, which allows you to correspond the axis-1 bins to actual times """

        S, freqs, times = mlab.specgram(samples, NFFT=4096, Fs=fs, window=mlab.window_hanning, noverlap=(4096 // 2))
        return S, freqs, times
