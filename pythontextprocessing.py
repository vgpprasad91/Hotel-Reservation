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
stop.update(['books',('', ' ', 'books'),'name',('', ' ', 'name'),'book',('', ' ', 'book'),'seats',('', ' ', 'seats'),'seat',('', ' ', 'seat'),'tickets',('', ' ', 'tickets'),'ticket',('', ' ', 'ticket'),'stay',('', ' ', 'stay'),'days',('', ' ', 'days'),'day',('', ' ', 'day'),'night',('',' ','night')])
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

#-------------Finding the intent of the booking--------------------------------------------------
    #----------------------We have to book a bigger database such that it contains all the categories of booking------------
    #----------------------Currently, I am serving the categories with a sample combination of several e-commerce website---------------------------

#---------------printing date and time---------------------------------------------
mytime = []
seatflag = 0
booktimelength = 0
dateflag = 0
timeflag = 0
forflag = 0
todayday = datetime.date.today( )
tomorrow = todayday + datetime.timedelta(days=1)
mon = ""
numbers = []
todayword = []
booktime = ""
bookdate = ""
timestr = ""
seats = ""
stringsplit = str1.split()
seat = list()
bktime = 0

         #--------------printing time----------------------------------
daytimewords = 'morning afternoon evening'
timingword = 'pm am'
todaywords = 'tonight today tomorrow'
afterdayswords = 'after tomorrow next day following day'
weekdaywords = 'monday tuesday wednesday thursday friday saturday sunday'
weekdaymap = {'monday': 0, 'tuesday': 1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
time = re.findall(r"(\w*)(\W)(\w*)\s*(?=CD pobj|CD num|CD dep|NNP pobj|NNS pobj|NNP appos|NN pobj|NN dobj|NN tmod|NN dep|NN conj|NN nn|NN appos|ADD pobj|CD npadvmod)", str1)
for x in range(0,len(time)):
    pos1 = (dictword[''.join(time[x]).lower().strip()])
    if (str1.split()[pos1] == "days") or (str1.split()[pos1] == "day"):
        bkdate = str1.split()[pos1-1]
        bkdateword = str1.split()[pos1-2]
        if (bkdateword == "after"):
            if (bkdate.isdigit()):
                bookdate = todayday + datetime.timedelta(days=int(bkdate))
                dateflag = 1
                bookdate = str(bookdate)
                break
            elif (str(text2num(bkdate)).isdigit()):
                bookdate = todayday + datetime.timedelta(days=text2num(bkdate))
                dateflag = 1
                bookdate = str(bookdate)
                break
        elif (bkdateword == "for"):
            if (bkdate.isdigit()):
                for i in range(int(bkdate)):
                    bookdate = bookdate +" "+"and"+" "+ str(todayday+datetime.timedelta(days=i))
                    dateflag = 1
                    forflag = 1
            elif (str(text2num(bkdate)).isdigit()):
                for i in range(text2num(bkdate)):
                    bookdate = bookdate +" "+"and"+" "+ str(todayday+datetime.timedelta(days=i))
                    dateflag = 1
                    forflag = 1
        break
if (dateflag == 1) and (forflag == 1): bookdate = bookdate.lower().strip().split(' ', 1)[1]
time = ([i for i in time if i not in stop])
for x in range(len(time)):timestr = timestr+" "+''.join(time[x]).lower().strip()
for x in range(0,len(time)):
    pos = (dictword[''.join(time[x]).lower().strip()])
    if (str1.split()[pos] == "pm"):
        time.pop(x)
        time.pop(x)
        time.extend([str(text2num(str1.split()[pos-1]))+str(str1.split()[pos])])
        break
for x in range(0,len(time)):
    if (("pm" in ''.join(time[x]).lower().strip()) or ("am" in ''.join(time[x]).lower().strip())):
        pos = ''.join(time[x]).lower().strip().find("am")
        pos1 = ''.join(time[x]).lower().strip().find("pm")
        if ((''.join(time[x]).lower().strip()[pos-1]).isdigit()) or ((''.join(time[x]).lower().strip()[pos1-1]).isdigit()):
            booktime = ''.join(time[x]).lower().strip()
            timeflag = 1
    else:
        posi = (dictword[''.join(time[x]).lower().strip()])
	if (str1.split()[posi-1] != "at"):
            if (((''.join(time[x]).strip()).isdigit()) and (seatflag == 0) and (dateflag == 0)):
                seats = "Number of seats :"+''.join(time[x])
                seatflag = 1
            elif (text2num(''.join(time[x]).lower().strip()) > 0) and (seatflag == 0 and (dateflag == 0)):
                seats = text2num(''.join(time[x]).lower().strip())
                seats = "Number of seats :"+ str(seats)
                seatflag = 1
for x in range(len(time)):
    S2 = ''.join(time[x]).lower().strip()
    if (daytimewords.find(S2) >= 0) and (timeflag == 0):
        timeflag = 1
        befor_keyword, keyword, after_keyword = str1.partition(''.join(time[x]))
        for i in range(len(befor_keyword.split())):numbers.extend([i])
        dictbefword = dict(zip(befor_keyword.split(), numbers))
        pos = after_keyword.index("Parse")
        after_keyword = after_keyword[:pos]
        dictaftword = dict(zip(after_keyword.split(), numbers))
        if (" at " in befor_keyword):
            position = dictbefword["at"]
            for y,z in dictbefword.items():
                if ((z == int(position)+1) and (S2 == daytimewords.split()[0])):
                    if (y.isdigit()):
                        booktime = str(y)+" "+"am"
                    elif (text2num(y) > 0):
                        booktime = str(y)+" "+"am"
                    break
                elif (((y == position+1) and (S2 == daytimewords.split()[1])) or ((S2 == daytimewords.split()[2]) and (y == position+1))):
                    if (x.isdigit() > 0):
                        booktime = str(text2num(x))+"pm"
                    elif (text2num(x) > 0):
                        booktime = str(x)+" "+"am"
                    break
        elif (" at " in after_keyword):
            position1 = dictaftword["at"]
            for x,y in dictaftword.items():
                if ((y == position1+1) and (S2 == daytimewords.split()[0])):
                    if (text2num(x) > 0):
                        booktime = str(text2num(x))+" "+"am"
                    break
                elif (((y == position1+1) and (S2 == daytimewords.split()[1])) or ((S2 == daytimewords.split()[2]) and (y == position1+1))):
                    if (text2num(x) > 0):
                        booktime = str(text2num(x))+" "+"pm"
                    break
        else:
            booktime = raw_input('At what time do you want me to book the seats?')
        if (" for " in befor_keyword) and (seatflag == 0) and (dateflag == 0):
            position = dictbefword["for"]
            for x,y in dictbefword.items():
                if (y == position+1):
                    seats = "Number of seats: "+str(x)
            seatflag = 1
    elif (str1.find("after tomorrow") >= 0) and (dateflag == 0):
        bookdate = todayday + datetime.timedelta(days=2)
        dateflag = 1
    elif ((str1.find("next day") >= 0) and (dateflag==0)) or ((str1.find("following day") >= 0) and (dateflag==0)):
        bookdate = todayday + datetime.timedelta(days=1)
        dateflag = 1
    elif (weekdaywords.find(S2) >= 0) and (dateflag==0):
        bookdate = todayday + datetime.timedelta( (weekdaymap[''.join(time[x]).lower().strip()]-todayday.weekday()) % 7 )
        dateflag = 1
    elif ("weekend".find(S2) >= 0) and (dateflag==0):
        bookdate1 = todayday + datetime.timedelta( (weekdaymap['saturday']-todayday.weekday()) % 7 )
        bookdate2 = todayday + datetime.timedelta( (weekdaymap['sunday']-todayday.weekday()) % 7 )
        bookdate = str(bookdate1) +" "+"and "+" "+ str(bookdate2)
        dateflag = 1
    elif ((timestr.find("tomorrow") >= 0) and (timestr.find("tonight") >= 0) and (dateflag==0)) or ((timestr.find("today") >= 0) and (timestr.find("tomorrow") >= 0) and (dateflag==0)):
        bookdate = str(todayday) +" "+ "and"+" "+ str(tomorrow)
        dateflag = 1
    elif (todaywords.find(S2) >= 0) and (dateflag==0):
        if ("tomorrow".find(S2) >= 0):
            bookdate = todayday + datetime.timedelta(days=1)
            dateflag = 1
        elif ("tonight".find(S2) >= 0) or ("today".find(S2) >= 0):
            bookdate = str(todayday)
            dateflag = 1
            #------------------printing future booking date and day-------------------
                #---------------------printing datemonth----------------------------------
datemon = ""
month = ["january","february","march","april","may","jun","july","august","september","october","november","december"]
datemonth = re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP pobj)", str1)
for x in range(len(datemonth)):
    datemon = filter(lambda y: ''.join(datemonth[x]).lower().strip() in y, month)
    combined = '\t'.join(month)
    if (''.join(datemonth[x]).lower().strip() in combined):
        mon = ''.join(datemonth[x]).strip()
                #--------------------printing day-----------------------------------------
