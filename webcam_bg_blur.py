import numpy as np
import cv2 as cv

def start(webcam):
  contour_num = 10
  shadows = False
  time = 500
  knn_edge = cv.createBackgroundSubtractorKNN(history=time, detectShadows=shadows)
  avg_contours = []

  while True:
    rval, frame = webcam.read()
    mask = knn_edge.apply(frame)
    mask = cv.GaussianBlur(mask, (3,3), cv.BORDER_DEFAULT)
    ret, thresh = cv.threshold(mask, thresh=0.0, maxval=255.0, type=cv.THRESH_BINARY+cv.THRESH_OTSU)
    frame2, contours, hierarchy = cv.findContours(thresh, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    largest = max(contours, key=cv.contourArea)

    if len(avg_contours) >= contour_num:
      avg_contours = avg_contours[1:]
    avg_contours.append(largest)

    cv.drawContours(frame, avg_contours, -1, (0,255,0), -1)

    cv.imshow("mask", mask)
    cv.imshow("image", frame)

    key = cv.waitKey(33)
    if key == 27:
      break
