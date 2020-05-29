############################################################
# Author: Orion Crocker
# Filename: foreground.py
# Date: 05/23/20
# 
# foreground detector
# 	detects foreground in image based on KNN algorithm
############################################################

import cv2 as cv
import numpy as np

def get_edge():
  threshold = 100
  shadows = False
  time = 100
  edge = cv.createBackgroundSubtractorKNN(history=time,
          dist2Threshold=threshold, detectShadows=shadows)
  return edge


def apply_edge(frame, edge):
  frame = edge.apply(frame)
  x,y = frame.shape
  return cv.medianBlur(frame, 3)


def get_contours(frame):
  _, thresh = cv.threshold(frame, thresh=0.0, maxval=255.0, type=cv.THRESH_BINARY)
  _, contours, hierarchy = cv.findContours(thresh, 0, cv.CHAIN_APPROX_TC89_KCOS)
  return contours


def grabcut(mask, frame):
  trimap = np.copy(mask)



def blur_bg(frame, contours, k):
  mask = frame.copy()
  mask = cv.blur(mask, (k,k))
  cv.drawContours(mask, contours, 0, (0, 0, 0), cv.FILLED)
  frame[np.where((mask != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
  return mask + frame


def layer_bg(frame, bg, contours):
  cv.drawContours(bg, contours, 0, (0, 0, 0), cv.FILLED)
  frame[np.where((bg != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
  return frame + bg


def display_all(knn, mask, frame, bg):
  knn = cv.cvtColor(knn, cv.COLOR_GRAY2RGB)
  top = np.hstack((knn, mask))
  bot = np.hstack((frame, bg))
  stack = np.vstack((top, bot))
  cv.imshow('all frames', stack)


def start(webcam, k_size):
  edge = get_edge()

  contour_num = 3
  avg_contours = []

  while True:
    _, frame = webcam.read()
    mask = apply_edge(frame, edge)
    contours = get_contours(mask)

    #if len(avg_contours) >= contour_num:
    #  avg_contours = avg_contours[1:]
    #avg_contours.append(max(contours, key=cv.contourArea))
    #contours = avg_contours

    result = blur_bg(frame, [max(contours, key=cv.contourArea)], k_size)
    cv.imshow('result', result)

    if cv.waitKey(33) == 27:
      break
