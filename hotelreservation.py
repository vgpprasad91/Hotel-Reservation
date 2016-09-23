import os
import re
booking = ""
intentflag = 1
bookingintent = []
bookingcategory = ["flight","shoes","house","dress","software","flower"]
print("Hi I am Mezi, how can I help you?")
os.system("./getmsg.sh")
str1 = open("output.txt").read()
while(intentflag == 1):
    intentflag = 0
    for i in range(len(bookingcategory)):
        if (str1.find(''.join(bookingcategory[i])) >= 0):
            print("Hi, it looks like you are trying to book for a "+''.join(bookingcategory[i])+".\nThis is a restaurant reservation system.\n Can you please enter details for hotel reservation?")
            os.system("./getmsg1.sh")
            str1 = open("output.txt").read()
            intentflag = 1
os.system("./getbash.sh")

