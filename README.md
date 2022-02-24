# [Camera Calibration using OpenCV](https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html)

***Text copied from OpenCV documentation***

*The important input data needed for calibration of the camera is the set of 3D real world points and the corresponding 2D coordinates of these points in the image.* 

1. 2D image points are OK which we can easily find from the image. These image points are locations where two black squares touch each other in chess boards.

2. What about the 3D points from real world space? Those images are taken from a static camera and chess boards are placed at different locations and orientations. So we need to know (X,Y,Z) values. **But for simplicity, we can say chess board was kept stationary at XY plane, (so Z=0 always) and camera was moved accordingly.** This consideration helps us to find only X,Y values. Now for X,Y values, we can simply pass the points as (0,0), (1,0), (2,0), ... which denotes the location of points. In this case, the results we get will be in the scale of size of chess board square. But if we know the square size, (say 30 mm), we can pass the values as (0,0), (30,0), (60,0), ... . Thus, we get the results in mm. (In this case, we don't know square size since we didn't take those images, so we pass in terms of square size).

*3D points are called **object points** and 2D image points are called **image points.***

### Note that in openCV [`cv.calibrateCamera()`](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#ga3207604e4b1a1758aa66acb6ed5aa65d) expects the real world coordinates of the checker board pattern intersect points with respect to a known coordinate system! They have generated those coordinates simply by a `np.mgrid()` using the number of intersecting points in horizontal and vertical direction in our checkerboard. This coordinate system must be considered when we map 2D image points from image to the real world and therefore shoul be a fixed one.

