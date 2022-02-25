#################################################################
#                                                               #
#            Image plane to Real World mapping                  #
#                                                               #
#################################################################
import  yaml
import numpy as np
import cv2 as cv

# get the camera matrix from the yaml file
with open('./LogitechC310.yaml', 'r') as stream:
    try:
        calib_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# read the image
img = cv.imread("./raw_images/image36.jpg")
h,  w = img.shape[:2]

# extract camera matrix and distortion coefficients from yaaml file
mtx = np.array(calib_params['mtx']).reshape(3,3)
dist = np.array(calib_params['dist']).reshape(1,5)

# get the new camera matrix 
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort the image
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# Convert to grayscale
gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

# Find the chess board corners
PatternSize = (9,7)
WindowSize = (5,5) # Half of the side length of the search window for cornerSubPix()
TerminationCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001) # termination criteria for cornerSubPix()
ret, corners = cv.findChessboardCorners(gray, PatternSize, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

assert ret == True

# refining pixel coordinates for given 2d points.
corners2 = cv.cornerSubPix(gray, corners, WindowSize, (-1,-1), TerminationCriteria)

# Draw and display the corners
img = cv.drawChessboardCorners(img, PatternSize, corners2, ret)   
# cv.imshow('Image', img)
# cv.waitKey(0)

# read the _3Dto2Dtransformation from the yaml file
with open('./transformations_image36.yaml', 'r') as stream2:
    try:
        transform_params = yaml.safe_load(stream2)
    except yaml.YAMLError as exc:
        print(exc)

_3Dto2Dtransformation = np.array(transform_params['_3Dto2Dtransformation']).reshape(3,4)

# get the shape of _3Dto2Dtransformation
print("_3Dto2Dtransformation shape: ", _3Dto2Dtransformation.shape)

matrix2 = _3Dto2Dtransformation.T @ _3Dto2Dtransformation
print("matrix2: \n", matrix2)

# get the inverse of the matrix2
alpha = 5e-5
matrix2_inv = np.linalg.inv(matrix2)

## scale 
scale_lambda = 656.31453705


for i in range(8):
    homogeneous_image_coord = np.array([corners2[i][0][0], corners2[i][0][1], 1])
    print("Homogeneous Image Coord: \n", homogeneous_image_coord)

    # multiply with the scaling factor lambda
    homogeneous_image_coord = homogeneous_image_coord*scale_lambda

    # multiply with the transpose of the transformation matrix
    matrix1 = _3Dto2Dtransformation.T @ homogeneous_image_coord

    # multiply with the inverse of matrix 2
    homogeneous_real_coord = matrix2_inv @ matrix1

    # print the real world coordinates
    print("Real World Coordinates: ", homogeneous_real_coord)