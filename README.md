# webcam_bg_blur
Provide an extra layer of privacy to your webcam feed

CS410/510 Computational Photography, Portland State University

## Covid-19 related privacy concerns
If you've attended a Zoom, Discord video chat, or Google Hangouts meeting during the 2020 Pandemic, chances are you have gotten a peek into someone else's home. webcam_bg_blur is my response to this benign invasion of privacy, as well as a good excuse to learn a bit about OpenCV.

While there are other solutions to this problem (such as Zoom's background replacement tool), I've found that they are distracting and look unprofessional. Instead of overlaying another image on the background, webcam_bg_blur will blur any part of the image not in the foreground, adding an extra layer of privacy to your webcam feed while still looking professional in your own home.

## How it works
OpenCV's built in KNN algorithm detects movement, in this case the parameters of this examples are
 
 ```
dist2Threshold = 10
history = 100
detectShadows = False
 ```

[!KNN[Duncan Trussel](examples/duncan_knn.png)](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_knn.png)

From this blob of motion detection, OpenCV can create contours. In this case, the contour that appears over the frame are the largest contours available, as sorted by `(max(contours, key=cv.contourArea)`.

[!Contours[Duncan Trussel](examples/duncan_filled_contour.png)](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_filled_contour.png)

The frame is copied and blurred before both images are converted to RGBA color space. All pixels within contour mask on the background image are replaced with pixel value `[0,0,0,0]`. For every pixel that is not `[0,0,0,0]` in the original image, set the pixel value to `[0,0,0,0]`.

[!Transparent[Duncan Trussel](examples/duncan_transparent.png)](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_transparent.png)

Then the two images are simply added together to combine their pixel values into one image.

[!Result[Duncan Trussel](examples/duncan_result.png)](https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/duncan_result.png)

## Test it out for yourself
`python3 start.py`

## View examples from clips
`python3 demo.py`

## Problems / Future Work
As of turning in this assignment, the program fully relies on the KNN algorithm to detect motion. This means that the camera itself must be relatively steady in order to achieve satisfactory results. Perhaps a motion stability algorithm could be used to counteract this, but I'm not sure that it's worth it.

This is an example of a video that looks relatively stable, but is probably shot from a camera a great distance away and is zooming in. The micro-movements of the camera itself create a lot of noise for KNN to have to deal with.

[!Problem[Donald Trump](examples/donald_movement.png)(https://github.com/orioncrocker/webcam_bg_blur/blob/master/examples/donald_movement.png)]