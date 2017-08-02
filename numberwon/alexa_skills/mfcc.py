from numpy import *
from numpy.linalg import *
from matplotlib.pyplot import *
from glob import glob
import os
from scikits.talkbox.features import mfcc
import scipy.io.wavfile
from scipy.spatial import distance
from sklearn.mixture import GMM
import operator

def hamming(n):
    """
    Generate a hamming window of n points as a numpy array.
    """
    return 0.54 - 0.46 * cos(2 * pi / n * (arange(n) + 0.5))

def melfb(p, n, fs):
    """
    Return a Mel filterbank matrix as a numpy array.
    Inputs:
        p:  number of filters in the filterbank
        n:  length of fft
        fs: sample rate in Hz
    Ref. http://www.ifp.illinois.edu/~minhdo/teaching/speaker_recognition/code/melfb.m
    """
    f0 = 700.0 / fs
    fn2 = int(floor(n/2))
    lr = log(1 + 0.5/f0) / (p+1)
    CF = fs * f0 * (exp(arange(1, p+1) * lr) - 1)
    bl = n * f0 * (exp(array([0, 1, p, p+1]) * lr) - 1)
    b1 = int(floor(bl[0])) + 1
    b2 = int(ceil(bl[1]))
    b3 = int(floor(bl[2]))
    b4 = min(fn2, int(ceil(bl[3]))) - 1
    pf = log(1 + arange(b1,b4+1) / f0 / n) / lr
    fp = floor(pf)
    pm = pf - fp
    M = zeros((p, 1+fn2))
    for c in range(b2-1,b4):
        r = int(fp[c] - 1)
        M[r,c+1] += 2 * (1 - pm[c])
    for c in range(b3):
        r = int(fp[c])
        M[r,c+1] += 2 * pm[c]
    return M, CF

def dctmtx(n):
    """
    Return the DCT-II matrix of order n as a numpy array.
    """
    x,y = meshgrid(range(n), range(n))

    D = sqrt(2.0/n) * cos(pi * (2*x+1) * y / (2*n))
    D[0] /= sqrt(2)
    return D

FS = 16000                              # Sampling rate
FRAME_LEN = int(0.02 * FS)              # Frame length
FRAME_SHIFT = int(0.01 * FS)            # Frame shift
FFT_SIZE = 2048                         # How many points for FFT
WINDOW = hamming(FRAME_LEN)             # Window function
PRE_EMPH = 0.95                         # Pre-emphasis factor

BANDS = 40                              # Number of Mel filters
COEFS = 13                              # Number of Mel cepstra coefficients to keep
POWER_SPECTRUM_FLOOR = 1e-100           # Flooring for the power to avoid log(0)
M, CF = melfb(BANDS, FFT_SIZE, FS)      # The Mel filterbank matrix and the center frequencies of each band
D = dctmtx(BANDS)[1:COEFS+1]            # The DCT matrix. Change the index to [0:COEFS] if you want to keep the 0-th coefficient
invD = inv(dctmtx(BANDS))[:,1:COEFS+1]  # The inverse DCT matrix. Change the index to [0:COEFS] if you want to keep the 0-th coefficient
nr_mixture = 32 # Number of components in the GMM
train  = glob(os.path.join("data/train", "*.wav"))
test  = glob(os.path.join("data/test", "*.wav"))


def extract(x, show = False):
    """
    Extract MFCC coefficients of the sound x in numpy array format.
    """
    if x.ndim > 1:
        print "INFO: Input signal has more than 1 channel; the channels will be averaged."
        x = mean(x, axis=1)

    # Normalize the Sequence First
    #total = 0.0
    #for i in x: total += i**2
    #total = sqrt(total / len(x))
    #x = x / total

    frames = (len(x) - FRAME_LEN) / FRAME_SHIFT + 1
    feature = []
    for f in range(frames):
        # Windowing
        frame = x[f * FRAME_SHIFT : f * FRAME_SHIFT + FRAME_LEN] * WINDOW
        # Pre-emphasis
        frame[1:] -= frame[:-1] * PRE_EMPH
        # Power spectrum
        X = abs(fft.fft(frame, FFT_SIZE)[:FFT_SIZE/2+1]) ** 2
        X[X < POWER_SPECTRUM_FLOOR] = POWER_SPECTRUM_FLOOR  # Avoid zero
        # Mel filtering, logarithm, DCT
        X = dot(D, log(dot(M,X)))
        feature.append(X)
    feature = row_stack(feature)
    # Show the MFCC spectrum before normalization
    if show:
        # figure().show()
        subplot(2,1,2)
        show_MFCC_spectrum(feature)
        # Show the MFCC
        # subplot(2,1,1)
        show_MFCC(feature)
        draw()
    # Mean & variance normalization
    if feature.shape[0] > 1:
        mu = mean(feature, axis=0)
        sigma = std(feature, axis=0)
        feature = (feature - mu) / sigma
    return feature

