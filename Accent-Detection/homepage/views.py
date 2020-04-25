# -*- coding: utf-8 -*-
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr
import statistics
from statistics import mode

# import os
import sys
from django.core.checks import Error
# sys.path.append(os.path.abspath("D:/Akshay/Projects/Sem 6/SDP/dialect_version1/homepage/"))
# "D:/Akshay/Projects/Sem 6/SDP/dialect_version1/homepage/temp"
# from temp import *


def convert_dic_to_vector(dic, max_word_length):
    print("Inside convert dic to vector function")
    new_list = []
    for word in dic:
        vec = ''
        n = len(word)
        for i in range(n):
            current_letter = word[i]
            ind = ord(current_letter)-2688
            placeholder = (str(0)*ind) + str(1) + str(0)*(126-ind)
            vec = vec + placeholder
        if n < max_word_length:
            excess = max_word_length-n
            vec = vec +str(0)*127*excess
        new_list.append(vec)
    return new_list


def makepredict(text):
    my_dic = {}
    my_lst = []
    print("inside makepridct")
    max_letters = 8
    language_tags = {

                'ahmedabadi':[],

                'charotari': [],

                'surati': [],

                'mahesani': [],

                'kathiyavadi': []

                 }
    print("Neural net start creating")
    network = Sequential()
    print("1 Neural net start creating")
    network.add(Dense(900, input_dim=127*max_letters, activation='sigmoid'))
    network.add(Dense(600, activation='sigmoid'))
    network.add(Dense(300, activation='sigmoid'))
    network.add(Dense(100, activation='sigmoid'))
    network.add(Dense(len(language_tags), activation='softmax'))
    print("2 Neural net start creating")
    try:
        network.load_weights('weights.hdf5')
    except Exception as e:
        print("this is exception : ")
       # print(e.message)
    print("3 Neural net start creating")
    network.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
    print("neural net is created")
    lst = text.split()
    for i in lst:
        dic = []
        valid = False
        while not valid:
            # word = input('Enter word to predict:\n')
            word = i
            if len(word) <= max_letters:
                word = word.lower()
                valid = True
            else:
                print('Word must be less than ' + str(max_letters + 1) + ' letters long')
        dic.append(word)
        vct_str = convert_dic_to_vector(dic, max_letters)
        vct = np.zeros((1, 127 * max_letters))
        count = 0
        for digit in vct_str[0]:
            vct[0,count] = int(digit)
            count += 1
        prediction_vct = network.predict(vct)
        tmp = 0
        langs = list(language_tags.keys())
        for i in range(len(language_tags)):
            lang = langs[i]
            score = prediction_vct[0][i]
            print(lang + ': ' + str(round(100*score, 2)) + '%')
            my_dic[lang] = round(100*score, 2)
            print('\n')
        my_lst.append(max(my_dic, key=my_dic.get))
    return(my_lst)
    # return render(request, 'homepage/homepage.html',{'s':text})

def getmaxstring(str_lst):
    return(mode(str_lst))

def index(request) :
    if 'speak' in request.POST :
        r=sr.Recognizer()
        with sr.Microphone() as source :
            print("Speak Anything : ")
            audio=r.listen(source)
        try :
            text=r.recognize_google(audio, language="gu-IN")
            print("You Said : ",format(text))
            my_lst = makepredict(text)
            dic2 = getmaxstring(my_lst)
            # txt = format(text)
            # request.session["tx"] = text
        
        except :
            print("Sorry could not recognize your voice")
            text="Sorry could not recognize your voice"
            dic2 = "NOBOdy"
        return render(request, 'homepage/homepage.html',{'s':text,'predict':dic2})
    elif request.method == "POST" and len(request.FILES)!=0 :
        uploaded_file = request.FILES["document"]
        r = sr.Recognizer()
        with sr.AudioFile(uploaded_file) as source :
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.record(source)
        try :
            s=r.recognize_google(audio, language="gu-IN")
            print(s)
            my_lst = makepredict(text)
            dic2 = getmaxstring(my_lst)
            return render(request, 'homepage/homepage.html',{'s':s, 'predict':dic2})
        except :
            print("Something Went Wrong")
    return render(request, 'homepage/homepage.html')