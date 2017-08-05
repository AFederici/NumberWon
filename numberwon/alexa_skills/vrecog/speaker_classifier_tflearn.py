#!/usr/bin/env python
#!/usr/local/bin/python
#!/usr/bin/env PYTHONIOENCODING="utf-8" python
import os
import tensorflow as tf
import tflearn
import vrecog.speech_data as data

# Simple speaker recognition demo, with 99% accuracy in under a minute ( on digits sample )

# | Adam | epoch: 030 | loss: 0.05330 - acc: 0.9966 -- iter: 0000/1000
# 'predicted speaker for 9_Vicki_260 : result = ', 'Vicki'
import tensorflow as tf
print("You are using tensorflow version "+ tf.__version__) #+" tflearn version "+ tflearn.version)
if tf.__version__ >= '0.12' and os.name == 'nt':
	# print("sorry, tflearn is not ported to tensorflow 0.12 on windows yet!(?)")
	quit() # why? works on Mac?

# path='data/spoken_numbers_pcm/'
path='data/people/'
number_classes=0
speakers=None
model=None


def train():
	global speakers, number_classes
	speakers = data.get_speakers(path)
	number_classes=len(speakers)
	print("speakers",speakers)

	# Classification
	tf.reset_default_graph()
	tflearn.init_graph(num_cores=8, gpu_memory_fraction=0.5)

	net = tflearn.input_data(shape=[None, 8192]) #Two wave chunks
	net = tflearn.fully_connected(net, 64)
	net = tflearn.dropout(net, 0.5)
	net = tflearn.fully_connected(net, number_classes, activation='softmax')
	net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')
	global model
	model = tflearn.DNN(net)
	batch=data.wave_batch_generator(batch_size=1000, source=data.Source.DIGIT_WAVES, target=data.Target.speaker,path=path)
	X,Y=next(batch)
	model.fit(X, Y, n_epoch=100, show_metric=True, snapshot_step=100)
	model.save('vrecog/vrecog.tflearn')

def test(fname):
	speakers = data.get_speakers(path)
	number_classes=len(speakers)
	print("speakers",number_classes,speakers)

	# Classification
	tf.reset_default_graph()
	tflearn.init_graph(num_cores=8, gpu_memory_fraction=0.5)

	net = tflearn.input_data(shape=[None, 8192]) #Two wave chunks
	net = tflearn.fully_connected(net, 64)
	net = tflearn.dropout(net, 0.5)
	net = tflearn.fully_connected(net, number_classes, activation='softmax')
	net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')
	modelb = tflearn.DNN(net)
	modelb.load('vrecog/vrecog.tflearn')
	result=data.load_wav_file(path+fname)
	result=modelb.predict([result])
	print(result)
	result=data.one_hot_to_item(result,speakers)
	print("predicted speaker for %s : result = %s "%(fname,result))
	return result

if __name__ == '__main__':
	command = raw_input("What to do\n")
	if command == 'train':
		train()
	elif command == 'test':
		# loadmodel()
		demo_file = "personname.wav.ig"
		test(demo_file)
