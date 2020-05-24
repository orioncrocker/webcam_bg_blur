############################################################
# Author: Orion Crocker
# Filename: foreground.py
# Date: 05/23/20
# 
# foreground detector
# 	
############################################################

import numpy as np
import cv2 as cv

def apply_edge(frame, edge):
  frame = edge.apply(frame)
  h, w = frame.shape
  cv.line(frame, (0, h), (w, h), (255, 255, 255), thickness=2)
  return cv.medianBlur(frame, 5)


def get_contours(frame):
  _, thresh = cv.threshold(frame, thresh=0.0, maxval=255.0, type=cv.THRESH_BINARY)
  _, contours, hierarchy = cv.findContours(thresh, 0, cv.CHAIN_APPROX_TC89_KCOS)
  return contours


def start(webcam):
  # this works for now, but needs to be a better solution
  contour_num = 3

  threshold = 100
  shadows = False
  time = 250
  edge = cv.createBackgroundSubtractorKNN(history=time, dist2Threshold=threshold, detectShadows=shadows)

  avg_contours = []

  while True:
    _, frame = webcam.read()
    mask = apply_edge(frame, edge)
    contours = get_contours(mask)

    if len(avg_contours) >= contour_num:
      avg_contours = avg_contours[1:]
    avg_contours.append(max(contours, key=cv.contourArea))

    if len(avg_contours) >= contour_num:
      sorted_contours = avg_contours.copy()
      sorted(sorted_contours, key=cv.contourArea)
      cover = frame.copy()
      cv.drawContours(cover, avg_contours, 0, (255,255,255), cv.FILLED)
      cv.imshow("image", cover)

    cv.imshow("mask", mask)

    key = cv.waitKey(33)
    if key == 27:
      break

  print("break!")
