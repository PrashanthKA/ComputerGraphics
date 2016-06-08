# Kolandaiswami Arjunan, Prashanth
# 1001-110-082
# 2015-02-15
# Assignment_01

from numpy  import *
from math import *
from tkinter import *
from random import random


class cl_world:
    thisVectors = []
    thisFaces =[]
    thisWindow = []
    thisViewpot = []
    def __init__(self, objects=[],canvases=[]):
        self.objects=objects
        self.canvases=canvases
        #self.display
        
 
    def add_canvas(self,canvas):
            self.canvases.append(canvas)
            canvas.world=self
    def create_graphic_objects(self,canvas):
        self.objects.append(canvas.create_line(0,0,canvas.cget("width"),canvas.cget("height")))
        self.objects.append(canvas.create_line(canvas.cget("width"),0,0,canvas.cget("height")))
        self.objects.append(canvas.create_oval(int(0.25*int(canvas.cget("width"))),
            int(0.25*int(canvas.cget("height"))),
            int(0.75*int(canvas.cget("width"))),
            int(0.75*int(canvas.cget("height")))))        
    def redisplay(self,canvas,event):

        canvas.delete('all')
        print(self.thisWindow)
        if len(self.thisVectors)>0 and len(self.thisFaces)>0 and len(self.thisWindow)>0 and len(self.thisViewpot)>0:
            self.plotFace2D(canvas,self.thisVectors,self.thisFaces,self.thisWindow,self.thisViewpot)
    def plotFace2D(self,canvas,vectors=[],faces=[],window=[],viewport=[]):
        canvas.delete('all')
        self.thisVectors=vectors[:]
        self.thisFaces=faces[:]
        self.thisWindow=window[:]
        self.thisViewpot=viewport[:]
        mainNewPoints=[]
        temp_width = canvas.cget("width")
        temp_height = canvas.cget("height")
        sx = (float(viewport[2])-float(viewport[0]))/(float(window[2])-float(window[0]))
        sy = (float(viewport[3])-float(viewport[1]))/(float(window[3])-float(window[1]))
        for xVector in vectors:
            newX = float(viewport[0]) + sx * (float(xVector[0])-float(window[0]))
            newY = float(viewport[0]) + sy * (float(window[3])-float(xVector[1]))
            newX = newX * float(temp_width)
            newY = newY * float(temp_height)
            temp = [newX,newY]
            mainNewPoints.append(temp)

        print (self.thisViewpot)
        tx_min = float(viewport[0])
        ty_min = float (viewport[1])
        tx_max = float(viewport[2])
        ty_max = float(viewport[3])

        tempv = [tx_min * float(temp_width),ty_min * float(temp_height), tx_max * float(temp_width), ty_max * float(temp_height)]
        self.objects.append(canvas.create_rectangle(tempv,outline='black',width = '3'))
        x = 0
        for f in faces:
            tempVertex = []
            for fx in f:
                tempVertex.append(mainNewPoints[int(fx)-1])
            module = x % 2
            x = x + 1
            self.objects.append(canvas.create_polygon(tempVertex,fill = "red",outline = 'black'))
            #elif module==0:
                #self.objects.append(canvas.create_polygon(tempVertex,fill = "green",outline = 'black'))
            
            
