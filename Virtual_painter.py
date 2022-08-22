# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:41:11 2022

@author: joshi
"""

import cv2
import HANDTRACKINGMODULE as htm
import os
import time
import numpy as np

############

brushThicknes=10
eraserThicknes=50

############
folderPath="Header"
myList=os.listdir(folderPath)
print(myList)

overlayList=[]

for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

header=overlayList[0]

drawColor=(70,255,255)

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.handDetector(detectionCon=0.9)
xp,yp=0,0

imgcanvas=np.zeros((720,1280,3),np.uint8)

while True:
    
    #import the image
    success,img=cap.read()
    img=cv2.flip(img,1)
    
    # Find hand landmarks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    
    if len(lmList)!=0:
        
        #print(lmList)
        
        # Tip of index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        
        
        # Checking which fingers are up
        fingers=detector.fingersUp()
        #print(fingers)
        
        # If selection mode - two fingers are up
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            #checking for click
            if y1<125:
                if 250<x1<450:
                    header=overlayList[0]
                    drawColor=(0,255,0)
                elif 550<x1<650:
                    header=overlayList[1]
                    drawColor=(0,0,255)
                elif 700<x1<850:
                    header=overlayList[2]
                    drawColor=(255,0,20)
                elif 900<x1<1200:
                    header=overlayList[3]
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
            
            print("selection mode")
   
                    
        # If drawing mode - index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img,(x1,y1),10,drawColor,cv2.FILLED)
            
            print("Drawing mode")
            
            if xp==0 and yp==0:
                xp,yp=x1,y1
            
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThicknes)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),drawColor,eraserThicknes)
            else:   
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThicknes)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),drawColor,brushThicknes)
            
            xp,yp=x1,y1
    
    imgGray=cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _,imginv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imginv=cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imginv)
    img=cv2.bitwise_or(img,imgcanvas)
    
    # Setting the Header image
    img[0:125,0:1280]=header
    
    img=cv2.addWeighted(img,0.5,imgcanvas,0.5,0)
    cv2.imshow("image",img)
    cv2.imshow("imagecanvas",imgcanvas)
    cv2.imshow("inv",imginv)
    cv2.waitKey(1)
    

