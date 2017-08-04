import librosa
path='data/ss/_christine'
y, sr = librosa.load(path+'.wav')
for i in range(1,17):
    if i == 4:
        librosa.output.write_wav('{}_{}.wav'.format(path,i), y, sr)
    else:
        y_stretch = librosa.effects.time_stretch(y, (i*2/16)+.5)  # .5 to 2.5 factor
        librosa.output.write_wav('{}_{}.wav'.format(path,i), y_stretch, sr)
