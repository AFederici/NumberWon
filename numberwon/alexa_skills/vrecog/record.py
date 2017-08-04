from sys import byteorder
from array import array
from struct import pack
import librosa

import pyaudio
import wave
import os

THRESHOLD = 2500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in xrange(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    os.system('afplay /System/Library/Sounds/Glass.aiff')
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)
        # print(num_silent,silent,snd_started)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    # r = add_silence(r, 0.2)
    return sample_width, r

def record_to_file(path,train=True): #name
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)
    path2 = 'data/people/'
    wf = wave.open(path2+path+'.wav.ig', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    if train:
        y, sr = librosa.load(path2+path+'.wav.ig')
        for i in range(16):
            if i == 4:
                librosa.output.write_wav('{}_{}_{}.wav'.format(path2,path,i+1), y, sr)
            else:
                y_stretch = librosa.effects.time_stretch(y, (i*2/16)+.5)  # .5 to 2.5 factor
                librosa.output.write_wav('{}_{}_{}.wav'.format(path2,path,i+1), y_stretch, sr)

if __name__ == '__main__':
    print("please speak a word into the microphone")
    record_to_file('demo.wav')
    print("done - result written to demo.wav")
#!/usr/bin/env python

# from scipy.io import wavfile
# import os
# import numpy as np
# import argparse
# from tqdm import tqdm
#
# # Utility functions
#
# def windows(signal, window_size, step_size):
#     if type(window_size) is not int:
#         raise AttributeError("Window size must be an integer.")
#     if type(step_size) is not int:
#         raise AttributeError("Step size must be an integer.")
#     for i_start in xrange(0, len(signal), step_size):
#         i_end = i_start + window_size
#         if i_end >= len(signal):
#             break
#         yield signal[i_start:i_end]
#
# def energy(samples):
#     return np.sum(np.power(samples, 2.)) / float(len(samples))
#
# def rising_edges(binary_signal):
#     previous_value = 0
#     index = 0
#     for x in binary_signal:
#         if x and not previous_value:
#             yield index
#         previous_value = x
#         index += 1
#
# # Process command line arguments
#
# parser = argparse.ArgumentParser(description='Split a WAV file at silence.')
# parser.add_argument('input_file', type=str, help='The WAV file to split.')
# parser.add_argument('--output-dir', '-o', type=str, default='.', help='The output folder. Defaults to the current folder.')
# parser.add_argument('--min-silence-length', '-m', type=float, default=.5, help='The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.')
# parser.add_argument('--silence-threshold', '-t', type=float, default=1e-6, help='The energy level (between 0.0 and 1.0) below which the signal is regarded as silent. Defaults to 1e-6 == 0.0001%.')
# parser.add_argument('--step-duration', '-s', type=float, default=None, help='The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).')
# parser.add_argument('--dry-run', '-n', action='store_true', help='Don\'t actually write any output files.')
#
# args = parser.parse_args()
#
# input_filename = args.input_file
# window_duration = args.min_silence_length
# if args.step_duration is None:
#     step_duration = window_duration / 10.
# else:
#     step_duration = args.step_duration
# silence_threshold = args.silence_threshold
# output_dir = args.output_dir
# output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]
# dry_run = args.dry_run
#
# print "Splitting {} where energy is below {}% for longer than {}s.".format(
#     input_filename,
#     silence_threshold * 100.,
#     window_duration
# )
#
# # Read and split the file
#
# sample_rate, samples = input_data=wavfile.read(filename=input_filename, mmap=True)
#
# max_amplitude = np.iinfo(samples.dtype).max
# max_energy = energy([max_amplitude])
#
# window_size = int(window_duration * sample_rate)
# step_size = int(step_duration * sample_rate)
#
# signal_windows = windows(
#     signal=samples,
#     window_size=window_size,
#     step_size=step_size
# )
#
# window_energy = (energy(w) / max_energy for w in tqdm(
#     signal_windows,
#     total=int(len(samples) / float(step_size))
# ))
#
# window_silence = (e > silence_threshold for e in window_energy)
#
# cut_times = (r * step_duration for r in rising_edges(window_silence))
#
# # This is the step that takes long, since we force the generators to run.
# print "Finding silences..."
# cut_samples = [int(t * sample_rate) for t in cut_times]
# cut_samples.append(-1)
#
# cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in xrange(len(cut_samples) - 1)]
# print(cut_ranges)
# for i, start, stop in tqdm(cut_ranges):
#     print(output_dir)
#     output_file_path = "{}_{:03d}.wav".format(
#         os.path.join(output_dir, output_filename_prefix),
#         i
#     )
#     if not dry_run:
#         print "Writing file {}".format(output_file_path)
#         wavfile.write(
#             filename=output_file_path,
#             rate=sample_rate,
#             data=samples[start:stop]
#         )
#     else:
#         print "Not writing file {}".format(output_file_path)
