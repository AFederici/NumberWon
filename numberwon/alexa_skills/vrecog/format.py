import librosa
path='data/test/' #default
def formataudio():
    y, sr = librosa.load(path+path2+'.wav.ig')
    for i in range(16):
        if i == 4:
            librosa.output.write_wav('{}_{}_{}.wav'.format(path,path2,i+1), y, sr)
        else:
            y_stretch = librosa.effects.time_stretch(y, (i*2/16)+.5)  # .5 to 2.5 factor
            librosa.output.write_wav('{}_{}_{}.wav'.format(path,path2,i+1), y_stretch, sr)
if __name__ == '__main__':
    path2 = raw_input("Please enter the file to format\n")
    formataudio()
