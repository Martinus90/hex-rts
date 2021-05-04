import matplotlib.pyplot as plt
from settings import * 
from random import random
import math
import pydoc as pdw

class doc_generator(object):
    """
    Generating documentation based on single dictionary
    """
    def __init__(self, dictionary):
        """
        Construct of new documentation

        :param dictionary["Args"]: Args
        :param dictionary["Returns"]: Returns
        :param dictionary["Raises"]: Raises
        :param dictionary["Attributes"]: Attributes
        :param dictionary["Summary"]: Summary
        :param dictionary["Description"]: Description
        """

        self.agruments = dictionary["Args"]
        self.returns = dictionary["Returns"]
        self.raises = dictionary["Raises"]
        self.attributes = dictionary["Attributes"]
        self.summary = dictionary["Summary"]
        self.description = dictionary["Description"]

    def do_html(self):
        """
        Function that generate and save documentation
        """
        pdw.writedoc('testy')

d = doc_generator({"Args" : None, "Returns" : None, "Raises" : None, "Attributes" : None, "Summary": None, "Description": None})
#d.do_html()


print(ctts(RED))
print(plt.style.available)

plt.style.use('dark_background')
#seaborn-dark
#plt.style.use('seaborn-dark')
#plt.rcParams['axes.facecolor'] = ctts(BLACK)
#plt.rcParams['figure.facecolor'] = ctts(DARKGREY)
#plt.text
x = []
for d in range(10):
    x.append(d + 1980)
y=[random()*100 for e in range(10)]
z=[random()*100 for e in range(10)]
s=[random()*100 for e in range(10)]
t=[random()*100 for e in range(10)]

w = ((1981, 30), (1982, 25), (1983, 31))
w1 = [a[0] for a in w]
w2 = [a[1] for a in w]
print(w1)
print(w2)

line1, = plt.plot(x,y, ctts(RED))
line2, = plt.plot(x,z, ctts(BLUE))
line3, = plt.plot(w1, w2, ctts(YELLOW))
line4, = plt.plot(x,s, ctts(WHITE))
line5, = plt.plot(x,t, ctts(GREEN))

plt.legend( handles =[line1, line2, line3, line4, line5],
            labels = ['A simple line', 'Second line', 'Third line', 'Forth', 'Fifth'])

#plt.show()

der = ["HAHAHA","Dumb text","Hitler did everything wrong"]

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #0 == PL, 1 == EN
engine.runAndWait()
engine.say("Jakiś tekst do testów.")
#for a in der:
#    engine.say(a)

