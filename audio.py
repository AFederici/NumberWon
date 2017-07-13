import matplotlib.mlab as mlab
import librosa
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
digital, fs = librosa.load(r"/Users/huangfamily/Downloads/music to import/mof.mp3", sr=44100, mono=True)

# S, freqs, times= mlab.specgram(digital, NFFT=4096, Fs=fs,
#                                                     window=mlab.window_hanning,
#                                                     noverlap=(4096 // 2))
S, freqs, times, im = ax.specgram(digital, NFFT=4096, Fs=fs,
                                                      window=mlab.window_hanning,
                                                      noverlap=(4096 // 2))

fig.colorbar(im)  # adds colorbar to figure

# ck =  np.fft.rfft(digital)
# L = len(digital) / 44100
# k = np.arange(len(ck)) / L
# ax.plot(k[::1000],np.abs(ck[::1000]))
