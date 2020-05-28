###########################################################
# Author: Orion Crocker
# Filename: demo.py
# Date: 05/28/20
# 
# Demo
#   Presentation demo for CS 410/510 Computational
# Photography
###########################################################

import sys
import cv2 as cv
import numpy as np
import foreground as fg

def blur_bg_demo(frame, contours):
  mask = frame.copy()
  mask = cv.medianBlur(mask, 21)
  cv.drawContours(mask, contours, -1, (0, 0, 0), cv.FILLED)
  frame[np.where((mask != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
  return mask, frame

def start(webcam):
    edge = fg.get_edge()

    while True:
        _, frame = webcam.read()
        mask = fg.apply_edge(frame, edge)
        cv.imshow('KNN Mask', mask)

        if cv.waitKey(33) == 27:
                break
    cv.destroyAllWindows()

    while True:
        _, frame = webcam.read()
        mask = fg.apply_edge(frame, edge)
        contours = fg.get_contours(mask)

        cv.drawContours(frame, contours, -1, (0,255,0), 4)
        cv.imshow("All contours", frame)

        if cv.waitKey(33) == 27:
            break
    cv.destroyAllWindows()


    contour_num = 3
    avg_contours = []
    while True:
        _, frame = webcam.read()
        mask = fg.apply_edge(frame, edge)
        contours = fg.get_contours(mask)

        if len(avg_contours) >= contour_num:
            avg_contours = avg_contours[1:]
        avg_contours.append(max(contours, key=cv.contourArea))

        cv.drawContours(frame, avg_contours, -1, (0,255,0), 4)
        cv.imshow("Only largest contours", frame)

        if cv.waitKey(33) == 27:
            break
    cv.destroyAllWindows()

    while True:
        _, frame = webcam.read()
        mask = fg.apply_edge(frame, edge)
        contours = fg.get_contours(mask)

        if len(avg_contours) >= contour_num:
            avg_contours = avg_contours[1:]
        avg_contours.append(max(contours, key=cv.contourArea))

        cv.drawContours(frame, avg_contours, -1, (0,255,0), cv.FILLED)
        cv.imshow("Only largest contours filled with green", frame)

        if cv.waitKey(33) == 27:
            break
    cv.destroyAllWindows()

    while True:
        _, frame = webcam.read()
        mask = fg.apply_edge(frame, edge)
        contours = fg.get_contours(mask)

        if len(avg_contours) >= contour_num:
            avg_contours = avg_contours[1:]
        avg_contours.append(max(contours, key=cv.contourArea))

        mask, frame = blur_bg_demo(frame, avg_contours)

        stack = np.hstack((mask, frame))
        cv.imshow('background, foreground', stack)

        if cv.waitKey(33) == 27:
            break

    cv.destroyAllWindows()

    while True:
        _, frame = webcam.read()
        mask = fg.apply_edge(frame, edge)
        contours = fg.get_contours(mask)

        if len(avg_contours) >= contour_num:
            avg_contours = avg_contours[1:]
        avg_contours.append(max(contours, key=cv.contourArea))

        result = fg.blur_bg(frame, avg_contours)
        cv.imshow('Final result', result)

        if cv.waitKey(33) == 27:
            break
    cv.destroyAllWindows()

    while True:
        _, frame = webcam.read()
        mask = fg.apply_edge(frame, edge)
        contours = fg.get_contours(mask)

        if len(avg_contours) >= contour_num:
            avg_contours = avg_contours[1:]
        avg_contours.append(max(contours, key=cv.contourArea))
        contours = avg_contours

        result = fg.layer_bg(frame, cv.imread('test_images/bg_test.png'), contours)
        cv.imshow('Final result', result)

        if cv.waitKey(33) == 27:
            break
    cv.destroyAllWindows()


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

        print("\nPress ESC to quit.")
        start(webcam)

if __name__ == '__main__':
    main()
