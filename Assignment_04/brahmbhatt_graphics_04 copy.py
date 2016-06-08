# Brahmbhatt, Meet
# 1001-119-131
# 2015-03-09
# Assignment_04

from numpy  import *
from math import *
from tkinter import *
from random import random


class cl_world:
    thisVectors = []
    thisFaces =[]
    thisWindow = []
    thisViewpot = []
    thisVectorsForScaling=[]
    vectorVRP = []
    vectorVPN = []
    vectorVUP = []
    vectorPRP = []
    filesOriginalPoints = []
    filesOriginalWindowPoints= []
    cameraObjects=[]
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
        if len(self.thisVectors)>0 and len(self.thisFaces)>0 and len(self.thisWindow)>0 and len(self.thisViewpot)>0:
            self.plotFace2D_final(canvas,self.thisVectors,self.thisFaces,self.thisWindow,self.thisViewpot)
    def rotateBy(self,canvas,degree,around,isLast):
        canvas.delete('all')

        tempVectors = self.filesOriginalPoints
        tempFaces = self.thisFaces
        tempWindow = self.thisWindow
        tempViewPort = self.thisViewpot
        mVectors = []
        firstPoint = tempVectors[0]

        Mat1 = [[0 for x in range(4)] for x in range(4)] 
        Mat2 = [[0 for x in range(4)] for x in range(4)] 
        Mat3 = [[0 for x in range(4)] for x in range(4)]
        compositeMat = [[0 for x in range(4)] for x in range(4)]

        #transform to origin
        Mat1[0][0]=1
        Mat1[0][1]=0
        Mat1[0][2]=0
        Mat1[0][3]=-float(firstPoint[0])
        Mat1[1][0]=0
        Mat1[1][1]=1
        Mat1[1][2]=0
        Mat1[1][3]=-float(firstPoint[1])
        Mat1[2][0]=0
        Mat1[2][1]=0
        Mat1[2][2]=1
        Mat1[2][3]=-float(firstPoint[2])
        Mat1[3][0]=0
        Mat1[3][1]=0
        Mat1[3][2]=0
        Mat1[3][3]=1

        if(around==1):
            print ("rotation is around X")
            #rotation around x
            Mat2[0][0]=1
            Mat2[0][1]=0
            Mat2[0][2]=0
            Mat2[0][3]=0
            Mat2[1][0]=0
            Mat2[1][1]=cos(float(degree) * 0.0174532925)
            Mat2[1][2]=-sin(float(degree) * 0.0174532925)
            Mat2[1][3]=0
            Mat2[2][0]=0
            Mat2[2][1]=-Mat2[1][2]
            Mat2[2][2]=Mat2[1][1]
            Mat2[2][3]=0
            Mat2[3][0]=0
            Mat2[3][1]=0
            Mat2[3][2]=0
            Mat2[3][3]=1
        elif(around==2):
            print ("rotation is around Y")
            #rotation around y
            Mat2[0][0]=cos(float(degree) * 0.0174532925)
            Mat2[0][1]=0
            Mat2[0][2]=sin(float(degree) * 0.0174532925)
            Mat2[0][3]=0
            Mat2[1][0]=0
            Mat2[1][1]=1
            Mat2[1][2]=0
            Mat2[1][3]=0
            Mat2[2][0]=-Mat2[0][2]
            Mat2[2][1]=0
            Mat2[2][2]=Mat2[0][0]
            Mat2[2][3]=0
            Mat2[3][0]=0
            Mat2[3][1]=0
            Mat2[3][2]=0
            Mat2[3][3]=1
        elif(around==3):
            print ("rotation is around Z")
            #rotation around z
            Mat2[0][0]=cos(float(degree) * 0.0174532925)
            Mat2[0][1]=-sin(float(degree) * 0.0174532925)
            Mat2[0][2]=0
            Mat2[0][3]=0
            Mat2[1][0]=-Mat2[0][1]
            Mat2[1][1]=Mat2[0][0]
            Mat2[1][2]=0
            Mat2[1][3]=0
            Mat2[2][0]=0
            Mat2[2][1]=0
            Mat2[2][2]=1
            Mat2[2][3]=0
            Mat2[3][0]=0
            Mat2[3][1]=0
            Mat2[3][2]=0
            Mat2[3][3]=1

        compositeMat = self.matrixMultiplication4x4(Mat1,Mat2)

        

        #transform again to original point
        Mat3[0][0]=1
        Mat3[0][1]=0
        Mat3[0][2]=0
        Mat3[0][3]=float(firstPoint[0])
        Mat3[1][0]=0
        Mat3[1][1]=1
        Mat3[1][2]=0
        Mat3[1][3]=float(firstPoint[1])
        Mat3[2][0]=0
        Mat3[2][1]=0
        Mat3[2][2]=1
        Mat3[2][3]=float(firstPoint[2])
        Mat3[3][0]=0
        Mat3[3][1]=0
        Mat3[3][2]=0
        Mat3[3][3]=1

        compositeMat = self.matrixMultiplication4x4(compositeMat,Mat3)

        for vector in tempVectors:
            temp = []
            Xtemp2DVector=[[0 for x in range(1)] for x in range(4)] 
            Xtemp2DVector[0][0]=float(vector[0])
            Xtemp2DVector[1][0]=float(vector[1])
            Xtemp2DVector[2][0]=float(vector[2])
            Xtemp2DVector[3][0]=1.0
            Xtemp2DVector = self.matrixMultiplication4x1(Mat2,Xtemp2DVector)
            temp=[Xtemp2DVector[0][0],Xtemp2DVector[1][0],Xtemp2DVector[2][0]]
            mVectors.append(temp)
        self.filesOriginalPoints=mVectors
        self.plotFace2D(canvas,mVectors,self.thisFaces,self.filesOriginalWindowPoints,self.thisViewpot,self.vectorVRP,self.vectorVPN,self.vectorVUP,self.vectorPRP)

    def doTranslation(self,canvas,xtranslate,ytranslate,ztranslate):
        canvas.delete('all')

        tempVectors = self.thisVectors
        tempFaces = self.thisFaces
        tempWindow = self.thisWindow
        tempViewPort = self.thisViewpot
        mVectors = []

        trnaslateMatrix = [[0 for x in range(4)] for x in range(4)]

        trnaslateMatrix[0][0]=1
        trnaslateMatrix[0][1]=0
        trnaslateMatrix[0][2]=0
        trnaslateMatrix[0][3]=xtranslate
        trnaslateMatrix[1][0]=0
        trnaslateMatrix[1][1]=1
        trnaslateMatrix[1][2]=0
        trnaslateMatrix[1][3]=ytranslate
        trnaslateMatrix[2][0]=0
        trnaslateMatrix[2][1]=0
        trnaslateMatrix[2][2]=1
        trnaslateMatrix[2][3]=ztranslate
        trnaslateMatrix[3][0]=0
        trnaslateMatrix[3][1]=0
        trnaslateMatrix[3][2]=0
        trnaslateMatrix[3][3]=1

        for vector in tempVectors:
            temp = []
            Xtemp2DVector=[[0 for x in range(1)] for x in range(4)] 
            Xtemp2DVector[0][0]=float(vector[0])
            Xtemp2DVector[1][0]=float(vector[1])
            Xtemp2DVector[2][0]=float(vector[2])
            Xtemp2DVector[3][0]=1.0
            Xtemp2DVector = self.matrixMultiplication4x1(trnaslateMatrix,Xtemp2DVector)
            temp=[Xtemp2DVector[0][0],Xtemp2DVector[1][0],Xtemp2DVector[2][0]]
            mVectors.append(temp)
        self.plotFace2D_final(canvas,mVectors,tempFaces,tempWindow,tempViewPort)

    def plotViewPorts(self,canvas):
        print ("number of objects: %s" % len(self.cameraObjects))
        temp_width=canvas.cget("width")
        temp_height=canvas.cget("height")

        for tCameraObject in self.cameraObjects:
            tempViewPort =tCameraObject.cViewPort
            tx_min = float(tempViewPort[0])
            ty_min = float (tempViewPort[1])
            tx_max = float(tempViewPort[2])
            ty_max = float(tempViewPort[3])
            tempv = [tx_min * float(temp_width),ty_min * float(temp_height), tx_max * float(temp_width), ty_max * float(temp_height)]
            self.objects.append(canvas.create_rectangle(tempv,outline='black',width = '3'))


    def updateCameraList(self,canvas,cameraObjectList = []):
        self.mainCameraObjectList = cameraObjectList
    def scaleBy(self,canvas,xScale,yScale,zScale,isLast):
        canvas.delete('all')
        temp_width=canvas.cget("width")
        temp_height=canvas.cget("height")
        if(len(self.thisVectorsForScaling)==0):
            self.thisVectorsForScaling=self.thisVectors
        tempVectors = self.thisVectorsForScaling
        tempFaces = self.thisFaces
        tempWindow = self.thisWindow

        tempViewPort = self.thisViewpot
        mVectors = []
        firstPoint = tempVectors[0]

        Mat1 = [[0 for x in range(4)] for x in range(4)] 
        Mat2 = [[0 for x in range(4)] for x in range(4)] 
        Mat3 = [[0 for x in range(4)] for x in range(4)]
        compositeMat = [[0 for x in range(4)] for x in range(4)]

        #transform to origin
        Mat1[0][0]=1
        Mat1[0][1]=0
        Mat1[0][2]=0
        Mat1[0][3]=-float(firstPoint[0])
        Mat1[1][0]=0
        Mat1[1][1]=1
        Mat1[1][2]=0
        Mat1[1][3]=-float(firstPoint[1])
        Mat1[2][0]=0
        Mat1[2][1]=0
        Mat1[2][2]=1
        Mat1[2][3]=-float(firstPoint[2])
        Mat1[3][0]=0
        Mat1[3][1]=0
        Mat1[3][2]=0
        Mat1[3][3]=1

        #scaling
        Mat2[0][0]=xScale
        Mat2[0][1]=0
        Mat2[0][2]=0
        Mat2[0][3]=0
        Mat2[1][0]=0
        Mat2[1][1]=yScale
        Mat2[1][2]=0
        Mat2[1][3]=0
        Mat2[2][0]=0
        Mat2[2][1]=0
        Mat2[2][2]=zScale
        Mat2[2][3]=0
        Mat2[3][0]=0
        Mat2[3][1]=0
        Mat2[3][2]=0
        Mat2[3][3]=1

        compositeMat = self.matrixMultiplication4x4(Mat1,Mat2)

        

        #transform again to original point
        Mat3[0][0]=1
        Mat3[0][1]=0
        Mat3[0][2]=0
        Mat3[0][3]=float(firstPoint[0])
        Mat3[1][0]=0
        Mat3[1][1]=1
        Mat3[1][2]=0
        Mat3[1][3]=float(firstPoint[1])
        Mat3[2][0]=0
        Mat3[2][1]=0
        Mat3[2][2]=1
        Mat3[2][3]=float(firstPoint[2])
        Mat3[3][0]=0
        Mat3[3][1]=0
        Mat3[3][2]=0
        Mat3[3][3]=1

        compositeMat = self.matrixMultiplication4x4(compositeMat,Mat3)

        
        for vector in tempVectors:
            temp = []
            Xtemp2DVector=[[0 for x in range(1)] for x in range(4)] 
            Xtemp2DVector[0][0]=float(vector[0])
            Xtemp2DVector[1][0]=float(vector[1])
            Xtemp2DVector[2][0]=float(vector[2])
            Xtemp2DVector[3][0]=1.0
            Xtemp2DVector = self.matrixMultiplication4x1(compositeMat,Xtemp2DVector)
            temp=[Xtemp2DVector[0][0],Xtemp2DVector[1][0],Xtemp2DVector[2][0]]
            mVectors.append(temp)
        self.plotFace2D_final(canvas,mVectors,tempFaces,tempWindow,tempViewPort)
        if(isLast==1):
            self.thisVectorsForScaling=[]

    def matrixMultiplication4x4(self,Mat1 = [[0 for x in range(4)] for x in range(4)], Mat2 = [[0 for x in range(4)] for x in range(4)]):
        compositeMat = [[0 for x in range(4)] for x in range(4)]
        for x in range(4):
            for y  in range (4):
                sum1 = 0
                for z in range(4):
                    sum1=sum1+Mat2[x][z]*Mat1[z][y]
                compositeMat[x][y] = sum1

        return compositeMat

    def matrixMultiplication4x1(self,Mat2 = [[0 for x in range(4)] for x in range(4)],Mat1 = [[0 for x in range(1)] for x in range(4)]):
        compositeMat = [[0 for x in range(1)] for x in range(4)] 
        compositeMat[0][0] = float(Mat2[0][0])*float(Mat1[0][0]) + float(Mat2[0][1])*float(Mat1[1][0]) + float(Mat2[0][2])*float(Mat1[2][0]) + float(Mat2[0][3])*float(Mat1[3][0])
        compositeMat[1][0] = float(Mat2[1][0])*float(Mat1[1][0]) + float(Mat2[1][1])*float(Mat1[1][0]) + float(Mat2[1][2])*float(Mat1[2][0]) + float(Mat2[1][3])*float(Mat1[3][0])
        compositeMat[2][0] = float(Mat2[2][0])*float(Mat1[2][0]) + float(Mat2[2][1])*float(Mat1[1][0]) + float(Mat2[2][2])*float(Mat1[2][0]) + float(Mat2[2][3])*float(Mat1[3][0])
        compositeMat[3][0] = float(Mat2[3][0])*float(Mat1[3][0]) + float(Mat2[3][1])*float(Mat1[1][0]) + float(Mat2[3][2])*float(Mat1[2][0]) + float(Mat2[3][3])*float(Mat1[3][0])
        return compositeMat


    def plotFace2D(self,canvas,vectors=[],faces=[],window=[],viewport=[],TvectorVRP=[],TvectorVPN=[],TvectorVUP=[],TvectorPRP=[]):
        canvas.delete('all')
        self.vectorVRP=TvectorVRP[:]
        self.vectorVRP.append(1.0)
        self.vectorVPN=TvectorVPN[:]
        self.vectorVPN.append(1.0)
        self.vectorVUP=TvectorVUP[:]
        self.vectorVUP.append(1.0)
        self.vectorPRP=TvectorPRP[:]
        self.vectorPRP.append(1.0)

        Mat1 = [[0 for x in range(4)] for x in range(4)] 
        Mat2 = [[0 for x in range(4)] for x in range(4)] 
        Mat3 = [[0 for x in range(4)] for x in range(4)] 
        Mat4 = [[0 for x in range(4)] for x in range(4)] 
        Mat5 = [[0 for x in range(4)] for x in range(4)] 
        Mat6 = [[0 for x in range(4)] for x in range(4)] 
        Mat7 = [[0 for x in range(4)] for x in range(4)] 
        compositeMat = [[0 for x in range(4)] for x in range(4)] 

        Mat1[0][0]=1
        Mat1[0][1]=0
        Mat1[0][2]=0
        Mat1[0][3]=-float(self.vectorVRP[0])
        Mat1[1][0]=0
        Mat1[1][1]=1
        Mat1[1][2]=0
        Mat1[1][3]=-float(self.vectorVRP[1])
        Mat1[2][0]=0
        Mat1[2][1]=0
        Mat1[2][2]=1
        Mat1[2][3]=-float(self.vectorVRP[2])
        Mat1[3][0]=0
        Mat1[3][1]=0
        Mat1[3][2]=0
        Mat1[3][3]=1

        newVPN=[[0 for x in range(1)] for x in range(4)] 
        newVPN[0][0]=float(self.vectorVPN[0])
        newVPN[1][0]=float(self.vectorVPN[1])
        newVPN[2][0]=float(self.vectorVPN[2])
        newVPN[3][0]=float(self.vectorVPN[3])

        newVUP=[[0 for x in range(1)] for x in range(4)]
        newVUP[0][0]=float(self.vectorVUP[0])
        newVUP[1][0]=float(self.vectorVUP[1])
        newVUP[2][0]=float(self.vectorVUP[2])
        newVUP[3][0]=float(self.vectorVUP[3])

        newVRP=[[0 for x in range(1)] for x in range(4)]
        newVRP[0][0]=float(self.vectorVRP[0])
        newVRP[1][0]=float(self.vectorVRP[1])
        newVRP[2][0]=float(self.vectorVRP[2])
        newVRP[3][0]=float(self.vectorVRP[3])

        newVRP1=[[0 for x in range(1)] for x in range(4)]
        newVRP1[0][0]=float(self.vectorVRP[0])
        newVRP1[1][0]=float(self.vectorVRP[1])
        newVRP1[2][0]=float(self.vectorVRP[2])
        newVRP1[3][0]=float(self.vectorVRP[3])

        newPRP=[[0 for x in range(1)] for x in range(4)]
        newPRP[0][0]=float(self.vectorPRP[0])
        newPRP[1][0]=float(self.vectorPRP[1])
        newPRP[2][0]=float(self.vectorPRP[2])
        newPRP[3][0]=float(self.vectorPRP[3])


        newVRP = self.matrixMultiplication4x1(Mat1,newVRP)

        #Rotation around x Axis
        Mat2[0][0]=1
        Mat2[1][0]=0
        Mat2[2][0]=0
        Mat2[3][0]=0
        Mat2[0][1]=0
        if(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0])==0):
            Mat2[1][1]=1
        else:
            Mat2[1][1]=newVPN[2][0]/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #a
        if(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0])==0):
            Mat2[2][1]=0
        else:
            Mat2[2][1]=newVPN[1][0]/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #b
        Mat2[3][1]=0
        Mat2[0][2]=0
        if(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0])==0):
            Mat2[1][2]=0
        else:
            Mat2[1][2]=-newVPN[1][0]/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #a
        Mat2[2][2]=Mat2[1][1] #a
        Mat2[3][2]=0
        Mat2[0][3]=0
        Mat2[1][3]=0
        Mat2[2][3]=0
        Mat2[3][3]=1

        compositeMat = self.matrixMultiplication4x4(Mat2,Mat1)
        
        newVPN = self.matrixMultiplication4x1(Mat2,newVPN)
        newVRP = self.matrixMultiplication4x1(Mat2,newVRP)
        newVUP = self.matrixMultiplication4x1(Mat2,newVUP)

        #Rotation around y Axis
        Mat3[0][0] = newVPN[2][0]/(newVPN[2][0]*newVPN[2][0] + newVPN[0][0]*newVPN[0][0])**(1/2)
        Mat3[0][1]=0
        Mat3[0][2]=-newVPN[0][0]/(newVPN[2][0]*newVPN[2][0] + newVPN[0][0]*newVPN[0][0])**(1/2)
        Mat3[0][3]=0
        Mat3[1][0]=0
        Mat3[1][1]=1
        Mat3[1][2]=0
        Mat3[1][3]=0
        Mat3[2][0]=-Mat3[0][2]
        Mat3[2][1]=0
        Mat3[2][2]=Mat3[0][0]
        Mat3[2][3]=0
        Mat3[3][0]=0
        Mat3[3][1]=0
        Mat3[3][2]=0
        Mat3[3][3]=1

        newVPN = self.matrixMultiplication4x1(Mat3,newVPN)
        newVRP = self.matrixMultiplication4x1(Mat3,newVRP)
        newVUP = self.matrixMultiplication4x1(Mat3,newVUP)
        compositeMat = self.matrixMultiplication4x4(compositeMat,Mat3)
        


        #Rotation around z Axis
        Mat4[0][0]=newVUP[1][0]/(newVUP[1][0]*newVUP[1][0]+newVUP[0][0]*newVUP[0][0])**(1/2)
        Mat4[0][1]=-newVUP[0][0]/(newVUP[1][0]*newVUP[1][0]+newVUP[0][0]*newVUP[0][0])**(1/2)
        Mat4[0][2]=0
        Mat4[0][3]=0
        Mat4[1][0]=-Mat4[0][1]
        Mat4[1][1]=Mat4[0][0]
        Mat4[1][2]=0
        Mat4[1][3]=0
        Mat4[2][0]=0
        Mat4[2][1]=0
        Mat4[2][2]=1
        Mat4[2][3]=0
        Mat4[3][0]=0
        Mat4[3][1]=0
        Mat4[3][2]=0
        Mat4[3][3]=1

        newVPN = self.matrixMultiplication4x1(Mat4,newVPN)
        newVRP = self.matrixMultiplication4x1(Mat4,newVRP)
        newVUP = self.matrixMultiplication4x1(Mat4,newVUP)
        compositeMat = self.matrixMultiplication4x4(compositeMat,Mat4)

        uWidth = (float(window[0])+float(window[1]))/2
        vWidth = (float(window[2])+float(window[3]))/2

        #Shear
        Mat5[0][0]=1
        Mat5[0][1]=0
        Mat5[0][2]=-(newPRP[0][0]-uWidth)/newPRP[2][0]
        Mat5[0][3]=0
        Mat5[1][0]=0
        Mat5[1][1]=1
        Mat5[1][2]=-(newPRP[1][0]-vWidth)/newPRP[2][0]
        Mat5[1][3]=0
        Mat5[2][0]=0
        Mat5[2][1]=0
        Mat5[2][2]=1
        Mat5[2][3]=0
        Mat5[3][0]=0
        Mat5[3][1]=0
        Mat5[3][2]=0
        Mat5[3][3]=1

        
        newVRP = self.matrixMultiplication4x1(Mat5,newVRP)
        newPRP = self.matrixMultiplication4x1(Mat5,newPRP)
        compositeMat = self.matrixMultiplication4x4(compositeMat,Mat5)

        tempa=0
        tempb=0
        tempc=0
        scalx=1
        scaly=1
        scalz=1
        if(float(window[1])>float(window[0])):
            tempa = - float(window[0])
            scalx = 1/(float(window[1])-float(window[0]))
        else:
            tempa = - float(window[1])
            scalx = 1/(float(window[0])-float(window[1]))
        if(float(window[3])>float(window[2])):
            tempb = - float(window[2])
            scaly = 1/(float(window[3])-float(window[2]))
        else:
            tempb = - float(window[3])
            scaly = 1/(float(window[2])-float(window[3]))
        
        if(float(window[5])>float(window[4])):
            tempc = - float(window[4])
            scalz = 1/(float(window[5])-float(window[4]))
        else:
            tempc = - float(window[5])
            scalz = 1/(float(window[4])-float(window[5]))

        #Transform:
        Mat6[0][0]=1
        Mat6[0][1]=0
        Mat6[0][2]=0
        Mat6[0][3]=tempa
        Mat6[1][0]=0
        Mat6[1][1]=1
        Mat6[1][2]=0
        Mat6[1][3]=tempb
        Mat6[2][0]=0
        Mat6[2][1]=0
        Mat6[2][2]=1
        Mat6[2][3]=tempc
        Mat6[3][0]=0
        Mat6[3][1]=0
        Mat6[3][2]=0
        Mat6[3][3]=1

        newVRP = self.matrixMultiplication4x1(Mat6,newVRP)
        newPRP = self.matrixMultiplication4x1(Mat6,newPRP)
        compositeMat = self.matrixMultiplication4x4(compositeMat,Mat6)
        

        #scale
        Mat7[0][0]=scalx
        Mat7[0][1]=0
        Mat7[0][2]=0
        Mat7[0][3]=0
        Mat7[1][0]=0
        Mat7[1][1]=scaly
        Mat7[1][2]=0
        Mat7[1][3]=0
        Mat7[2][0]=0
        Mat7[2][1]=0
        Mat7[2][2]=scalz
        Mat7[2][3]=0
        Mat7[3][0]=0
        Mat7[3][1]=0
        Mat7[3][2]=0
        Mat7[3][3]=1

        newVRP = self.matrixMultiplication4x1(Mat7,newVRP)
        newPRP = self.matrixMultiplication4x1(Mat7,newPRP)
        compositeMat = self.matrixMultiplication4x4(compositeMat,Mat7)
        

        xwinmin = 0
        ywinmin = 0
        xwinmax = 1
        ywinmax = 1

        tempWindowVector = [xwinmin,ywinmin,xwinmax,ywinmax]

        


        # sx = (float(viewport[2])-float(viewport[0]))/(xwinmax-xwinmin)
        # sy = (float(viewport[3])-float(viewport[1]))/(ywinmax-ywinmin)
        # temp_width = canvas.cget("width")
        # temp_height = canvas.cget("height")

        
        mainNewPoints = []

        for xVector in vectors:
            xVector.append(1.0)
            Xtemp=[[0 for x in range(1)] for x in range(4)] 
            Xtemp[0][0]=float(xVector[0])
            Xtemp[1][0]=float(xVector[1])
            Xtemp[2][0]=float(xVector[2])
            Xtemp[3][0]=float(xVector[3])
            Xtemp = self.matrixMultiplication4x1(compositeMat,Xtemp)

            mTempVector = [Xtemp[0][0],Xtemp[1][0],Xtemp[2][0]]
            mainNewPoints.append(mTempVector)

        self.plotFace2D_final(canvas,mainNewPoints,faces,tempWindowVector,viewport)
        #     # newX = float(viewport[0]) + sx * (float(Xtemp[0][0]))
        #     # newY = float(viewport[1]) + sy * (1-float(Xtemp[1][0]))
        #     newX = float(viewport[0]) + sx * (float(Xtemp[0][0]-xwinmin))
        #     newY = float(viewport[1]) + sy * (ywinmax-float(Xtemp[1][0]))
        #     newX = newX * float(temp_width)
        #     newY = newY * float(temp_height)
        #     temp = [newX,newY]
        #     mainNewPoints.append(temp)

        # tx_min = float(viewport[0])
        # ty_min = float (viewport[1])
        # tx_max = float(viewport[2])
        # ty_max = float(viewport[3])

        # tempv = [tx_min * float(temp_width),ty_min * float(temp_height), tx_max * float(temp_width), ty_max * float(temp_height)]
        # self.objects.append(canvas.create_rectangle(tempv,outline='black',width = '3'))
        # x = 0
        # for f in faces:
        #     tempVertex = []
        #     for fx in f:
        #         tempVertex.append(mainNewPoints[int(fx)-1])
        #     module = x % 2
        #     x = x + 1
        #     if module==1:
        #         self.objects.append(canvas.create_polygon(tempVertex,fill = "red",outline = 'black'))
        #     elif module==0:
        #         self.objects.append(canvas.create_polygon(tempVertex,fill = "green",outline = 'black'))
    
    def plotFace2D_final(self,canvas,vectors=[],faces=[],window=[],viewport=[]):
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
            newY = float(viewport[1]) + sy * (float(window[3])-float(xVector[1]))
            newX = newX * float(temp_width)
            newY = newY * float(temp_height)
            temp = [newX,newY]
            mainNewPoints.append(temp)

        tx_min = float(viewport[0])
        ty_min = float (viewport[1])
        tx_max = float(viewport[2])
        ty_max = float(viewport[3])

        tempv = [tx_min * float(temp_width),ty_min * float(temp_height), tx_max * float(temp_width), ty_max * float(temp_height)]
        self.objects.append(canvas.create_rectangle(tempv,outline='black',width = '3'))
        xmin = tx_min * float(temp_width)
        ymin = ty_min * float(temp_height)
        xmax = tx_max * float(temp_width)
        ymax = ty_max * float(temp_height)
        for f in faces:
            numberOfVertex = len(f)
            for x in range(numberOfVertex):
                firstIndex = int (f[x % numberOfVertex])-1
                secondIndex = int (f[(x+1) % numberOfVertex])-1
                vector1 = mainNewPoints[firstIndex]
                vector2 = mainNewPoints[secondIndex]
                if((vector1[0]>=xmin and vector1[0]<=xmax and vector1[1]>=ymin and vector1[1]<=ymax) and (vector2[0]>=xmin and vector2[0]<=xmax and vector2[1]>=ymin and vector2[1]<=ymax)):
                    self.objects.append(canvas.create_line(vector1[0],vector1[1],vector2[0],vector2[1]))
                else:
                    if((vector2[0]-vector1[0])!=0):
                        slopM = (vector2[1]-vector1[1])/(vector2[0]-vector1[0])
                        if((vector1[0]>=xmin and vector1[0]<=xmax and vector1[1]>=ymin and vector1[1]<=ymax)):
                            #vector1 is inside the box
                            
                            if(vector2[0]<=xmin):
                                #intersection with left plan
                                yPoint = slopM*(xmin-vector1[0])+vector1[1]
                                if(yPoint>=ymin and yPoint<=ymax):
                                    self.objects.append(canvas.create_line(vector1[0],vector1[1],xmax,yPoint))
                                    continue
                            elif(vector2[0]>=xmax):
                                #intersection with right plan
                                yPoint = slopM*(xmax-vector1[0])+vector1[1]
                                if(yPoint>=ymin and yPoint<=ymax):
                                    self.objects.append(canvas.create_line(vector1[0],vector1[1],xmax,yPoint))
                                    continue

                            if(vector2[1]<=ymin):
                                #intersection with bottom plan    
                                xpoint = vector1[0]+1/(slopM*(ymin-vector1[1]))
                                if(xpoint>=xmin and xpoint<=xmax):
                                    self.objects.append(canvas.create_line(vector1[0],vector1[1],xpoint,ymin))
                                    continue
                            elif(vector2[1]>=ymax):
                                #intersection with top plan    
                                xpoint = vector1[0]+1/(slopM*(ymax-vector1[1]))
                                if(xpoint>=xmin and xpoint<=xmax):
                                    self.objects.append(canvas.create_line(vector1[0],vector1[1],xpoint,ymax))
                                    continue
                            
                            
                            

                        elif((vector2[0]>=xmin and vector2[0]<=xmax and vector2[1]>=ymin and vector2[1]<=ymax)):
                            #vector2 is inside the box
                            if(vector1[0]<=xmin):
                                #intersection with left plan
                                yPoint = slopM*(xmin-vector1[0])+vector1[1]
                                if(yPoint>=ymin and yPoint<=ymax):
                                    self.objects.append(canvas.create_line(vector2[0],vector2[1],xmax,yPoint))
                                    continue
                            elif(vector1[0]>=xmax):
                                #intersection with right plan
                                yPoint = slopM*(xmax-vector1[0])+vector1[1]
                                if(yPoint>=ymin and yPoint<=ymax):
                                    self.objects.append(canvas.create_line(vector2[0],vector2[1],xmax,yPoint))
                                    continue

                            if(vector1[1]<=ymin):
                                #intersection with bottom plan    
                                xpoint = vector1[0]+1/(slopM*(ymin-vector1[1]))
                                if(xpoint>=xmin and xpoint<=xmax):
                                    self.objects.append(canvas.create_line(vector2[0],vector2[1],xpoint,ymin))
                                    continue
                            elif(vector1[1]>=ymax):
                                #intersection with top plan    
                                xpoint = vector1[0]+1/(slopM*(ymax-vector1[1]))
                                if(xpoint>=xmin and xpoint<=xmax):
                                    self.objects.append(canvas.create_line(vector2[0],vector2[1],xpoint,ymax))
                                    continue
                        elif((vector1[0]<=xmin and vector1[0]>=xmax and vector1[1]<=ymin and vector1[1]>=ymax) and (vector2[0]<=xmin and vector2[0]>=xmax and vector2[1]<=ymin and vector2[1]>=ymax)):
                            if((vector2[0]-vector1[0])!=0):
                                slopM = (vector2[1]-vector1[1])/(vector2[0]-vector1[0])
                                point1 = []
                                point2 = []
                                point1found = 0
                                point2found = 0
                                yPoint = slopM*(xmin-vector1[0])+vector1[1]
                                if(yPoint>=ymin and yPoint<=ymax):
                                    point1 = [xmin,yPoint]
                                    point1found=1
                                yPoint = slopM*(xmax-vector1[0])+vector1[1]
                                if(yPoint>=ymin and yPoint<=ymax):
                                    if(point1found):
                                        point2 = [xmax,yPoint]
                                        point2found=1
                                    else:
                                        point1 = [xmax,yPoint]
                                        point1found=1
                                xpoint = vector1[0]+1/(slopM*(ymin-vector1[1]))
                                if(xpoint>=xmin and xpoint<=xmax):
                                    if(point1found):
                                        point2 = [xpoint,ymin]
                                        point2found=1
                                    else:
                                        point1 = [xpoint,ymin]
                                        point1found=1
                                xpoint = vector1[0]+1/(slopM*(ymax-vector1[1]))
                                if(xpoint>=xmin and xpoint<=xmax):
                                    if(point1found):
                                        point2 = [xpoint,ymax]
                                        point2found=1
                                    else:
                                        point1 = [xpoint,ymax]
                                        point1found=1

                                if(point1found and point2found):
                                    self.objects.append(canvas.create_line(point1[0],point1[1],point2[0],point2[1]))


                            
        
        # x = 0
        # for f in faces:
        #     tempVertex = []
        #     for fx in f:
        #         tempVertex.append(mainNewPoints[int(fx)-1])
        #     module = x % 2
        #     x = x + 1
        #     if module==1:
        #         self.objects.append(canvas.create_polygon(tempVertex,fill = "red",outline = 'black'))
        #     elif module==0:
        #         self.objects.append(canvas.create_polygon(tempVertex,fill = "green",outline = 'black'))
    def readCameraFile(self):
        # Load camera file:
        fl_obj = open("cameras_04.txt",'r')
        firstCamera = 0
        tempCameraObject = cameraClass(self)
        for line in fl_obj:
                if line[0] == 'c':
                    #its new camera object
                    if(firstCamera==1):
                        self.cameraObjects.append(tempCameraObject)
                    else:
                        firstCamera = 1
                    tempCameraObject = cameraClass(self)
                elif line[0] == 'i':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.cameraName = splitStr[0]
                elif line[0] == 't':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.viewName = splitStr[0]
                elif line[0] == 'r':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.cVRP = splitStr
                elif line[0] == 'n':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.cVPN = splitStr
                elif line[0] == 'u':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.cVUP = splitStr
                elif line[0] == 'p':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.cPRP = splitStr
                elif line[0] == 'w':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.cWindowPort = splitStr
                elif line[0] == 's':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    tempCameraObject.cViewPort = splitStr
        self.cameraObjects.append(tempCameraObject)
                    
        

class cameraClass:
    cVRP=[]
    cPRP=[]
    cVUP=[]
    cVPN=[]
    cWindowPort=[]
    cViewPort=[]
    cFaces=[]
    cVectors=[]
    global cameraName
    global viewName
    def __init__(self,master):
        pass