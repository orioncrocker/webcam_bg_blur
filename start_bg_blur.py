############################################################
# Author: Orion Crocker
# Filename: start_bg_blur.py
# Date: 05/23/20
# 
# webcam_bg_blur
# 	start script for webcam_bg_blur
############################################################

import sys
import cv2 as cv
import foreground as fg

def start(webcam, k_size):
  edge = fg.get_edge(100, False, 200)

  contour_num = 3
  avg_contours = []

  while True:
    _, frame = webcam.read()
    mask = fg.apply_edge(frame, edge)
    contours = fg.get_contours(mask)

    if len(avg_contours) >= contour_num:
      avg_contours = avg_contours[1:]
    avg_contours.append(max(contours, key=cv.contourArea))
    contours = avg_contours

    result = fg.blur_bg(frame, contours, k_size)
    cv.imshow('Webcam feed', result)

    if cv.waitKey(33) == 27:
      break

def main():
  webcam = cv.VideoCapture(0)
  if webcam.isOpened() and fg.version_check():
    print("\nPress ESC to quit.")

    kernel = 21
    if len(sys.argv) > 1:
      kernel = int(sys.argv[1])
    start(webcam, kernel)

  else:
    print("Couldn't access your webcam! Is it plugged in?")


if __name__ == '__main__':
  main()
