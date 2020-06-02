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
  mask = cv.blur(mask, (27,27))
  cv.drawContours(mask, contours, 0, (0, 0, 0), cv.FILLED)
  frame[np.where((mask != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
  return mask, frame


def display_hstack(comment, frame1, frame2):
  stack = np.hstack((frame1, frame2))
  cv.imshow(comment, stack)

def start(vid1):
    edge = fg.get_edge(10, False, 100)
    stage = 0

    # frame count info
    frame_count = 1
    end_frame = vid1.get(cv.CAP_PROP_FRAME_COUNT)

    # contour info
    contour_num = 3
    greatest = []

    while True:
        _, frame = vid1.read()

        # reset video
        frame_count += 1
        if frame_count >= end_frame:
            vid1.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame_count = 1

        mask = fg.apply_edge(frame, edge)

        if stage >= 1:
            contours = fg.get_contours(mask)
            if len(greatest) == contour_num:
                greatest = greatest[1:]
            greatest.append(max(contours, key=cv.contourArea))

            if stage == 1:
                cv.drawContours(frame, contours, -1, (0,255,0), 5)
            elif stage == 2:
                cv.drawContours(frame, greatest, 0, (0, 255, 0), 5)
            elif stage == 3:
                cv.drawContours(frame, greatest, 0, (0, 255, 0), cv.FILLED)
            elif stage == 4:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
                mask = frame.copy()
                cv.drawContours(mask, greatest, 0, (0, 0, 0, 0), cv.FILLED)
                frame[np.where((mask != [0, 0, 0, 0]).all(axis=2))] = [0, 0, 0, 0]
            elif stage == 5:
                mask = fg.blur_bg(frame, greatest, 21)
                frame = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)

        if stage >= 0 and stage < 4:
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2RGB)
        display_hstack('demo: ' + str(stage), frame, mask)

        key = cv.waitKey(33)
        if key == 27:
            break
        elif key == 81:
            stage -= 1
            if stage < 0:
                stage = 0
            cv.destroyAllWindows()
        elif key == 83:
            stage += 1
            cv.destroyAllWindows()

        if stage > 5:
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
        vid1 = cv.VideoCapture('test_videos/duncan.mp4')
        vid2 = cv.VideoCapture('test_videos/joe.mp4')
        start(vid1)
        start(vid2)

if __name__ == '__main__':
    main()
