import cv2 as cv
import mediapipe as mp
import time
import os
import uuid
import handtrackModule as htt
prevTime=0
currTime=0
cap= cv.VideoCapture(0)
detector=htt.handDetector()
os.mkdir('OpenCV images')

while True:
    success, frame=cap.read()
    frame= detector.findHands(frame)
    lmlist =detector.findPosition(frame)
    if len(lmlist)!=0:
        
        print(lmlist[4])
    currTime=time.time()
    fps= 1/(currTime-prevTime)  
    prevTime=currTime
    cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)  
    
    # outputting our images to a file
    
# cap.release()
# cv.destroyAllWindows()
    if cv.waitKey(1) & 0xFF==ord('d'):
            break
    cv.imshow('Video', frame)
    cv.imwrite(os.path.join('OpenCV images','{}.jpg'.format(uuid.uuid1())),frame)
    cv.waitKey(1)