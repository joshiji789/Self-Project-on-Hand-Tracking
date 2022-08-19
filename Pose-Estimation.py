#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2
import mediapipe as mp
import time

class poseDetector():
    def __init__(self,mode=False,complexity=1,landmark=True,esegmentation=False,ssegmentation=True,
                detectionCon=0.5,trackCon=0.5):
    
        self.mode=mode
        self.complexity=complexity
        self.landmark=landmark
        self.esegmentation=esegmentation
        self.ssegmentation=ssegmentation
        self.detectionCon=detectionCon
        self.trackCon=trackCon
       
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.complexity,self.landmark,self.esegmentation,self.ssegmentation,
                                   self.detectionCon,self.trackCon)
    
    def findPose(self,img,draw=True):
        
        
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.pose.process(imgRGB)
    
        #print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
       
        return img
    
    def findPosition(self,img,draw=True):
        lmList=[]
        if self.results.pose_landmarks:
            
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                #print(id,lm)
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
        return lmList
            
    
def main():
    cap=cv2.VideoCapture(0)
    
    pTime=0
    detector=poseDetector()
    
    while True:
        
        success,img=cap.read()
        img=detector.findPose(img)
        lmList=detector.findPosition(img)
        print(lmList)
        
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
    
        cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,4,(255,0,0),4)
    
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        
if __name__=="__main__":
    main()


# In[ ]:




