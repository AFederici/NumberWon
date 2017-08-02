import numpy as np
import scipy.io.wavfile
from scikits.talkbox.features import mfcc
from glob import glob
import os

train  = glob(os.path.join("data/train", "*.wav"))
test  = glob(os.path.join("data/test", "*.wav"))

def loadfile(wav):
    sample_rate, X = scipy.io.wavfile.read(wav)
    cep, mspec, spec = mfcc(X)
    return cep

ceps = [loadfile(tt) for tt in train]
print(ceps[0])

def dctmtx(n):
    """
    Return the DCT-II matrix of order n as a numpy array.
    """
    x,y = meshgrid(range(n), range(n))

    D = sqrt(2.0/n) * cos(pi * (2*x+1) * y / (2*n))
    D[0] /= sqrt(2)
    return D

def extract(wav):
    """
    Extract MFCC coefficients of the sound x in numpy array format.
    """
    sample_rate, signal = scipy.io.wavfile.read(wav)
    FRAME_LEN = 32
    FRAME_SHIFT = 16
    PRE_EMPH = .95
    FFT_SIZE = 2048
    POWER_SPECTRUM_FLOOR = 1e-100
    coefs = 15
    D = dctmtx[1: coefs + 1]
    window = 0.54 - 0.46 * np.cos(2 * np.pi / FRAME_LEN * (np.arange(FRAME_LEN) + 0.5))

    if signal.ndim > 1:
        print("INFO: Input signal has more than 1 channel; the channels will be averaged.")
        signal = mean(signal, axis=1)
    # assert len(signal) > 5 * FRAME_LEN, "Signal too short!"
    frames = (len(signal) - FRAME_LEN) / FRAME_SHIFT + 1
    feature = []
    for f in xrange(frames):
        # Windowing
        frame = signal[f * FRAME_SHIFT : f * FRAME_SHIFT +
                       FRAME_LEN] * window
        # Pre-emphasis
        frame[1:] -= frame[:-1] * PRE_EMPH
        # Power spectrum
        X = abs(np.fft.fft(frame, FFT_SIZE)[:FFT_SIZE / 2 + 1]) ** 2
        X[X < POWER_SPECTRUM_FLOOR] = POWER_SPECTRUM_FLOOR  # Avoid zero
        # Mel filtering, logarithm, DCT
        X = np.dot(D, log(dot(M, X)))
        feature.append(X)
    feature = row_stack(feature)
    # Show the MFCC spectrum before normalization
    # Mean & variance normalization
    if feature.shape[0] > 1:
        mu = mean(feature, axis=0)
        sigma = std(feature, axis=0)
        feature = (feature - mu) / sigma

    return feature

ceps = [extract(tt) for tt in train]
print(ceps[0])
