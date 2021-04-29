import matplotlib.pyplot as plt
from settings import * 
from random import random
import math

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
engine.setProperty('voice', voices[1].id)
engine.say("Do I exist? What is purpose of my life?")
for a in der:
    engine.say(a)
engine.runAndWait()