def show_MFCC(mfcc):
    """
    Show the MFCC as an image.
    """
    # print(mfcc.T)
    imshow(mfcc.T, aspect="auto", interpolation="none")
    title("MFCC features")
    xlabel("Frame")
    ylabel("Dimension")
    show()

def show_MFCC_spectrum(mfcc):
    """
    Show the spectrum reconstructed from MFCC as an image.
    """
    imshow(dot(invD, mfcc.T), aspect="auto", interpolation="none", origin="lower")
    title("MFCC spectrum")
    xlabel("Frame")
    ylabel("Band")
    show()

def loadfile(wav):
    sample_rate, X = scipy.io.wavfile.read(wav)
    # cep, mspec, spec = mfcc(X,sample_rate)
    cep = extract(X)
    return cep

class GMMSet(object):

    def __init__(self, gmm_order = 32):
        self.gmms = []
        self.gmm_order = gmm_order
        self.y = []

    def fit_new(self, x, label):
        self.y.append(label)
        gmm = GMM(self.gmm_order)
        gmm.fit(x)
        # print(gmm)
        self.gmms.append(gmm)

    def gmm_score(self, gmm, x):
        return np.sum(gmm.score(x))

    def predict_one(self, x):
        scores = [self.gmm_score(gmma, x) / len(x) for gmma in self.gmms]
        print(scores)
        p = sorted(enumerate(scores), key=operator.itemgetter(1), reverse=True)
        p = [(str(self.y[i]), y, p[0][1] - y) for i, y in p]
        result = [(self.y[index], value) for (index, value) in enumerate(scores)]
        p = max(result, key=operator.itemgetter(1))
        return p[0]
from sklearn.metrics.pairwise import cosine_similarity
class EDSet():
    def __init__(self, gmm_order = 32):
        self.fps = []
        self.y = []

    def fit_new(self, x, label):
        self.y.append(label)
        self.fps.append(x)

    def fp_score(self, fp, x):
        print(fp.shape,x.shape)
        A=fp
        B=x
        return cosine_similarity(fp,x)
        # return sum(scipy.spatial.distance.cdist(fp, x, 'cosine'))
        # return np.dot(A/norm(A, axis=1)[...,None],(B/np.linalg.norm(B,axis=1)[...,None]).T)

    def predict_one(self, x):
        scores = [self.fp_score(fp, x) / len(x) for fp in self.fps]
        print(scores)
        p = sorted(enumerate(scores), key=operator.itemgetter(1), reverse=True)
        p = [(str(self.y[i]), y, p[0][1] - y) for i, y in p]
        result = [(self.y[index], value) for (index, value) in enumerate(scores)]
        p = max(scores)
        return p


train_ceps = [(loadfile(tt),i) for i, tt in enumerate(train)]
# train_ceps2 = [loadfile2(tt) for tt in train]
test_ceps = [(loadfile(tt),i) for i, tt in enumerate(test)]
# print(ceps[0])
# print(train_ceps[6][0].shape)
# show_MFCC(train_ceps[3][0])
# show_MFCC(test_ceps[3][0])



# show_MFCC_spectrum(ceps[5])
gmmm = EDSet()
for ceps, ids in train_ceps:
    # show_MFCC(ceps)
    gmmm.fit_new(ceps, ids)
# for ceps, ids in test_ceps:
#     # show_MFCC(ceps)
#     gmmm.fit_new(ceps, ids)
#
print(gmmm.predict_one(train_ceps[6][0]))
