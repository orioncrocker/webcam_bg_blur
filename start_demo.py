###########################################################
# Author: Orion Crocker
# Filename: start_demo.py
# Date: 05/28/20
# 
# Demo
#   Presentation demo for CS 410/510 Computational
# Photography
###########################################################

import os, os.path
import cv2 as cv
import numpy as np
import foreground as fg


def display_hstack(comment, frame1, frame2):
  stack = np.hstack((frame1, frame2))
  cv.imshow(comment, stack)

def display_vstack(comment, frame1, frame2):
    stack = np.vstack((frame1, frame2))
    cv.imshow(comment, stack)

def start(vid, label, bg):
    edge = fg.get_edge(10, False, 100)
    stage = 0

    # frame count info
    frame_count = 1
    end_frame = vid.get(cv.CAP_PROP_FRAME_COUNT)

    # contour info
    contour_num = 3
    greatest = []

    while True:
        _, frame = vid.read()

        # reset video
        frame_count += 1
        if frame_count >= end_frame:
            vid.set(cv.CAP_PROP_POS_FRAMES, 0)
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
                mask = cv.blur(mask, (21,21))
                cv.drawContours(mask, greatest, 0, (0, 0, 0, 0), cv.FILLED)
                frame[np.where((mask != [0, 0, 0, 0]).all(axis=2))] = [0, 0, 0, 0]
            elif stage == 5:
                mask = fg.blur_bg(frame, greatest, 21)
                frame = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
            elif stage == 6:
                mask = fg.layer_bg(frame, bg, greatest)
                frame = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)

        if 0 <= stage < 4:
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2RGB)

        display_hstack(label + ' - stage: ' + str(stage), frame, mask)

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
        elif key == 32:
            while True:
                if cv.waitKey(33) == 32:
                    break

        if stage > 6:
            break
    cv.destroyAllWindows()


def main():
    if not fg.version_check:
        quit()
    print("\nPress ESC to quit.")

    # test background
    bg = cv.imread('bg/forest_path.jpg')

    _, _, test_vids = next(os.walk('test_videos'))
    for video in test_vids:
        video = 'test_videos/' + video
        start(cv.VideoCapture(video), '', bg)


if __name__ == '__main__':
    main()
