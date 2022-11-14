import cv2 as cv
import mediapipe as mp
import time

cap= cv.VideoCapture(0)

mpHands= mp.solutions.hands
hands= mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
prevTime=0
currTime=0

while True:
    isTrue, frame=cap.read()
    
    # if cv.waitKey(1) & 0xFF==ord('d'):
    #     break
    
    imgRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, channel = frame.shape
                Cx, Cy= int(lm.x*w), int(lm.y*h) 
                print(id ,Cx,Cy)
                # if id==4:
                cv.circle(frame,(Cx,Cy),7,(255,0,0),cv.FILLED)               
            mpDraw.draw_landmarks(frame, handLms,mpHands.HAND_CONNECTIONS)
            
    currTime=time.time()
    fps= 1/(currTime-prevTime)  
    prevTime=currTime
    cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)  
# cap.release()
# cv.destroyAllWindows()
    if cv.waitKey(1) & 0xFF==ord('d'):
             break
    cv.imshow('Video', frame)
    cv.waitKey(1)