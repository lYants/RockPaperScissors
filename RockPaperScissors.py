import cv2
import time
import HandTrackingModule as htm
import numpy as np
import math
import random

#Time variables
prevTime = 0 
frame_count = 0
#Hand variables
thumb, index, middle, ring, pinky = 4,8,12,16,20
currentHand = 0
hands = ["Nothing", "Rock", "Paper", "Scissors"]
#Image/text variables
cap = cv2.VideoCapture(0)
detector = htm.handDetector(maxHands=1, detectionCon=0.7)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2
color = (255, 255, 255)  # white
thickness = 3


def isClosed(positions,finger):
    #Needs exception when finger == thumb (= 4)
    if math.hypot(positions[finger][1]-positions[finger-3][1],positions[finger][2]-positions[finger-3][2]) < 70:
        return True
    else:
        return False
    

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    canvas = np.zeros((720, 1280, 3), dtype=np.uint8) 

    if frame_count < 40:
        cv2.putText(canvas,"Rock...",(15,75),font,font_scale,color,thickness,cv2.LINE_AA)
    elif 40 <= frame_count < 80:
        cv2.putText(canvas,"Paper...",(15,75),font,font_scale,color,thickness,cv2.LINE_AA)
    elif 80 <= frame_count < 120:
        cv2.putText(canvas,"Scissors...",(15,75),font,font_scale,color,thickness,cv2.LINE_AA)
    else:
        cv2.putText(canvas,"Shoot!",(15,75),font,font_scale,color,thickness,cv2.LINE_AA)

        positions = detector.findPosition(img)
        if len(positions)!=0:
            if isClosed(positions,pinky) and isClosed(positions,ring):
                if isClosed(positions,index) and isClosed(positions,middle):
                    if currentHand != 1:
                        currentHand = 1
                else:
                    if currentHand != 3:
                        currentHand = 3
            else:
                if currentHand != 2:
                    currentHand = 2
    
    if frame_count > 135:
        break

    #FPS calculations and printing on screen
    curTime = time.time()
    fps = 1/(curTime-prevTime)
    prevTime = curTime
    cv2.putText(img, f'FPS: {int(fps)}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    #Small camera on screen
    cam_frame = cv2.resize(img,(320,240))
    x_offset = 1280 - 320
    y_offset = 720 - 240
    canvas[y_offset:y_offset+240, x_offset:x_offset+320] = cam_frame
    
    frame_count+=1
    cv2.imshow("RPS-game",canvas)
    cv2.waitKey(1)

sol = random.randint(1,3)

canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

cv2.putText(canvas,f'The computer chose: {hands[sol]}',(15,75),font,font_scale,color,thickness,cv2.LINE_AA)
cv2.putText(canvas,f'You chose: {hands[currentHand]}',(15,125),font,font_scale,color,thickness,cv2.LINE_AA)
cv2.imshow("RPS-game",canvas)
cv2.waitKey(3000)

if currentHand == sol:
    text = "Tied!"
elif currentHand-1 == sol or (currentHand==1 and sol == 3):
    text = "You Won :)"
else:
    text = "You Lost :("

canvas = np.zeros((720, 1280, 3), dtype=np.uint8) 
cv2.putText(canvas,text,(15,75),font,font_scale,color,thickness,cv2.LINE_AA)
cv2.imshow("RPS-game",canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()