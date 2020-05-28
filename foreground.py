############################################################
# Author: Orion Crocker
# Filename: foreground.py
# Date: 05/23/20
# 
# foreground detector
# 	
############################################################

import cv2 as cv
import numpy as np


def apply_edge(frame, edge):
  frame = edge.apply(frame)
  return cv.medianBlur(frame, 3)


def get_contours(frame):
  _, thresh = cv.threshold(frame, thresh=0.0, maxval=255.0, type=cv.THRESH_BINARY)
  _, contours, hierarchy = cv.findContours(thresh, 0, cv.CHAIN_APPROX_TC89_KCOS)
  return contours


def display_all(knn, mask, frame, bg):
  knn = cv.cvtColor(knn, cv.COLOR_GRAY2RGB)
  top = np.hstack((knn, mask))
  bot = np.hstack((frame, bg))
  stack = np.vstack((top, bot))
  cv.imshow('all frames', stack)


def start(webcam):
  # this works for now, but needs to be a better solution
  contour_num = 3

  threshold = 100
  shadows = False
  time = 100
  edge = cv.createBackgroundSubtractorKNN(history=time, dist2Threshold=threshold, detectShadows=shadows)

  avg_contours = []

  while True:
    _, frame = webcam.read()
    mask = apply_edge(frame, edge)
    contours = get_contours(mask)
    knn = mask.copy()
    bg = frame.copy()

    if len(avg_contours) >= contour_num:
      avg_contours = avg_contours[1:]
    avg_contours.append(max(contours, key=cv.contourArea))

    mask = frame.copy()
    cv.drawContours(mask, avg_contours, 0, (0, 0, 0), cv.FILLED)
    frame[np.where((mask != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
    bg = cv.blur(bg, (21,21))
    bg[np.where((frame != [0, 0, 0]).all(axis=2))] = [0, 0, 0]

    bg = bg + frame

    #display_all(knn, mask, frame, bg)
    cv.imshow('result', bg)


    key = cv.waitKey(33)
    if key == 27:
      break

