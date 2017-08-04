import record
# import formataudio
import speaker_classifier_tflearn
#
record.record_to_file("personname") #create data
speaker_classifier_tflearn.train() #retrain
import time
time.sleep(2)
speaker_classifier_tflearn.loadmodel() #load/reload model
record.record_to_file("temp",train=False) #create data
person = speaker_classifier_tflearn.test("temp.wav.ig") #call whenevr want to classify
