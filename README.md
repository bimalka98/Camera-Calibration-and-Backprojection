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

# View of the camera: `raw_images/image36.jpg`

|*raw image* | *processed image*|
|:----:|:----:|
|<img src="raw_images/image36.jpg" width="500" />| <img src="processed_images/image26.jpg" width="500" /> |

## Calibration Parameters
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

image36.jpg: 
Translational Vector: 
 [-122.22738712] [-117.38511046] [656.31453705]
------------------------------------------------------------

Rotational Vector:    
 [2.10602313] [2.15303455] [-0.19642816]
------------------------------------------------------------
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
