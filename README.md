# [Camera Calibration using OpenCV](https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html)

*The important input data needed for calibration of the camera is the set of 3D real world points and the corresponding 2D coordinates of these points in the image.* 

1. 2D image points are OK which we can easily find from the image. (These image points are locations where two black squares touch each other in chess boards)

2. What about the 3D points from real world space? Those images are taken from a static camera and chess boards are placed at different locations and orientations. So we need to know (X,Y,Z) values. But for simplicity, we can say chess board was kept stationary at XY plane, (so Z=0 always) and camera was moved accordingly. This consideration helps us to find only X,Y values. Now for X,Y values, we can simply pass the points as (0,0), (1,0), (2,0), ... which denotes the location of points. In this case, the results we get will be in the scale of size of chess board square. But if we know the square size, (say 30 mm), we can pass the values as (0,0), (30,0), (60,0), ... . Thus, we get the results in mm. (In this case, we don't know square size since we didn't take those images, so we pass in terms of square size).

*3D points are called **object points** and 2D image points are called **image points.***

## Method 1: Static camera and chess boards are placed at different locations

```
Camera Matrix:
 [[824.56316122   0.         329.56730044]
 [  0.         823.63476754 260.06591151]
 [  0.           0.           1.        ]]

Distortion Coefficients:
 [[0.00785561 0.41494786 0.00960021 0.00577902 1.53307777]]
```
![](figures/srcimgs.png)

## Method 2: Chess board was kept stationary at XY plane, (so Z=0 always) and camera was moved accordingly
