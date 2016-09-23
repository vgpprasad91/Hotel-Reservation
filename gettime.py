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
time = re.findall(r"(\w*)(\W)(\w*)\s*(?=CD pobj|CD num|CC cc|CD dep|ADD ROOT|ADD punct|LS ROOT|NN ROOT|NNP pobj|NNS pobj|NNP appos|NN pobj|NN dobj|NN tmod|NN dep|NN conj|NN nn|NN appos|NN dep|ADD pobj|CD npadvmod)", str1)
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
        if (((''.join(time[x]).strip()).isdigit()) and (seatflag == 0) and (dateflag == 0)):
            seats = "Number of seats :"+''.join(time[x])
            seatflag = 1
        elif (text2num(''.join(time[x]).lower().strip()) > 0) and (seatflag == 0) and (dateflag == 0):
            seats = text2num(''.join(time[x]).lower().strip())
            seats = "Number of seats :"+ str(seats)
            seatflag = 1
for x in range(len(time)):
    S2 = ''.join(time[x]).lower().strip()
    if (daytimewords.find(S2) >= 0) and (timeflag == 0):
        timeflag = 1
        befor_keyword, keyword, after_keyword = str1.partition(''.join(time[x]).strip())
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
        elif ((''.join(time[x])).isdigit()) or ((str(text2num(''.join(time[x])))).isdigit()):
            if (S2 == daytimewords.split()[0]):
                booktime = (''.join(time[x])) +" "+"am"
            elif (S2 == daytimewords.split()[1]) and (S2 == daytimewords.split()[2]):
                booktime = (''.join(time[x]))+" "+"pm"
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
    elif ((timestr.find("saturday") >= 0) and (timestr.find("sunday") >= 0)) and (dateflag==0):
        day1 = todayday + datetime.timedelta( (weekdaymap['saturday']-todayday.weekday()) % 7 )
	day2 = todayday + datetime.timedelta( (weekdaymap['sunday']-todayday.weekday()) % 7 )
        bookdate = str(day1) + " "+ "and" + " "+ str(day2)
	dateflag = 1
    elif ((timestr.find("friday") >= 0) and (timestr.find("saturday") >= 0)) and (dateflag==0):
        day1 = todayday + datetime.timedelta( (weekdaymap['saturday']-todayday.weekday()) % 7 )
	day2 = todayday + datetime.timedelta( (weekdaymap['friday']-todayday.weekday()) % 7 )
        bookdate = str(day1) + " "+ "and" + " "+ str(day2)
	dateflag = 1
    elif (timestr.find("thursday") >= 0) and (timestr.find("friday") >= 0) and (dateflag==0):
        day1 = todayday + datetime.timedelta( (weekdaymap['thursday']-todayday.weekday()) % 7 )
	day2 = todayday + datetime.timedelta( (weekdaymap['friday']-todayday.weekday()) % 7 )
        bookdate = str(day1) + " "+ "and" + " "+ str(day2)
	dateflag = 1
    elif (timestr.find("wednesday") >= 0) and (timestr.find("thursday") >= 0) and (dateflag==0):
        day1 = todayday + datetime.timedelta( (weekdaymap['wednesday']-todayday.weekday()) % 7 )
	day2 = todayday + datetime.timedelta( (weekdaymap['thursday']-todayday.weekday()) % 7 )
        bookdate = str(day1) + " "+ "and" + " "+ str(day2)
	dateflag = 1
    elif (timestr.find("tuesday") >= 0) and (timestr.find("wednesday") >= 0) and (dateflag==0):
        day1 = todayday + datetime.timedelta( (weekdaymap['tuesday']-todayday.weekday()) % 7 )
	day2 = todayday + datetime.timedelta( (weekdaymap['wednesday']-todayday.weekday()) % 7 )
        bookdate = str(day1) + " "+ "and" + " "+ str(day2)
	dateflag = 1
    elif (timestr.find("monday") >= 0) and (timestr.find("tuesday") >= 0) and (dateflag==0):
        day1 = todayday + datetime.timedelta( (weekdaymap['monday']-todayday.weekday()) % 7 )
	day2 = todayday + datetime.timedelta( (weekdaymap['tuesday']-todayday.weekday()) % 7 )
        bookdate = str(day1) + " "+ "and" + " "+ str(day2)
	dateflag = 1
    elif (timestr.find("sunday") >= 0) and (timestr.find("monday") >= 0) and (dateflag==0):
        day1 = todayday + datetime.timedelta( (weekdaymap['sunday']-todayday.weekday()) % 7 )
	day2 = todayday + datetime.timedelta( (weekdaymap['monday']-todayday.weekday()) % 7 )
        bookdate = str(day1) + " "+ "and" + " "+ str(day2)
	dateflag = 1
    elif (weekdaywords.find(S2) >= 0) and (dateflag==0):
        bookdate = todayday + datetime.timedelta( (weekdaymap[''.join(time[x]).lower().strip()]-todayday.weekday()) % 7 )
        dateflag = 1
    elif ("weekend".find(S2) >= 0) and (dateflag==0):
        bookdate1 = todayday + datetime.timedelta( (weekdaymap['saturday']-todayday.weekday()) % 7 )
        bookdate2 = todayday + datetime.timedelta( (weekdaymap['saturday']-todayday.weekday()) % 7 )
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
    print(bookdate)
    print("3")
    booktime = "Booktime: "+ booktime+ " "+str(bookdate)

with open("parse.txt", "a") as myfile:
    myfile.write(booktime)
    
str1 = open("parse.txt").read()
print(str1)
