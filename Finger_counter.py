# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 10:21:18 2022

@author: joshi
"""

import cv2
import time
import os
import HANDTRACKINGMODULE as htm


cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,500)

folderPath="HAND_SIGN"
myList=os.listdir(folderPath)
print(myList)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)
    
#print(len(overlayList))

pTime=0

detector=htm.handDetector(detectionCon=0.75)

tipids=[4,8,12,16,20]



while True:
    succes, img=cap.read()
    img=detector.findHands(img)
    
    lmList=detector.findPosition(img,draw=False)
    
    if len(lmList)!=0:
        fingers=[]
        
        # Thumb
        # 4
        if lmList[tipids[0]][1] > lmList[tipids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # For Fingers
        for id in range(1,5):
            # 8-6,12-10,16-14,20
            if lmList[tipids[id]][2]<lmList[tipids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                #print("index finger Open")
        
        #print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)
        
        h,w,c=overlayList[totalFingers-1].shape
        img[0:h,0:w]= overlayList[totalFingers-1]
        
        cv2.rectangle(img,(20,255),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(43,375),cv2.FONT_HERSHEY_PLAIN,
                    10,(255,0,0),22)
        
        
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    
    cv2.putText(img,f'fps:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,
                3,(255,0,0),3)
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    
    

