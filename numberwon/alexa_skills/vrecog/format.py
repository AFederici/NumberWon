import librosa
path='data/test/_michael' #default
def formataudio():
    y, sr = librosa.load(path+'.wav.ig')
    for i in range(1,17):
        if i == 4:
            librosa.output.write_wav('{}_{}.wav'.format(path,i), y, sr)
        else:
            y_stretch = librosa.effects.time_stretch(y, (i*2/16)+.5)  # .5 to 2.5 factor
            librosa.output.write_wav('{}_{}.wav'.format(path,i), y_stretch, sr)
if __name__ == '__main__':
    path = raw_input("Please enter the file to format\n")
    formataudio()