## *Note*
* **Image size:** 640 x 480 pixels<br>
* **Camera:** [Logitech C310 HD Webcam, 720p Video](https://support.logi.com/hc/en-us/articles/360023464573-Logitech-HD-Webcam-C310-Technical-Specifications)<br>
* **Square Size of Checkerboard:** 30 mm (*useful in camera calibration*)<br>
* **Lens and Sensor Type:**	Plastic, CMOS<br>
* **Focus Type:**	Fixed<br>
* **Field of View (FOV):**	60°<br>
* **Focal Length:**	4.4mm (*useful in 2D to 3D coordinate transformation*)<br>


## Calibration Parameters (Intrinsic parameters -> Common for all the images)
```
------------------------------------------------------------
Camera Matrix:
 [[806.14517655   0.         323.87146568]
 [  0.         811.24976479 236.50327395]
 [  0.           0.           1.        ]]
------------------------------------------------------------ 

Distortion Coefficients:
 [[-3.80673064e-02  1.00564222e+00 -1.28647942e-03  3.27139495e-03 -1.79549627e+00]] 
------------------------------------------------------------

Real world object points:

[[  0.   0.   0.]
 [  0.  30.   0.]
 [  0.  60.   0.]
 [  0.  90.   0.]
 [  0. 120.   0.]
 [  0. 150.   0.]
 [  0. 180.   0.]
 [  0. 210.   0.]
 [  0. 240.   0.]
 [ 30.   0.   0.]
 [ 30.  30.   0.]
 [ 30.  60.   0.]
 [ 30.  90.   0.]
 [ 30. 120.   0.]
 [ 30. 150.   0.]
 [ 30. 180.   0.]
 [ 30. 210.   0.]
 [ 30. 240.   0.]
 [ 60.   0.   0.]
 [ 60.  30.   0.]
 [ 60.  60.   0.]
 [ 60.  90.   0.]
 [ 60. 120.   0.]
 [ 60. 150.   0.]
 [ 60. 180.   0.]
 [ 60. 210.   0.]
 [ 60. 240.   0.]
 [ 90.   0.   0.]
 [ 90.  30.   0.]
 [ 90.  60.   0.]
 [ 90.  90.   0.]
 [ 90. 120.   0.]
 [ 90. 150.   0.]
 [ 90. 180.   0.]
 [ 90. 210.   0.]
 [ 90. 240.   0.]
 [120.   0.   0.]
 [120.  30.   0.]
 [120.  60.   0.]
 [120.  90.   0.]
 [120. 120.   0.]
 [120. 150.   0.]
 [120. 180.   0.]
 [120. 210.   0.]
 [120. 240.   0.]
 [150.   0.   0.]
 [150.  30.   0.]
 [150.  60.   0.]
 [150.  90.   0.]
 [150. 120.   0.]
 [150. 150.   0.]
 [150. 180.   0.]
 [150. 210.   0.]
 [150. 240.   0.]
 [180.   0.   0.]
 [180.  30.   0.]
 [180.  60.   0.]
 [180.  90.   0.]
 [180. 120.   0.]
 [180. 150.   0.]
 [180. 180.   0.]
 [180. 210.   0.]
 [180. 240.   0.]]

```


# Extrinsic Parameters of : `raw_images/image36.jpg` (Specific for an image )

|*raw image* | *processed image*|
|:----:|:----:|
|<img src="raw_images/image36.jpg" width="500" />| <img src="processed_images/image26.jpg" width="500" /> |

```

Translational Vector: 
 [-122.22738712] [-117.38511046] [656.31453705]
------------------------------------------------------------

Rotational Vector:    
 [2.10602313] [2.15303455] [-0.19642816]
------------------------------------------------------------

Image Points:
[[ 173.54767, 91.62902 ]
[ 210.7686, 92.32755 ]
[ 247.47551, 92.77607 ]
[ 284.47098, 93.51474 ]
[ 321.1669, 94.06741 ]
[ 357.76126, 95.03036 ]
[ 395.10233, 95.69413 ]
[ 431.89203, 96.42651 ]
[ 469.4813, 97.2708 ]
[ 171.63728, 127.19049 ]
[ 209.06671, 127.80512 ]
[ 246.2503, 128.5212 ]
[ 283.181, 128.65028 ]
[ 320.31326, 129.6341 ]
[ 357.05832, 130.68134 ]
[ 394.54123, 131.55125 ]
[ 432.02014, 132.50407 ]
[ 469.7123, 133.17534 ]
[ 169.62589, 163.48984 ]
[ 207.46173, 164.22824 ]
[ 244.51976, 164.52423 ]
[ 281.93274, 164.9935 ]
[ 319.34958, 166.34975 ]
[ 356.41205, 167.28563 ]
[ 394.31174, 168.02405 ]
[ 431.93896, 168.6989 ]
[ 470.23483, 169.49594 ]
[ 167.73346, 200.23148 ]
[ 205.58194, 200.75142 ]
[ 243.1283, 201.36891 ]
[ 280.80374, 201.77411 ]
[ 318.48804, 203.30768 ]
[ 355.8776, 204.15332 ]
[ 393.94986, 204.82649 ]
[ 432.0001, 205.57896 ]
[ 470.39276, 206.30649 ]
[ 165.46951, 237.35175 ]
[ 203.698, 238.09941 ]
[ 241.50809, 238.54573 ]
[ 279.67838, 239.42378 ]
[ 317.6305, 240.6864 ]
[ 355.47403, 241.80818 ]
[ 393.743, 242.63362 ]
[ 432.0229, 243.2718 ]
[ 470.79486, 243.9435 ]
[ 163.45647, 275.31726 ]
[ 201.74608, 276.00104 ]
[ 240.13731, 276.88266 ]
[ 278.50775, 277.63733 ]
[ 316.65363, 278.87833 ]
[ 355.05225, 279.8575 ]
[ 393.56052, 280.53806 ]
[ 432.25452, 281.38232 ]
[ 471.35577, 281.9048 ]
[ 161.2164, 313.73767 ]
[ 200.229, 314.60574 ]
[ 238.31091, 315.55875 ]
[ 277.1585, 316.4851 ]
[ 315.9854, 317.74756 ]
[ 354.43387, 318.6201 ]
[ 393.47363, 319.52905 ]
[ 432.31772, 320.20914 ]
[ 471.76373, 320.8632 ]
]

```

**Output vector of rotation vectors ([Rodrigues](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#ga61585db663d9da06b68e70cfbf6a1eac) ) estimated for each pattern view 
(e.g. std::vector<cv::Mat>>). That is, each i-th rotation vector together with 
the corresponding i-th translation vector, 
brings the calibration pattern from the object coordinate space 
(in which object points are specified)  to the camera coordinate space.
In more technical terms, the tuple of the i-th rotation and translation vector 
performs a change of basis from object coordinate space to camera coordinate space.
Due to its duality, this tuple is equivalent to the position of the calibration 
pattern with respect to the camera coordinate space.**