myday = []
daypresent = 0
day = []
daystr = ""
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
    if (len(myday)>0):
        bookday = ''.join(myday[0])
    else:
        bookday = [None] * 0
                #-------------------printing both month and day combined--------------------

if (len(booktime) > 0) and (len(myday) > 0) and (len(datemon) > 0):
    bookdate = bookday+" "+''.join(datemon[0])
elif (len(myday) > 0) and (len(datemon) > 0) and (len(booktime) <= 0):
    bookdate = bookday+" "+''.join(datemon[0])
if (len(booktime) > 0) or (len(str(bookdate)) > 0):
    booktime = "Booktime: "+ booktime+ " "+str(bookdate)
#------------------------printing location--------------------------------\
stopword = daytimewords.split()+todaywords.split()+afterdayswords.split()+weekdaywords.split()+month
stop.update(stopword)
mylocation = ""
mylocationx = []
mylocationy = []
mynewlocation = []
unique = []
detf = 0
num = 0
#-----------------------Finding location----------------------------------
location = re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP pobj|NN pobj|NNP dep|NNP dobj|RB advmod)", str1)
location = ([i for i in location if i not in stop])
locflag = [m.start() for m in re.finditer('NNP pobj|NN pobj|NNP dep|NNP dobj|RB advmod',str1)]
dictionary = dict(zip(locflag, location))
    #----------------sorting a dictionary in reverse order-------------
