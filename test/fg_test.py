################################################################################################
# Author: Orion Crocker
# Filename: foreground.py
# Date: 05/12/20
# 
# Foreground detector
# 	Foreground detection test for blur_the_rest
################################################################################################

import cv2

shadows = False
time = 300

mog2 = cv2.createBackgroundSubtractorMOG2(history=time, detectShadows=shadows)
knn = cv2.createBackgroundSubtractorKNN(history=time, detectShadows=shadows)
cv2.namedWindow("preview")

webcam = cv2.VideoCapture(0)

print("Press ESC to stop preview.")

if webcam.isOpened():
  rval, frame = webcam.read()
else:
  rval = False

while rval:
  mog2fg = mog2.apply(frame)
  knnfg = knn.apply(frame)

  cv2.imshow("original", frame)
  cv2.imshow("mog2", mog2fg) 
  cv2.imshow("knn", knnfg)

  rval, frame = webcam.read()

  key = cv2.waitKey(33)
  if key == 27:
    break

cv2.destroyWindow("preview")
