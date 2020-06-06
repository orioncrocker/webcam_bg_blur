############################################################
# Author: Orion Crocker
# Filename: foreground.py
# Date: 05/23/20
# 
# foreground detector
# 	detects foreground in image based on KNN algorithm
############################################################

import sys
import cv2 as cv
import numpy as np

def version_check():
  correct = True
  if sys.version_info[0] != 3:
    print("This program requires python3!")
    correct = False
  version = float(cv.__version__[:3])
  if version > 3.4 or version < 3.4:
    print("This program was written for opencv-python version 3.4.2.17!")
    print("Any other version might yield differing results, proceed with caution.")
  return correct


def get_edge(threshold, shadows, time):
  edge = cv.createBackgroundSubtractorKNN(history=time,
          dist2Threshold=threshold, detectShadows=shadows)
  return edge


def apply_edge(frame, edge):
  frame = edge.apply(frame)
  x,y = frame.shape
  return cv.medianBlur(frame, 3)


def get_contours(mask):
  _, thresh = cv.threshold(mask, thresh=0.0, maxval=255.0, type=cv.THRESH_BINARY)
  _, contours, hierarchy = cv.findContours(thresh, 0, cv.CHAIN_APPROX_TC89_KCOS)
  return contours


def blur_bg(frame, contours, k):
  frame = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
  mask = frame.copy()
  mask = cv.blur(mask, (k,k))
  cv.drawContours(mask, contours, 0, (0, 0, 0, 0), cv.FILLED)
  frame[np.where((mask != [0, 0, 0, 0]).all(axis=2))] = [0, 0, 0, 0]
  return mask + frame


def layer_bg(frame, bg, contours):
  frame = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
  bg = cv.cvtColor(bg, cv.COLOR_BGR2BGRA)
  cv.drawContours(bg, contours, 0, (0, 0, 0, 0), cv.FILLED)
  frame[np.where((bg != [0, 0, 0, 0]).all(axis=2))] = [0, 0, 0, 0]
  return frame + bg


def display_all(knn, mask, frame, bg):
  knn = cv.cvtColor(knn, cv.COLOR_GRAY2RGB)
  top = np.hstack((knn, mask))
  bot = np.hstack((frame, bg))
  stack = np.vstack((top, bot))
  cv.imshow('all frames', stack)
