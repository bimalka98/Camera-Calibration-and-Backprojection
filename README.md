# [Camera Calibration using OpenCV](https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html)

***Text copied from OpenCV documentation***

*The important input data needed for calibration of the camera is the set of 3D real world points and the corresponding 2D coordinates of these points in the image.* 

1. 2D image points are OK which we can easily find from the image. These image points are locations where two black squares touch each other in chess boards.

2. What about the 3D points from real world space? Those images are taken from a static camera and chess boards are placed at different locations and orientations. So we need to know (X,Y,Z) values. **But for simplicity, we can say chess board was kept stationary at XY plane, (so Z=0 always) and camera was moved accordingly.** This consideration helps us to find only X,Y values. Now for X,Y values, we can simply pass the points as (0,0), (1,0), (2,0), ... which denotes the location of points. In this case, the results we get will be in the scale of size of chess board square. But if we know the square size, (say 30 mm), we can pass the values as (0,0), (30,0), (60,0), ... . Thus, we get the results in mm. (In this case, we don't know square size since we didn't take those images, so we pass in terms of square size).

*3D points are called **object points** and 2D image points are called **image points.***

### Note that in openCV `cv.calibrateCamera()` expects the real world coordinates of the checker board pattern intersect points with respect to a known coordinate system! They have generated those coordinates simply by a `np.mgrid()` using the number of intersecting points in horizontal and vertical direction in our checkerboard. This coordinate system must be considered when we map 2D image points from image to the real world and therefore shoul be a fixed one.

## *Note*
* **Image size:** 640 x 480 pixels<br>
* **Camera:** [Logitech C310 HD Webcam, 720p Video](https://support.logi.com/hc/en-us/articles/360023464573-Logitech-HD-Webcam-C310-Technical-Specifications)<br>
* **Square Size of Checkerboard:** 30 mm (*useful in camera calibration*)<br>
* **Lens and Sensor Type:**	Plastic, CMOS<br>
* **Focus Type:**	Fixed<br>
* **Field of View (FOV):**	60°<br>
* **Focal Length:**	4.4mm (*useful in 2D to 3D coordinate transformation*)<br>

## Calibration Parameters
```
Camera Matrix:
 [[806.14517655   0.         323.87146568]
 [  0.         811.24976479 236.50327395]
 [  0.           0.           1.        ]]
------------------------------------------------------------ 

Distortion Coefficients:
 [[-3.80673064e-02  1.00564222e+00 -1.28647942e-03  3.27139495e-03 -1.79549627e+00]]
 
```
