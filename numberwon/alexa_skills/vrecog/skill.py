import record
import formataudio
import speaker_classifier_tflearn

record.record_to_file(person_name) #create data
speaker_classifier_tflearn.train() #retrain
speaker_classifier_tflearn.loadmodel() #load/reload model


record.record_to_file(temp,train=False) #create data
speaker_classifier_tflearn.test(temp) #call whenevr want to classify
