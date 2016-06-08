# Kolandaiswami Arjunan, Prashanth
# 1001-110-082
# 2016-04-19
# Assignment_04

from numpy  import *
from math import *
from tkinter import *
from random import random
import sys


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
    mainCameraObjectList = []
    firsttimeredisplay =1
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
        if(self.firsttimeredisplay==0):
            canvas.delete('all')    
        else:
            firsttimeredisplay =0
            if(len(self.filesOriginalPoints)>0):
                canvas.delete('all')
                self.doMagic(canvas)
    def rotateBy(self,canvas,degree,around,isLast):
        canvas.delete('all')

        tempVectors = self.mainCameraObjectList[0].cVectors
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
        self.updateVectorFaces(mVectors,self.mainCameraObjectList[0].cFaces)
        self.doMagic(canvas)

    def doTranslation(self,canvas,xtranslate,ytranslate,ztranslate):
        canvas.delete('all')

        tempVectors = self.mainCameraObjectList[0].cVectors
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
        self.filesOriginalPoints=mVectors
        self.updateVectorFaces(mVectors,self.mainCameraObjectList[0].cFaces)
        self.doMagic(canvas)

    def plotViewPorts(self,canvas,cameraObjectList = []):
        self.mainCameraObjectList = cameraObjectList
    def updateVectorFaces(self, tVectors=[], tFaces=[]):
        for x in range(len(self.mainCameraObjectList)):
            self.mainCameraObjectList[x].cVectors = tVectors[:]
            self.mainCameraObjectList[x].cFaces = tFaces[:]

    def updateCameraList(self,canvas,cameraObjectList = []):
        self.mainCameraObjectList = cameraObjectList

        # for tCameraObject in cameraObjectList:
        #     tempViewPort =tCameraObject.cViewPort
        #     print(tempViewPort)
        #     tx_min = float(tempViewPort[0])
        #     ty_min = float (tempViewPort[1])
        #     tx_max = float(tempViewPort[2])
        #     ty_max = float(tempViewPort[3])
        #     tempv = [tx_min * float(temp_width),ty_min * float(temp_height), tx_max * float(temp_width), ty_max * float(temp_height)]
        #     print ("tempv :%s " % tempv)
        #     self.objects.append(canvas.create_rectangle(tempv,outline='black',width = '1'))
        #     self.objects.append(canvas.create_text(tx_min * float(temp_width),ty_min * float(temp_height),text = tCameraObject.cameraName,anchor=W,font="Purisa"))
        #     canvas.update()

    def scaleBy(self,canvas,xScale,yScale,zScale,isLast):
        canvas.delete('all')
        temp_width=canvas.cget("width")
        temp_height=canvas.cget("height")
        if(len(self.thisVectorsForScaling)==0):
            self.thisVectorsForScaling=self.filesOriginalPoints
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
        self.filesOriginalPoints=mVectors
        self.updateVectorFaces(mVectors,self.mainCameraObjectList[0].cFaces)
        self.doMagic(canvas)
        if(isLast==1):
            self.thisVectorsForScaling=[]

    def matrixMultiplication4x4(self,Mat1 = [[0 for x in range(4)] for x in range(4)], Mat2 = [[0 for x in range(4)] for x in range(4)]):
        compositeMat = [[0 for x in range(4)] for x in range(4)]
        for x in range(4):
            for y  in range (4):
                sum1 = 0
                for z in range(4):
                    sum1=sum1+Mat1[x][z]*Mat2[z][y]
                compositeMat[x][y] = sum1

        return compositeMat

    def matrixMultiplication4x1(self,Mat2 = [[0 for x in range(4)] for x in range(4)],Mat1 = [[0 for x in range(1)] for x in range(4)]):
        compositeMat = [[0 for x in range(1)] for x in range(4)] 
        compositeMat[0][0] = float(Mat2[0][0])*float(Mat1[0][0]) + float(Mat2[0][1])*float(Mat1[1][0]) + float(Mat2[0][2])*float(Mat1[2][0]) + float(Mat2[0][3])*float(Mat1[3][0])
        compositeMat[1][0] = float(Mat2[1][0])*float(Mat1[0][0]) + float(Mat2[1][1])*float(Mat1[1][0]) + float(Mat2[1][2])*float(Mat1[2][0]) + float(Mat2[1][3])*float(Mat1[3][0])
        compositeMat[2][0] = float(Mat2[2][0])*float(Mat1[0][0]) + float(Mat2[2][1])*float(Mat1[1][0]) + float(Mat2[2][2])*float(Mat1[2][0]) + float(Mat2[2][3])*float(Mat1[3][0])
        compositeMat[3][0] = float(Mat2[3][0])*float(Mat1[0][0]) + float(Mat2[3][1])*float(Mat1[1][0]) + float(Mat2[3][2])*float(Mat1[2][0]) + float(Mat2[3][3])*float(Mat1[3][0])
        return compositeMat

    def doMagic(self,canvas):
        indexOfCamera = 0
        for tempCameraObject in self.mainCameraObjectList:
            if(tempCameraObject.viewName=="parallel"):
                self.doParallelProjection(canvas,indexOfCamera)
            elif(tempCameraObject.viewName=="perspective"):
                self.doPerspectiveProjection(canvas,indexOfCamera)
            indexOfCamera = indexOfCamera + 1

        # self.doParallelProjection(canvas,2)
        # self.doPerspectiveProjection(canvas,3)

        

    def doParallelProjection(self,canvas,indexOfCameraObject):

        tempParallelVRP = self.mainCameraObjectList[indexOfCameraObject].cVRP
        tempParallelVPN = self.mainCameraObjectList[indexOfCameraObject].cVPN
        tempParallelVUP = self.mainCameraObjectList[indexOfCameraObject].cVUP
        tempParallelPRP = self.mainCameraObjectList[indexOfCameraObject].cPRP
        window = self.mainCameraObjectList[indexOfCameraObject].cWindowPort

        tempParallelVRP.append (1.0)
        tempParallelVPN.append (1.0)
        tempParallelVUP.append (1.0)
        tempParallelPRP.append (1.0)
        view_text = self.mainCameraObjectList[indexOfCameraObject].cameraName
        tempviewport = self.mainCameraObjectList[indexOfCameraObject].cViewPort
        self.objects.append(canvas.create_text(float(tempviewport[0])*float(canvas.cget("width"))+5,float(tempviewport[1])*float(canvas.cget("height"))+6,text=view_text, anchor=W, font=("Purisa",12)))

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
        Mat1[0][3]=-float(tempParallelVRP[0])
        Mat1[1][0]=0
        Mat1[1][1]=1
        Mat1[1][2]=0
        Mat1[1][3]=-float(tempParallelVRP[1])
        Mat1[2][0]=0
        Mat1[2][1]=0
        Mat1[2][2]=1
        Mat1[2][3]=-float(tempParallelVRP[2])
        Mat1[3][0]=0
        Mat1[3][1]=0
        Mat1[3][2]=0
        Mat1[3][3]=1

        newVPN = [[tempParallelVPN[0]],[tempParallelVPN[1]],[tempParallelVPN[2]],[tempParallelVPN[3]]]
        newVUP = [[tempParallelVUP[0]],[tempParallelVUP[1]],[tempParallelVUP[2]],[tempParallelVUP[3]]]
        newVRP = [[tempParallelVRP[0]],[tempParallelVRP[1]],[tempParallelVRP[2]],[tempParallelVRP[3]]]
        newVRP1 = [[tempParallelVRP[0]],[tempParallelVRP[1]],[tempParallelVRP[2]],[tempParallelVRP[3]]]
        newPRP = [[tempParallelPRP[0]],[tempParallelPRP[1]],[tempParallelPRP[2]],[tempParallelPRP[3]]]

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
            Mat2[1][1]=float(newVPN[2][0])/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #a
        if(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0])==0):
            Mat2[2][1]=0
        else:
            Mat2[2][1]=float(newVPN[1][0])/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #b
        Mat2[3][1]=0
        Mat2[0][2]=0
        if(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0])==0):
            Mat2[1][2]=0
        else:
            Mat2[1][2]=-float(newVPN[1][0])/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #a
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
        Mat3[0][0] = float(newVPN[2][0])/(newVPN[2][0]*newVPN[2][0] + newVPN[0][0]*newVPN[0][0])**(1/2)
        Mat3[0][1]=0
        Mat3[0][2]=-float(newVPN[0][0])/(newVPN[2][0]*newVPN[2][0] + newVPN[0][0]*newVPN[0][0])**(1/2)
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
        compositeMat = self.matrixMultiplication4x4(Mat3,compositeMat)
        


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
        compositeMat = self.matrixMultiplication4x4(Mat4,compositeMat)

        uWidth = (float(window[0])+float(window[1]))/2
        vWidth = (float(window[2])+float(window[3]))/2

        #Shear
        Mat5[0][0]=1
        Mat5[0][1]=0
        Mat5[0][2]=-(float(newPRP[0][0])-uWidth)/float(newPRP[2][0])
        Mat5[0][3]=0
        Mat5[1][0]=0
        Mat5[1][1]=1
        Mat5[1][2]=-(float(newPRP[1][0])-vWidth)/float(newPRP[2][0])
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
        compositeMat = self.matrixMultiplication4x4(Mat5,compositeMat)

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
        compositeMat = self.matrixMultiplication4x4(Mat6,compositeMat)
        

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
        compositeMat = self.matrixMultiplication4x4(Mat7,compositeMat)
        

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
        vectors = self.mainCameraObjectList[indexOfCameraObject].cVectors
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

        self.plotFace2D_final_parallel(canvas,mainNewPoints,self.mainCameraObjectList[indexOfCameraObject].cFaces,tempWindowVector,self.mainCameraObjectList[indexOfCameraObject].cViewPort)

    def doPerspectiveProjection(self,canvas,indexOfCameraObject):

        tempParallelVRP = self.mainCameraObjectList[indexOfCameraObject].cVRP
        tempParallelVPN = self.mainCameraObjectList[indexOfCameraObject].cVPN
        tempParallelVUP = self.mainCameraObjectList[indexOfCameraObject].cVUP
        tempParallelPRP = self.mainCameraObjectList[indexOfCameraObject].cPRP
        window = self.mainCameraObjectList[indexOfCameraObject].cWindowPort
        tempviewport = self.mainCameraObjectList[indexOfCameraObject].cViewPort

        view_text = self.mainCameraObjectList[indexOfCameraObject].cameraName

        self.objects.append(canvas.create_text(float(tempviewport[0])*float(canvas.cget("width"))+5,float(tempviewport[1])*float(canvas.cget("height"))+6,text=view_text, anchor=W, font=("Purisa",12)))

        tempParallelVRP.append (1.0)
        tempParallelVPN.append (1.0)
        tempParallelVUP.append (1.0)
        tempParallelPRP.append (1.0)

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
        Mat1[0][3]=-float(tempParallelVRP[0])
        Mat1[1][0]=0
        Mat1[1][1]=1
        Mat1[1][2]=0
        Mat1[1][3]=-float(tempParallelVRP[1])
        Mat1[2][0]=0
        Mat1[2][1]=0
        Mat1[2][2]=1
        Mat1[2][3]=-float(tempParallelVRP[2])
        Mat1[3][0]=0
        Mat1[3][1]=0
        Mat1[3][2]=0
        Mat1[3][3]=1

        newVPN = [[tempParallelVPN[0]],[tempParallelVPN[1]],[tempParallelVPN[2]],[tempParallelVPN[3]]]
        newVUP = [[tempParallelVUP[0]],[tempParallelVUP[1]],[tempParallelVUP[2]],[tempParallelVUP[3]]]
        newVRP = [[tempParallelVRP[0]],[tempParallelVRP[1]],[tempParallelVRP[2]],[tempParallelVRP[3]]]
        newVRP1 = [[tempParallelVRP[0]],[tempParallelVRP[1]],[tempParallelVRP[2]],[tempParallelVRP[3]]]
        newPRP = [[tempParallelPRP[0]],[tempParallelPRP[1]],[tempParallelPRP[2]],[tempParallelPRP[3]]]

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
            Mat2[1][1]=float(newVPN[2][0])/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #a
        if(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0])==0):
            Mat2[2][1]=0
        else:
            Mat2[2][1]=float(newVPN[1][0])/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #b
        Mat2[3][1]=0
        Mat2[0][2]=0
        if(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0])==0):
            Mat2[1][2]=0
        else:
            Mat2[1][2]=-float(newVPN[1][0])/(float(newVPN[1][0])*float(newVPN[1][0]) + float(newVPN[2][0])*float(newVPN[2][0]))**(1/2) #a
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
        Mat3[0][0] = float(newVPN[2][0])/(newVPN[2][0]*newVPN[2][0] + newVPN[0][0]*newVPN[0][0])**(1/2)
        Mat3[0][1]=0
        Mat3[0][2]=-float(newVPN[0][0])/(newVPN[2][0]*newVPN[2][0] + newVPN[0][0]*newVPN[0][0])**(1/2)
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
        compositeMat = self.matrixMultiplication4x4(Mat3,compositeMat)
        


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
        compositeMat = self.matrixMultiplication4x4(Mat4,compositeMat)

        

        #translate PRP to origin
        Mat5[0][0]=1
        Mat5[0][1]=0
        Mat5[0][2]=0
        Mat5[0][3]=-float(tempParallelPRP[0])
        Mat5[1][0]=0
        Mat5[1][1]=1
        Mat5[1][2]=0
        Mat5[1][3]=-float(tempParallelPRP[1])
        Mat5[2][0]=0
        Mat5[2][1]=0
        Mat5[2][2]=1
        Mat5[2][3]=-float(tempParallelPRP[2])
        Mat5[3][0]=0
        Mat5[3][1]=0
        Mat5[3][2]=0
        Mat5[3][3]=1

        uWidth = (float(window[0])+float(window[1]))/2
        vWidth = (float(window[2])+float(window[3]))/2

        newVRP = self.matrixMultiplication4x1(Mat5,newVRP)
        masterPRPCopy = newPRP[:]
        newPRP = [[-float(newVRP[0][0])],[-float(newVRP[1][0])],[-float(newVRP[2][0])],[-float(newVRP[3][0])]]
        compositeMat = self.matrixMultiplication4x4(Mat5,compositeMat)

        #translate PRP to origin
        Mat6[0][0]=1
        Mat6[0][1]=0
        Mat6[0][2]=(-(float(masterPRPCopy[0][0])-uWidth))/float(masterPRPCopy[2][0])
        Mat6[0][3]=0
        Mat6[1][0]=0
        Mat6[1][1]=1
        Mat6[1][2]=(-(float(masterPRPCopy[1][0])-vWidth))/float(masterPRPCopy[2][0])
        Mat6[1][3]=0
        Mat6[2][0]=0
        Mat6[2][1]=0
        Mat6[2][2]=1
        Mat6[2][3]=0
        Mat6[3][0]=0
        Mat6[3][1]=0
        Mat6[3][2]=0
        Mat6[3][3]=1

        newVRP = self.matrixMultiplication4x1(Mat6,newVRP)
        newPRP = [[-float(newVRP[0][0])],[-float(newVRP[1][0])],[-float(newVRP[2][0])],[-float(newVRP[3][0])]]
        compositeMat = self.matrixMultiplication4x4(Mat6,compositeMat)

        scaleX=1
        scaleY=1
        scaleZ=1

        absff42pb7 = abs (float(newVRP[2][0]+float(window[5])))
        absff42pb6 = abs (float(newVRP[2][0]+float(window[4])))
        f42pb7 = (float(newVRP[2][0]+float(window[5])))
        f42pb6 = (float(newVRP[2][0]+float(window[4])))
        absf42 = abs(float(newVRP[2][0]))
        b3mib2 = (float(window[1])-float(window[0]))/2
        b5mib4 = (float(window[3])-float(window[2]))/2

        if(absff42pb7 > absff42pb6):
            scaleX = absf42/(b3mib2*f42pb7)
            scaleY = absf42/(b5mib4*f42pb7)
        else:
            scaleX = absf42/(b3mib2*f42pb6)
            scaleY = absf42/(b5mib4*f42pb6)

        if(absff42pb7*absff42pb6 < 0):
           print("Error:Two sided view Volume")
           sys.exit("Error:Two sided view Volume")
        else:
            if(absff42pb7 > absff42pb6):
                scaleZ = 1/(f42pb7)
            else:
                scaleZ = 1/f42pb6
        
        

        #scale
        Mat7[0][0]=scaleX
        Mat7[0][1]=0
        Mat7[0][2]=0
        Mat7[0][3]=0
        Mat7[1][0]=0
        Mat7[1][1]=scaleY
        Mat7[1][2]=0
        Mat7[1][3]=0
        Mat7[2][0]=0
        Mat7[2][1]=0
        Mat7[2][2]=scaleZ
        Mat7[2][3]=0
        Mat7[3][0]=0
        Mat7[3][1]=0
        Mat7[3][2]=0
        Mat7[3][3]=1

        newVRP = self.matrixMultiplication4x1(Mat7,newVRP)
        newPRP = [[-float(newVRP[0][0])],[-float(newVRP[1][0])],[-float(newVRP[2][0])],[-float(newVRP[3][0])]]
        
        compositeMat = self.matrixMultiplication4x4(Mat7,compositeMat)

        xwinmin = -1
        ywinmin = -1
        xwinmax = 1
        ywinmax = 1

        tempWindowVector = [xwinmin,ywinmin,xwinmax,ywinmax]

        
        mainNewPoints = []
        vectors = self.mainCameraObjectList[indexOfCameraObject].cVectors
        for xVector in vectors:
            xVector.append(1.0)
            Xtemp=[[0 for x in range(1)] for x in range(4)] 
            Xtemp[0][0]=float(xVector[0])
            Xtemp[1][0]=float(xVector[1])
            Xtemp[2][0]=float(xVector[2])
            Xtemp[3][0]=float(xVector[3])
            Xtemp = self.matrixMultiplication4x1(compositeMat,Xtemp)
            mTempVector = [Xtemp[0][0]/Xtemp[2][0],Xtemp[1][0]/Xtemp[2][0],Xtemp[2][0]]
            mainNewPoints.append(mTempVector)
        self.plotFace2D_final_perspective(canvas,mainNewPoints,self.mainCameraObjectList[indexOfCameraObject].cFaces,tempWindowVector,self.mainCameraObjectList[indexOfCameraObject].cViewPort)




    
    def plotFace2D_final_parallel(self,canvas,vectors=[],faces=[],window=[],viewport=[]):
        # canvas.delete('all')
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
    def plotFace2D_final_perspective(self,canvas,vectors=[],faces=[],window=[],viewport=[]):
        # canvas.delete('all')
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