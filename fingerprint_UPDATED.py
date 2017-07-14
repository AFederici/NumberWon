import numpy as np
import librosa
import microphone
from collections import Counter


class FingerPrint:
    def fingerprinting(peaks_insert, dictionary, song_id):

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

    def compare(database, peaks_sample):
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
                    mostCommon.append(tup[0], time_new)
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