items = dictionary.items()
items.sort(key=lambda item: (item[0]))
locflag = [ item[0] for item in items ]
location = [ item[1] for item in items ]
    #----------------Finding location1---------------------------------
location1 = re.findall(r"(\w*)(\W)(\w*)\s*(?=NNP nn|NN nn|RB advmod|VB partmod)", str1)
location1 = ([i for i in location1 if i not in stop])
locflag1 = [m.start() for m in re.finditer('NNP nn|NN nn|RB advmod|VB partmod',str1)]
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
    for i in range(len(prep)):
        if ('at' in prep[i]) or ('in' in prep[i]):
            for x,y in product(range(len(locflag)), range(len(locflag1))):
                if ((prepflag[i] < locflag[x] < (locflag1[y])) and (locflag[x] > locflag1[y] - 40) and (prepflag[i] > locflag1[y] - 80)):
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
    #-------------------Logical conditions to print locations end---------------------
#---------------printing number of seats----------------------------------
seatlen = 0
pluralflag = 0
nnnum = 0
myflag = 0
artflag = 0
myseats = 0
num = 0
count = 0
myseats = []
mynewseats = []
newseats = []
if seatflag == 0:
    seats = re.findall(r"(\w+)\s*(?=CD num|CD pobj|CD dobj|NN nsubj|CD parataxis|NN conj|NNS conj|CD conj|NN appos|NNS appos|NNS dep)", str1)
    seats = ([i for i in seats if i not in stop])
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
##------------------------------Program Logic end-------------------------------------------------
#--------------print entities as per OR Gate----------------------------------
if (len(booktime) > 0 and len(mylocation) > 0 and len(seats) > 0):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Intent: restaurant-reservation"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Entities:"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(mylocation+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(seats+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(booktime+"\n")
elif (len(booktime) > 0 and len(mylocation) > 0 and len(seats) < 1):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Intent: restaurant-reservation"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Entities:"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(mylocation+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(booktime+"\n")
    print("Happy to help you and Can you please say to book for how many seats?") 
    subprocess.call("./getseats.sh", shell=True)
elif (len(booktime) > 0 and len(mylocation) < 1 and len(seats) > 0):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Intent: restaurant-reservation"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Entities:"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(seats+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(booktime+"\n")
    print("Happy to help and can you provide details of the location?")
    subprocess.call("./getlocation.sh", shell=True)
elif (len(booktime) < 1 and len(mylocation) > 0 and len(seats) > 0):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Intent: restaurant-reservation"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Entities:"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(seats+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(mylocation+"\n")
    print("Happy to help and can you provide me the date and time?")
    subprocess.call("./gettime.sh", shell=True)
elif (len(booktime) > 0 and len(mylocation) < 1 and len(seats) < 1):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Intent: restaurant-reservation"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Entities:"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(booktime+"\n")
    print("Happy to help and can you provide details of the location?")
    subprocess.call("./getlocation.sh", shell=True)
    print("Happy to help and for how many peope to book?")
    subprocess.call("./getseats.sh", shell=True)
elif (len(booktime) < 1 and len(mylocation) > 0 and len(seats) < 1):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Intent: restaurant-reservation"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Entities:"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(mylocation+"\n")
    print("Happy to help and can you provide me the date and time?")
    subprocess.call("./gettime.sh", shell=True)
    print("Happy to help and for how many peope to book?")
    subprocess.call("./getseats.sh", shell=True)
elif (len(booktime) < 1 and len(mylocation) < 1 and len(seats) > 0):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Intent: restaurant-reservation"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write("Entities:"+"\n")
    with open("parse.txt", "a") as myfile: myfile.write(seats+"\n")
    print("Happy to help and can you provide details of the location?")
    subprocess.call("./getlocation.sh", shell=True)
    print("Happy to help and can you provide me the date and time?")
    subprocess.call("./gettime.sh", shell=True)
elif (len(booktime) < 1 and len(mylocation) < 1 and len(seats) < 1):
    with open("parse.txt", "a") as myfile: myfile.write(inputstring[0]+"\n")
    print("Happy to help and can you provide details of the location?")
    subprocess.call("./getlocation.sh", shell=True)
    print("Happy to help and can you provide me the date and time?")
    subprocess.call("./gettime.sh", shell=True)
    print("Happy to help and for how many peope to book?")
    subprocess.call("./getseats.sh", shell=True)
                                      
str1 = open("parse.txt").read()
print(str1)
