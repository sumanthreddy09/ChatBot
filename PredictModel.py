"""
File : PredictModel
Description : Predict the response from the model that is saved by TrainModel.py.
Author : Sumanth Kaliki <sumanth.reddy542@gmail.com>
Date : 26-04-2018
"""

import nltk
import hashlib
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import random

# restore all of our data structures
import pickle
data = pickle.load( open( "./models/training_data2", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']
checksum = data['checksum']

modelName='model9'
dataJSON='Data.json'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

present_checksum = md5(dataJSON)
# import our chat-bot intents file
import json
'''
if not present_checksum == checksum:
    raise Exception('data file modified!', present_checksum, checksum)
'''
with open(dataJSON) as json_data:
    intents = json.load(json_data)
print(len(train_x), len(train_y), len(train_x[0]), len(train_y[0]))

# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net)
model.load('./models/%s.tflearn'%(modelName))

def bow(text):
    li=[]
    wordList=[]
    text=  filterAlphabets(text)
    text=[stemmer.stem(word.lower()) for word in text.split(' ')]
    for w in words:
        if w in text:
            li.append(1)
            if(w not in wordList):
                wordList.append(w)
        else:
            li.append(0)
    print('\nHits: %s\n'%(wordList))
    return(li)

def filterAlphabets(x):
    temp=""
    for a in x:
        if(a.isalpha() or a.isdigit() or a==" "):
            temp+=a
    return(temp)

# for testing purpose
def manual_input():
    inp=''
    while(inp != 'exit'):
        inp=input('\nInput Text to check: ')
        p = bow(inp)
        res=model.predict([p])
        maxVal=0
        resClass=''
        for i in range(len(classes)):
            if(maxVal<res[0][i]):
                maxVal=res[0][i]
                resClass=classes[i]
        print('\nResult: %s -> %s'%(resClass,maxVal))
        
        for tag in intents['intents']:
            if(tag['tag']==resClass):
                jsonClass=tag
        
        
        message=jsonClass['responses']
        print(message)
        print('\n\n')
        random.shuffle(message)
        if '' in message:
            message.remove('')
        message=message[0]
        print(message)
        if('extra' in jsonClass):
            if random.randint(0,1) == 1:
                message += '\n' + jsonClass['extra'][random.randint(0,len(jsonClass['extra'])-1)]

def response(text):
    p = bow(text)
    res=model.predict([p])
    maxVal=0
    resClass=''
    for i in range(len(classes)):
        if(maxVal<res[0][i]):
            maxVal=res[0][i]
            resClass=classes[i]
    if(maxVal<0.3):
        resClass='unsure'
    for tag in intents['intents']:
        if(tag['tag']==resClass):
            return tag
            
if __name__ == '__main__':
    manual_input()
