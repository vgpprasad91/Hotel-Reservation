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
#---------------------------------------------------------------------------------------------------

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
#------------------------printing location--------------------------------\
daytimewords = 'morning afternoon evening'
timingword = 'pm am'
todaywords = 'tonight today tomorrow'
afterdayswords = 'after tomorrow next day following day'
weekdaywords = 'monday tuesday wednesday thursday friday saturday sunday'
month = ["january","february","march","april","may","jun","july","august","september","october","november","december"]
stopword = daytimewords.split()+todaywords.split()+afterdayswords.split()+weekdaywords.split()+month
stop.update(stopword)
mylocation = ""
mylocationx = []
mylocationy = []
mynewlocation = []
unique = []
detf = 0
num = 0
myday = []
daypresent = 0
day = []
daystr = ""
datemon = ""
mon = ""
month = ["january","february","march","april","may","jun","july","august","september","october","november","december"]
datemonth = re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP pobj)", str1)
for x in range(len(datemonth)):
    datemon = filter(lambda y: ''.join(datemonth[x]).lower().strip() in y, month)
    combined = '\t'.join(month)
    if (''.join(datemonth[x]).lower().strip() in combined):
        mon = ''.join(datemonth[x]).strip()

day = re.findall(r"(\w*)(\W)(\w*)\s*(?=JJ amod)", str1)
day.extend(re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP nn)", str1))
for x in range(len(day)):daystr = daystr+" "+''.join(day[x]).lower().strip()
for x in range(len(daystr.split())):
    for i in range(len(daystr.split()[x])):
        try:
            if ((daystr.split()[x].split('rd')[0][-1]).isdigit()) or ((daystr.split()[x].split('rd')[0][-2]).isdigit()):
                myday.append(daystr.split()[x])
                break
            elif ((daystr.split()[x].split('st')[0][-1]).isdigit()) or ((daystr.split()[x].split('st')[0][-2]).isdigit()):
                myday.append(daystr.split()[x])
                break
            elif ((daystr.split()[x].split('th')[0][-1]).isdigit()) or ((daystr.split()[x].split('th')[0][-1]).isdigit()):
                myday.append(daystr.split()[x])
                break
        except:
            None

#-----------------------Finding location----------------------------------
location = re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP pobj|NN pobj|NNP dep|UH ROOT|NNP ROOT|NN ROOT|NNP dobj|NN dobj|RB advmod)", str1)
location = ([i for i in location if i not in stop])
locflag = [m.start() for m in re.finditer('NNP pobj|NN pobj|NNP dep|UH ROOT|NNP dobj|NN dobj|NNP ROOT|RB advmod|NN ROOT',str1)]
dictionary = dict(zip(locflag, location))
    #----------------sorting a dictionary in reverse order-------------
items = dictionary.items()
items.sort(key=lambda item: (item[0]))
locflag = [ item[0] for item in items ]
location = [ item[1] for item in items ]
    #----------------Finding location1---------------------------------
location1 = re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP nn|NN dep|NN nn|RB advmod|VB partmod)", str1)
location1 = ([i for i in location1 if i not in stop])
locflag1 = [m.start() for m in re.finditer('NNP nn|NN dep|NN nn|RB advmod|VB partmod',str1)]
dictionary1 = dict(zip(locflag1, location1))
    #----------------sorting a dictionary in reverse order-------------
items = dictionary1.items()
items.sort(key=lambda item: (item[0], item[1]),reverse=True)
locflag1 = [ item[0] for item in items ]
location1 = [ item[1] for item in items ]
    #------------------Finding the det--------------------------------
det = re.findall(r"(\w*)(\W)(\w*)\s*(?=DT det)", str1)
detflag = [m.start() for m in re.finditer('DT det',str1)]
location2 = re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP dobj)", str1)
location2 = ([i for i in location2 if i not in stop])
locflag2 = [m.start() for m in re.finditer('NNP dobj',str1)]
dictionary2 = dict(zip(locflag2, location2))
locflag2 = dictionary2.keys()
location2 = dictionary2.values()
location3 = re.findall(r"(\w*)(\W)(\w*)\s*(?=JJ nn)", str1)
location3 = ([i for i in location3 if i not in stop])
locflag3 = [m.start() for m in re.finditer('JJ nn',str1)]
dictionary3 = dict(zip(locflag3, location3))
locflag3 = dictionary3.keys()
location3 = dictionary3.values()
    #---------------Logical conditions to print location--------------------
