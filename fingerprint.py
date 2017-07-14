import numpy as np
import librosa
import microphone
from collections import Counter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure

class FingerPrint():

    def find_peaks(self, S, freqs):
        """ Listens with mic and returns sampled np array of input
                Parameters
                ----------
                S : list of samples
                freqs : frequencies of the samples

                Returns
                -------
                peaks: np array of peaks"""
        ys, xs = np.histogram(S.flatten(), bins=len(freqs)//2, normed=True)
        dx = xs[-1] - xs[-2]
        cdf = np.cumsum(ys)*dx  # this gives you the cumulative distribution of amplitudes
        cutoff = xs[np.searchsorted(cdf, 0.77)]
        foreground = S >= cutoff

        struct = generate_binary_structure(2, 1)
        neighborhood = iterate_structure(struct, 20)
        local = S == maximum_filter(S, footprint=neighborhood)
        peaks = local & foreground
        peaks = np.argwhere(peaks)
        return peaks

    def fingerprinting(self, peaks_insert, dictionary, song_id):
        for index, freq_time in enumerate(peaks_insert):
            try:
                dict_test = peaks_insert[index:index + 20]
                # peaks_insert[index] = f_1
                for index2, freq_time2 in dict_test:
                    dictionary[(peaks_insert[index], peaks_insert[index2], freq_time2 - freq_time)].append(
                        (song_id, freq_time))
            except:
                print(index)
                print(len(peaks_insert))
                break
        return dictionary

    def compare(self, database, peaks_sample):
        # going to take

        # Counter(elem[0] for elem in list1)
        # peaks: [(time, freq)]

        # still need to generate features

        mostCommon = []
        for index, freq_time in enumerate(peaks_sample):
            time, freq = freq_time
            try:
                time2, freq2 = peaks_sample[index + 1]
                appending = database[(
                freq, freq2, time2 - time)]  # list of song_id's and times that correspond to frequencies and delta t
                # going through appending
                for tup in appending:
                    time_new = time - tup[1]
                    mostCommon.append((tup[0], np.round(time_new, 2)))
            except:
                print(index)
                print(len(peaks))
                break
                # t*-t1, t*-t2, offset should be the same
                # t1 and t2 are times in the database

                #         most = Counter.most_common(10) #for debugging
                #         print(most) #for debugging
                #         first = most[0] #for debugging
                #         return first[0]
        return Counter.most_common(1)[0]
