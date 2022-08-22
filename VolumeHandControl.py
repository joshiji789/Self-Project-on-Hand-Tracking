# Guesture control to change the volume
# We will use the previous 
import cv2
import mediapipe as mp
import HANDTRACKINGMODULE as htm
import time
import numpy as np
import math 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#%%
wCam,hCam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

#%%

# Python Core Audio Windows Library, working for both Python2 and Python3.

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=(volume.GetVolumeRange())


minVol=volRange[0]
maxVol=volRange[1]

#%%

detector=htm.handDetector(detectionCon=0.8)

volBar=400
vol=0
volPer=0
while True:
    
    success,img=cap.read()
    img=detector.findHands(img)
    
    lmList=detector.findPosition(img,draw=False)
    
    if len(lmList)!=0:
        print(lmList[4],lmList[8])          # Thumb and index finger
        x1,y1=lmList[4][1],lmList[4][2]     # x1,y1 position of Thumb
        x2,y2=lmList[8][1],lmList[8][2]     # x2,y2 position of Index finger
        cx,cy=(x1+x2)//2,(y1+y2)//2         # Midpoint of line joining thumb and index finger
        
        # Draw circle at (x1,y1)
        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        # Draw circle at (x2,y2)
        cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
    
        # Draw line between (x1,y1) and (x2,y2)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        
        # Draw circle at midpoint in the line joining thumb and finger
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        
        length=math.hypot(x2-x1,y2-y1)
        #print(length)
        
        # Hand range 50 to 300
        # Volume range -65 to 0
        
        vol=np.interp(length,[30,300],[minVol,maxVol])
        volBar=np.interp(length,[30,300],[400,150])
        volPer=np.interp(length,[50,300],[0,100])
        
        # Printing volumne
        print(vol)
        # Set/Control master P.C Volume 
        volume.SetMasterVolumeLevel(vol, None)
        
        # Click botton condition
        if length<50:
            # Fill the circle with green 
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
    
    # Volume Bar 
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
        
        
    # For FPS
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    
    # TEXT of FPS and Volume %
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,255),3)
    cv2.putText(img,f' {int(volPer)} % ',(40,450),cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,255),3)
    
    # Show image
    cv2.imshow("img",img)
    cv2.waitKey(1)
 