if ((len(location) > 0) and (len(location1) > 0) and (len(det) > 0)):
    for x,y in product(range(len(locflag)), range(len(locflag1))):
        if ((int(dictword[''.join(location[x]).lower().strip()])-1 == int(dictword[''.join(location1[y]).lower().strip()]))):
                mylocationy.append((''.join(location1[y])).lower().strip())
                detf = 1
        if ((int(dictword[''.join(location[x]).lower().strip()])-2 == int(dictword[''.join(location1[y]).lower().strip()]))):
                mylocationy.append((''.join(location1[y])).lower().strip())
                detf = 1
    mylocationy = sorted(set(mylocationy),key=mylocationy.index)
    try:
        for i in range(len(mylocationy)):
            if "pm" in mylocationy[i]:
                if (len(mylocationy) > 1):
                    mylocationy.remove(mylocationy[i])
                else:
                    mylocationy = []
    except:
        None
    if (len(myday) > 0):
        mylocationy = re.sub(''.join(myday).lower().strip(),"",''.join(mylocationy).lower().strip(),count=1)
    for x,y in product(range(len(locflag)), range(len(locflag1))):
        if ((int(dictword[''.join(location[x]).lower().strip()])+1 == int(dictword[''.join(location1[y]).lower().strip()]))):
            mylocationx.append((''.join(location[x])).lower().strip())
    for x,y in product(range(len(locflag)), range(len(locflag1))):
        if ((int(dictword[''.join(location[x]).lower().strip()])-1 == int(dictword[''.join(location1[y]).lower().strip()]))):
            mylocationx.append((''.join(location[x])).lower().strip())
    mylocationx = sorted(set(mylocationx),key=mylocationx.index)
    try:
        for i in range(len(mylocationx)):
            if "pm" in mylocationx[i]:
                if (len(mylocationx) > 1):
                    mylocationx.remove(mylocation[i])
                else:
                    mylocationx = []
    except:
        None
    if (len(mon) > 0):
        mylocationx = re.sub(''.join(mon).lower().strip(),"",''.join(mylocationx).lower().strip(),count=1)
    if (detf == 1):
        if (len(myday) > 0) and (len(mon) > 0):mylockeys = mylocationx.split() + mylocationy.split() + [''.join(det[0]).lower().strip()]
        elif (len(myday) > 0):mylockeys = mylocationx + mylocationy.split() + [''.join(det[0]).lower().strip()]
        elif (len(mon) > 0):mylockeys = mylocationx.split() + mylocationy + [''.join(det[0]).lower().strip()]
        else :mylockeys = mylocationx + mylocationy + [''.join(det[0]).lower().strip()]
        mylocvalues = [dictword[x] for x in mylockeys]
        dictmyloc = dict(zip(mylockeys, mylocvalues))
        sorted_myloc = sorted(dictmyloc.items(), key=operator.itemgetter(1))
        for i in range(len(sorted_myloc)):
            mylocation = mylocation + " "+" "+sorted_myloc[i][0]
        mylocation = "Location: "+ mylocation
        if ('the' in mylocation) or ('a' in mylocation) or ('an' in mylocation):
                mylocation = re.sub(" the ","",mylocation,count=1)
                mylocation = re.sub(" a ","",mylocation,count=1)
                mylocation = re.sub(" an ","",mylocation,count=1)
    else:
        for x,y in product(range(len(locflag)), range(len(locflag1))):
            if ((int(dictword[''.join(location[x]).lower().strip()])+1 == int(dictword[''.join(location1[y]).lower().strip()]))):
                mylocationy = ''.join(mylocationy)+''.join(location1[y])
                num = y
        mylocationy = ''.join(mylocationy)
        if (len(myday) > 0):
            mylocationy = re.sub(''.join(myday).lower().strip(),"",''.join(mylocationy).lower().strip(),count=1)
        if ("st" in mylocationy) or ("th" in mylocationy) or ("rd" in mylocationy):
            num = num - 1
        for x in range(len(locflag1)):
            if ((int(dictword[''.join(location[x]).lower().strip()])+1 == int(dictword[''.join(location1[y]).lower().strip()]))):
                mylocationx = ''.join(mylocationx) + ''.join(location1[x])
        mylocationx = ''.join(mylocationx)
        if (len(myday)>0):
            mylocationy = re.sub(''.join(myday[0]).lower().strip(),"",mylocationy,count=1)
        if (len(myday) > 0) and (len(mon) > 0):mylockeys = mylocationx.split() + mylocationy.split() 
        elif (len(myday) > 0):mylockeys = mylocationx + mylocationy.split() 
        elif (len(mon) > 0):mylockeys = mylocationx.split() + mylocationy
        else :mylockeys = mylocationx + mylocationy
        mylocation = "Location: "+ mylockeys
elif ((len(location) > 0) and (len(location1) > 0) and (len(det) <= 0)):
    prep = re.findall(r"(\w+)\s*(?=IN prep)", str1)
    prepflag = [m.start() for m in re.finditer('IN prep',str1)]
    if (len(prep)>0):
        for i in range(len(prep)):
            if ('at' in prep[i]) or ('in' in prep[i]):
                for x,y in product(range(len(locflag)), range(len(locflag1))):
                    if ((prepflag[i] < locflag[x] < (locflag1[y])) and (locflag[x] > locflag1[y] - 40) and (prepflag[i] > locflag1[y] - 80)):
                        mylocation = "Location: "+''.join(location1[y])+''.join(location[x])
            else:
                for x,y in product(range(len(locflag)), range(len(locflag1))):
                    if ((locflag[x] < (locflag1[y])) and (locflag[x] > locflag1[y] - 40)):
                        mylocation = "Location: "+''.join(location1[y])+''.join(location[x])
    else:
	for x,y in product(range(len(locflag)), range(len(locflag1))):
            if ((locflag[x] < (locflag1[y])) and (locflag[x] > locflag1[y] - 40)):
                 mylocation = "Location: "+''.join(location1[y])+''.join(location[x])
elif ((len(location2) > 0) and (len(location3) > 0)):
    for x,y in product(range(len(locflag2)), range(len(locflag3))):
        if (locflag2[x] > (locflag3[y] - 40)):
            mylocation = "Location: "+''.join(location3[y])+''.join(location2[x])
elif (len(location)>0):
    for i in range(len(location)):mynewlocation.extend(''.join(location[i]).lower().split())
    location = ([i for i in mynewlocation if i not in stop])
    for x in range(len(location)):
        mylocation = mylocation + ''.join(location[x])+","
    mylocation = "Location: " + mylocation[:-1]
elif (len(location2)>0):
    mylocation = "Location: "+''.join(location2[0])

mylocation = mylocation.title()

with open("parse.txt", "a") as myfile:
    myfile.write(mylocation)
    
str1 = open("parse.txt").read()
print(str1)

    #-------------------Logical conditions to print locations end---------------------
