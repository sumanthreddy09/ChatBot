"""
File : TrainModel
Description : Train and save the model.
Author : Sumanth Kaliki <sumanth.reddy542@gmail.com>
Date : 26-04-2018
"""

from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import numpy as np
import hashlib
import tflearn
import random
import json
import pickle
from nltk.corpus import stopwords

modelName='model9'
dataJSON='final.json'

class Training_Model:
    def __init__(self):
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?']
        self.stemmer = PorterStemmer()

    def load_data(self, file):
        with open(file) as json_data:
            return json.load(json_data)

    def initialize(self, intents):
        # loop through each sentence in our intents patterns
        for intent in intents['intents']:
            # add the tag itself as a row    
            w=word_tokenize(intent['tag'])
            self.words.extend(w)
            self.documents.append((w, intent['tag']))
                
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = word_tokenize(pattern)
                # add to our words list
                self.words.extend(w)
                # add to documents in our corpus
                self.documents.append((w, intent['tag']))
                # add to our classes list
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
                    
        # remove duplicates
        self.words = sorted(list(set(self.words)))
        self.words = list(map(lambda x: x.lower(), self.words))

        #remove stopwords
        temp_words=[]
        stop_words = stopwords.words('english')
        stop_words = []

        self.ignore_words = list(map(lambda x: x.lower(), self.ignore_words+temp_words+stop_words))
        tempWords = [w for w in self.words if w not in self.ignore_words]        
        self.words=tempWords

        #stemming
        self.words = [self.stemmer.stem(w.lower()) for w in self.words]

        # remove duplicates
        self.classes = sorted(list(set(self.classes)))

    def generate_training_data(self):
        training = []
        output = []

        # create an empty array for our output
        output_empty = [0] * len(self.classes)

        # training set, bag of words for each sentence
        for doc in self.documents:
            #documents format [([tokenized words list],tag),(),(),(),(testCases)...]
            bag = self.bag_of_words(doc[0])    
            # output is a '0' for each tag and '1' for current tag
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1

            training.append([bag, output_row])

        return training

    def bag_of_words(self, pattern_words):
        # initialize our bag of words
        bag = []
        # stem each word
        pattern_words = [self.stemmer.stem(word.lower()) for word in pattern_words]
        # create our bag of words array
        for w in self.words:
            bag.append(1) if w in pattern_words else bag.append(0)
        
        return bag
        
    def train_model(self, training):
        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training)

        # create train and test lists
        self.train_x = list(training[:,0])
        self.train_y = list(training[:,1])

        # Build neural network
        net = tflearn.input_data(shape=[None, len(self.train_x[0])])
        net = tflearn.fully_connected(net, 16)
        net = tflearn.fully_connected(net, 16)
        net = tflearn.fully_connected(net, len(self.train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        model = tflearn.DNN(net)
        # Start training (apply gradient descent algorithm)
        model.fit(self.train_x, self.train_y, n_epoch=1000, batch_size=16, show_metric=True)

        return model

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def save_model(self, model):
        global modelName
        # save all of our data structures
        model.save('./models/%s.tflearn'%(modelName))
        checksum = self.md5(dataJSON)
        pickle.dump( {'words': self.words, 'classes':self.classes, 'train_x':self.train_x, 'train_y':self.train_y, 'checksum': checksum}, open( "./models/training_data2", "wb" ) )

def main():

    trainer = Training_Model()
    intents = trainer.load_data(dataJSON)
    trainer.initialize(intents)
    training_data = trainer.generate_training_data()
    model = trainer.train_model(training_data)
    
    trainer.save_model(model)

if __name__ == '__main__':
    main()

