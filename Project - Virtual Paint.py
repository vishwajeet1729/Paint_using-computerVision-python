import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import os

folderPath="C:/Users\ASUS\PycharmProjects\OpencvPython\Resources\Virtual Paint Photo"
myList=os.listdir(folderPath)
#print(myList)
overlayList = []

for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
#print(len(overlayList))

header=overlayList[0]


################
brushThickness=15
eraserThickness=75
################


cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,100)

drawcolor=(203,192,255)

detector= htm.handDetector(maxHands=1)
xp,yp=0,0

imgCanvas = np.zeros((720,1280,3),np.uint8)

while True:

    #1.Import Image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #2.Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) !=0:
        #print(lmList)
        #tip of Index and Middle fingers
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

    #3. Check Which Finger is Up
        fingers=detector.fingersUp()
        #print(fingers)

     #4. If Selection mode - Two finger are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            #print("Selection Mode")

            #Checking for the Click
            if y1<123:
                if 180 < x1 < 330:
                    header = overlayList[0]
                    #Pink
                    drawcolor=(255,51,255)
                elif 360 < x1 < 500:
                    header = overlayList[1]
                    #Blue
                    drawcolor = (255, 0, 0)
                elif 530 < x1 < 680:
                    header = overlayList[2]
                    #Green
                    drawcolor = (0, 255, 0)
                elif 700 < x1 < 860:
                    header = overlayList[3]
                    #Red
                    drawcolor = (0, 0, 255)
                elif 880 < x1 < 1025:
                    header = overlayList[4]
                    #Yellow
                    drawcolor = (0, 255, 255)
                elif 1075 < x1 < 1276:
                    header = overlayList[5]
                    #Eraser
                    drawcolor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawcolor, cv2.FILLED)

        #5. If Drawing Mode - Index Finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawcolor,cv2.FILLED)
            #print("Drawing Mode")
            if xp==0 and yp==0:
                xp,yp = x1,y1
            if drawcolor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawcolor,brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, brushThickness)
            xp,yp=x1,y1


    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)

    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)

    #Setting the header Image
    img[0:123 , 0:1280] = header
    #img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    cv2.imshow("Output",img)
    #cv2.imshow("Image Canvas",imgCanvas)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break