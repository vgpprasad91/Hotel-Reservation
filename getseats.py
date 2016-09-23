#!/usr/bin/python

#--------------------------------Various imports needed for the file---------------------------------
import re
import subprocess
import time
import datetime
import itertools
import numpy as np
import operator
import collections
import nltk
from nltk.stem import WordNetLemmatizer
from itertools import groupby
from nltk.corpus import stopwords
from collections import OrderedDict
from itertools import product
from  __builtin__ import any as b_any
#-------------------------------Inputs and Imports---------------------------------------------------------

wnl = WordNetLemmatizer()
stop = set(stopwords.words('english'))
stop.update(['books',('', ' ', 'books'),'book',('', ' ', 'book'),'seats',('', ' ', 'seats'),'seat',('', ' ', 'seat'),'tickets',('', ' ', 'tickets'),'ticket',('', ' ', 'ticket'),'stay',('', ' ', 'stay'),'days',('', ' ', 'days'),'day',('', ' ', 'day'),'night',('',' ','night')])
#--------------------------------------------------------------------------------------------------
strnumbers=[]
str1 = open("output1.txt").read()
inputstring = str1.split("Parse")
for i in range(len(inputstring[0].lower().split())):strnumbers.extend([i])
dictword = dict(zip(inputstring[0].lower().split(), strnumbers))

#--------------------------------Dependency Logic-----------------------------------------------

    #---------------------------Logic for text2num---------------------------------------------
Smallnumbers = {'zero': 0,'one': 1,'two': 2,'three': 3,'four': 4,'five': 5,'six': 6,'seven': 7,'eight': 8,'nine': 9,'ten': 10,'eleven': 11,'twelve': 12,'thirteen': 13,'fourteen': 14,'fifteen': 15,'sixteen': 16,'seventeen': 17,'eighteen': 18,'nineteen': 19,'twenty': 20,'thirty': 30,'forty': 40,'fifty': 50,'sixty': 60,'seventy': 70,'eighty': 80,'ninety': 90}
largenumber = {'thousand':     1000}

def text2num(s):
    n = 0
    g = 0
    for w in (re.split(r"[\s-]+", s)):
        x = Smallnumbers.get(w, None)
        if x is not None:g += x
        elif w == "hundred" and g != 0:g *= 100
        else:
            x = largenumber.get(w, None)
            if x is not None:
                n += g * x
                g = 0
    return n + g
    #---------------------------Logic for text2num ends-----------------------------------------------
##--------------------Program Logic---------------------------------------------

#---------------printing seats---------------------------------------------

seatlen = 0
seatflag = 0
pluralflag = 0
nnnum = 0
myflag = 0
artflag = 0
myseats = 0
num = 0
count = 0
myseats = []
numbers = []
mynewseats = []
newseats = []
daytimewords = 'morning afternoon evening'
timingword = 'pm am'
todaywords = 'tonight today tomorrow'
afterdayswords = 'after tomorrow next day following day'
weekdaywords = 'monday tuesday wednesday thursday friday saturday sunday'
month = ["january","february","march","april","may","jun","july","august","september","october","november","december"]
stopword = daytimewords.split()+todaywords.split()+afterdayswords.split()+weekdaywords.split()+month
stop.update(stopword)
if seatflag == 0:
    seats = re.findall(r"(\w+)\s*(?=CD ROOT|CD num|CD pobj|CD dobj|NN nsubj|CD parataxis|NN conj|NNS conj|CD conj|NN appos|NNS appos|NNS dep)", str1)
    seats = ([i for i in seats if i not in stop])
    for x in range(0,len(seats)):
        if (("pm" not in ''.join(seats[x]).lower().strip()) or ("am" not in ''.join(seats[x]).lower().strip())):
            pos1 = (dictword[''.join(seats[x]).lower().strip()])
            if ((''.join(seats[x]).strip()).isdigit()):
                if (str1.split()[pos1] != "days") or (str1.split()[pos1] != "day"):
                    seats = "Number of seats :"+''.join(seats[x])
                    seatflag = 1
                    timeflag = 1
            elif (text2num(''.join(seats[x]).lower().strip()) > 0):
                if (str1.split()[pos1] != "days") or (str1.split()[pos1] != "day"):
                    seats = text2num(''.join(seats[x]).lower().strip())
                    seats = "Number of seats :"+ str(seats)
                    seatflag = 1
                    timeflag = 1
else:
    try:
        for i in range(0,len(seats)):
            if "pm" in ''.join(seats[i]).lower().strip():
                if (0,len(seats) > 1):
                    seats.remove(seats[i])
                else:
                    seats = []
    except:
        None
    mycount = str1.count(' my ')
    mecount = str1.count(' me ')
    mycount = mycount/2
    mecount = mecount/2
    if (mecount > 0) or (mycount > 0):
        pluralflag = 1
    for nn in seats:
        plural = True if nn is not wnl.lemmatize(nn, 'n') else False
        if (plural == True):
            nnnum = raw_input('Can I know how much '+nn+' do you bring?')
            pluralflag = 1
            mycount = mycount - 1
            seatlen = seatlen + int(nnnum)
    seatlen = seatlen + mecount + mycount
    if ((len(seats) > 0) and (seatflag ==0) and (pluralflag == 0)):
        seats = "Number of seats: "+ ''.join(seats)
    elif (seatlen > 0) and (seatflag == 0) and (pluralflag == 1):
        seats = "Number of seats: "+ str(seatlen)


with open("parse.txt", "a") as myfile:
    myfile.write(str(seats))
    
str1 = open("parse.txt").read()
print(str1)


