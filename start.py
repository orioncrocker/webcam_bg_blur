############################################################
# Author: Orion Crocker
# Filename: start.py
# Date: 05/23/20
# 
# webcam_bg_blur
# 	start wrapper for webcam_bg_blur
############################################################

import cv2 as cv
import sys
import webcam_bg_blur

def main():
  webcam = cv.VideoCapture(0)
  if webcam.isOpened():
    if sys.version_info[0] != 3:
      print("This program requires python3!")
      quit()
    version = float(cv.__version__[:3])
    if version > 3.4 or version < 3.4:
      print("This program was written for opencv-python version 3.4.2.17!")
      print("Any other version might yield differing results, proceed with caution.")

    webcam_bg_blur.start(webcam)
  else:
    print("Couldn't access your webcam! Is it plugged in?")


if __name__ == '__main__':
  main()
