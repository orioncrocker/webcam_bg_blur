# webcam_bg_blur
Provide an extra layer of privacy to your webcam feed

CS410/510 Computational Photography, Portland State University

## Covid-19 related privacy concerns
If you've attended a Zoom, Discord video chat, or Google Hangouts meeting during the 2020 Pandemic, chances are you have gotten a peek into someone else's home. webcam_bg_blur is my response to this benign invasion of privacy, as well as a good excuse to learn a bit about OpenCV.

While there are other solutions to this problem (such as Zoom's background replacement tool), I've found that they are distracting and look unprofessional. Instead of overlaying another image on the background, webcam_bg_blur will blur any part of the image not in the foreground, adding an extra layer of privacy to your webcam feed while still looking professional in your own home.

## How it works
OpenCV's built in KNN algorithm detects "movement" based on changes of pixel color and intensity from previously viewed frames. In this case, the parameters of this examples are
 
 ```
edge = cv.createBackgroundSubtractorKNN(history=100, dist2Threshold=10, detectShadows=False)
 ```

![KNN](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_knn.png)

From this blob of "motion detection," OpenCV can detect various shapes in the form of contours. In this case, the contour that appears in the frame is the largest contour available, as sorted by `cv.contourArea`.

![Contour](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_contour.png)

With the largest contour detected, it is filled in to whatever pixel value desired.

![Contours](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_filled_contour.png)

A copy of the frame is created and blurred (using fast box blur) before both images are converted to RGBA color space. All pixels within the largest contour mask on the blurred image are replaced with pixel value `[0,0,0,0]`. For every pixel that is not `[0,0,0,0]` in the original image, the pixel value is set to `[0,0,0,0]`.

![Transparent](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_transparent.png)

Then the two images are simply added together to combine their pixel values into one image.

![Result](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_result.png)

This technique can also be used to replace the background image with something else.

![Background Replaced](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_bg_replaced.png)

## Test it out for yourself using your webcam!
`python3 start_bg_blur.py`

## View examples from clips provided
`python3 start_demo.py`

Scroll through visual phases of algorithm using left or right arrow keys, ESC to quit.

## Problems / Future Work
As of turning in this assignment, the program fully relies on the KNN algorithm to detect motion. This means that the camera itself must be relatively steady in order to achieve satisfactory results. Perhaps a motion stability algorithm could be used to counteract this, but I'm not sure that it's worth it.

This is an example of a video that looks relatively stable, but is probably shot from a camera a great distance away and is zooming in. The micro-movements of the camera itself create a lot of noise for KNN to have to deal with.

![Problem](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/donald_movement.png)