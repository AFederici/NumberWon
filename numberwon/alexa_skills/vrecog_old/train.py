from mfcc import *
# from mfcc2 import *
from LBG import *
# from LBG2 import generate_codebook as lbg
import matplotlib.pyplot as plt
import scipy.io.wavfile
import scipy.cluster.vq
from glob import glob
import os
import scikits.talkbox.features

train  = glob(os.path.join("data/train", "*.wav"))
test  = glob(os.path.join("data/test", "*.wav"))
# train_ceps = [(loadfile(tt),i) for i, tt in enumerate(train)]
# print(train_ceps[0][0].shape)
# train_ceps2 = [loadfile2(tt) for tt in train]
# test_ceps = [(loadfile(tt),i) for i, tt in enumerate(test)]
# print(ceps[0])
# print(train_ceps[6][0].shape)
# show_MFCC(train_ceps[3][0])
# show_MFCC(test_ceps[3][0])

# show_MFCC_spectrum(ceps[5])
# gmmm = EDSet()
# for ceps, ids in train_ceps:
    # show_MFCC(ceps)
    # gmmm.fit_new(ceps, ids)
# for ceps, ids in test_ceps:
#     # show_MFCC(ceps)
#     gmmm.fit_new(ceps, ids)
#
# print(gmmm.predict_one(train_ceps[6][0]))
nSpeaker = 8
nfiltbank = 12
nCentroid = 16
codebooks_mfcc = np.empty((nSpeaker,nfiltbank,nCentroid))
for i, fname in enumerate(train):
    # print(fname)
    sample_rate, X = scipy.io.wavfile.read(fname)
    # mel_coeff = mfcc(s, fs, nfiltbank)
    mel_coeff = scikits.talkbox.features.mfcc(X,sample_rate)[0]
    # print(len(mel_coeff))
    # mel_coeff = np.rot90(extract(s))
    # mel_coeff = extract(s)
    # plt.imshow(mel_coeff.T, aspect="auto", interpolation="none")
    # plt.title("MFCC features")
    # plt.xlabel("Frame")
    # plt.ylabel("Dimension")
    # plt.show()
    print(mel_coeff.shape,np.array(lbg(mel_coeff, nCentroid)).shape)
    codebooks_mfcc[i,:,:] = lbg(mel_coeff, nCentroid)  # VQ Quantization
    # mel_coeff = scipy.cluster.vq.whiten(mel_coeff)
    # print(scipy.cluster.vq.kmeans2(mel_coeff,nCentroid))
    # codebooks_mfcc[i,:,:] = scipy.cluster.vq.kmeans2(mel_coeff,nCentroid)[0]
    #
    # plt.figure(i)
    # plt.title('Codebook for speaker ' + str(i+1) + ' with ' + str(nCentroid) + ' centroids')
    #
    # for j in range(nCentroid):
    #     plt.stem(codebooks_mfcc[i,:,j])
    #     plt.ylabel('MFCC')
    #     plt.axis(ymin = -1, ymax = 1)
    #     plt.xlabel('Number of features')

# plt.show()
print 'Training complete'
# print(codebooks_mfcc.shape)
# def minDistance(features, codebooks):
#     speaker = 0
#     distmin = np.inf
#     for k in range(np.shape(codebooks)[0]):
#         D = EUDistance(features, codebooks[k,:,:])
#         dist = np.sum(np.min(D, axis = 1))/(np.shape(D)[0])
#         if dist < distmin:
#             distmin = dist
#             speaker = k
#     return speaker
# numCorrect = 0;
# for i, fname in enumerate(test):
#     # print(fname)
#     (fs,s) = sample_rate, X = scipy.io.wavfile.read(fname)
#     # mel_coeff = mfcc(s, fs, nfiltbank)
#     mel_coeff = np.rot90(extract(s))
#     # mel_coeff = lbg(mel_coeff, nCentroid)
#     sp_mfcc = minDistance(mel_coeff, codebooks_mfcc)
#     print 'Speaker', (i+1), ' in test matches with speaker ', (sp_mfcc+1), 'in train for training with MFCC'
#     if i == sp_mfcc:
#         numCorrect += 1
# print(numCorrect)


# codebooks = np.empty((2, nfiltbank, nCentroid))
# mel_coeff = np.empty((2, nfiltbank, 68))
#
# for i in range(2):
#     (fs,s) = scipy.io.wavfile.read(train[i])
#     # mel_coeff[i,:,:] = mfcc(s, fs, nfiltbank)[:,0:68]
#     mel_coeff[i,:,:] = np.rot90(extract(s))[:,0:68]
#     codebooks[i,:,:] = lbg(mel_coeff[i,:,:], nCentroid)
#     print(codebooks)
#
# plt.figure(nSpeaker + 1)
# s1 = plt.scatter(mel_coeff[0,4,:], mel_coeff[0,5,:], s = 100, color = 'r', marker = 'o')
# c1 = plt.scatter(codebooks[0,4,:], codebooks[0,5,:], s = 100, color = 'r', marker = '+')
# # plt.show()
# # plt.figure(nSpeaker + 2)
# s2 = plt.scatter(mel_coeff[1,4,:], mel_coeff[1,5,:], s = 100, color = 'b', marker = 'o')
# c2 = plt.scatter(codebooks[1,4,:], codebooks[1,5,:], s = 100, color = 'b', marker = '+')
# # plt.grid()
# # plt.legend((s1, s2, c1, c2), ('Sp1','Sp2','Sp1 centroids', 'Sp2 centroids'),scatterpoints=1,
# # loc = 'lower right')
# plt.show()

# (fs,s) = scipy.
io.wavfile.read(train[0])
# mel_coeff = np.empty((1, nfiltbank, 68))
# codebooks_mfcc = np.empty((nSpeaker,nfiltbank,nCentroid))
# codebooks = np.empty((1, 16, 68))
# # mel_coeff[0,:,:] = np.rot90(extract(s))[:,0:68]
# mel_coeff[0,:,:] = mfcc(s, fs, nfiltbank)[:,0:68]
# codebooks[0,:,:] = lbg(mel_coeff[0,:,:], nCentroid)
# print(mel_coeff[0,:,:].ndim,np.array(codebooks).shape)
# plt.figure(nSpeaker + 1)
# # s1 = plt.scatter(mel_coeff[0,4,:], mel_coeff[0,5,:], s = 100, color = 'r', marker = 'o')
# c1 = plt.scatter(codebooks[0,4,:], codebooks[0,5,:], s = 100, color = 'r', marker = '+')
# plt.show()
