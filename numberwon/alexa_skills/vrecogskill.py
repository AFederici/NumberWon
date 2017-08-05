import vrecog.record as record
# import formataudio
import vrecog.speaker_classifier_tflearn as speaker_classifier_tflearn
#
record.record_to_file("personname") #create data
speaker_classifier_tflearn.train() #retrain

record.record_to_file("temp",train=False) #create data
person = speaker_classifier_tflearn.test("temp.wav.ig") #call whenevr want to classify

record.record_to_file("personnamee") #create data
speaker_classifier_tflearn.train() #retrain

record.record_to_file("temp",train=False) #create data
person = speaker_classifier_tflearn.test("temp.wav.ig") #call whenevr want to classify
