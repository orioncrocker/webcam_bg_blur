############################################################
# Author: Orion Crocker
# Filename: face_detect.py
# Date: 05/23/20
# 
# face detection
# 	detect largest face and blur the rest of the image
############################################################

import cv2 as cv
import numpy as np

def start(webcam):
    file = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

    while True:
        _, frame = webcam.read()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        faces = file.detectMultiScale(hsv, 1.3, 5)
        circle = frame.copy()
        for face in faces:
            circle = cv.circle(frame, (face.x,face.y), 10, (face.x+face.w,face.y+face.h), (0,255,0),2)

        cv.imshow("your face!", circle)

        key = cv.waitKey(33)
        if key == 27:
            break
