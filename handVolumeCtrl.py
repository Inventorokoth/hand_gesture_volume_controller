import math
import time
import pycaw
import cv2 as cv
import numpy as np
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import handtrackModule as htm

wCam, hcam = 640,480
cap= cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hcam)
prevTime=0
currTime=0

detector =htm.handDetector(detectionCon=1)


devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
volume=cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
volBar=400
volper=400
vol=0
# print(volRange)

while True:
    isTrue, frame=cap.read()
    frame=detector.findHands(frame)
    lmlist=detector.findPosition(frame,draw=False)
    
    if len(lmlist)!=0:
        print(lmlist[4],lmlist[8])
        
        x1,y1= lmlist[4][1], lmlist[4][2]
        x2,y2= lmlist[8][1], lmlist[8][2]
        cx,cy=(x1+x2) // 2 , (y1+y2) // 2
        cv.circle(frame,(x1,y1),7,(255,0,0),cv.FILLED)
        cv.circle(frame,(x2,y2),7,(255,0,0),cv.FILLED)
        cv.circle(frame,(cx,cy),7,(255,0,0),cv.FILLED)
        cv.line(frame,(x1,y1),(x2,y2),(255,0,255),3)
        
        length=math.hypot(x2-x1, y2-y1)
        print(length)
        
        vol=np.interp(length,[20,185],[minVol,maxVol])
        volBar=np.interp(length,[20,200],[400,150])
        volper=np.interp(length,[20,200],[0,100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        
        
        if length<50:
          cv.circle(frame,(cx,cy),7,(0,255,255),cv.FILLED)  
          
    cv.rectangle(frame,(50,150),(85,400),(255,0,0),3)  
    cv.rectangle(frame,(50,int(volBar)),(85,400),(255,0,0),cv.FILLED)  
    cv.putText(frame,f'{int(volper)}%',(10,450),cv.FONT_HERSHEY_PLAIN,3,(122,255,255),3)
        # frame=cv.flip(frame,1) #horizontally flipping the image 
    currTime=time.time()
    fps= 1/(currTime-prevTime)  
    prevTime=currTime
    cv.putText(frame,f'{int(fps)}',(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)  
# cap.release()
    if cv.waitKey(1) & 0xFF==ord('d'):
             break
    cv.imshow('Video', frame)
    cv.waitKey(1)
    