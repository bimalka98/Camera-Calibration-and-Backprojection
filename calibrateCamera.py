# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 10:12:36 2022

@author: Bimalka Piyaruwan
@script: calibrateCamera.py
@description: This script calibrates the camera and saves the calibration parameters in the specified directory.
"""
# Importing the required libraries
import cv2 as cv
import numpy as np
import glob

# define Number of <<inner>> corners per a chessboard row and column
PatternSize = (9,7)
SquareSize = 30 # size of the PatternSize square in mm

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((PatternSize[0] * PatternSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:PatternSize[0], 0:PatternSize[1]].T.reshape(-1, 2)
objp = objp * SquareSize # multiply by 30mm to get the real world coordinates

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Extracting path of individual image stored in a given directory
images = glob.glob('./images/*.jpg')
ImageCount = 0

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv.findChessboardCorners(gray, PatternSize, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
    print(corners)

    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """

    if ret == True:
        print("Chessboard Detected")

        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv.cornerSubPix(gray, corners, (SquareSize//2, SquareSize//2), (-1,-1), criteria)
        
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv.drawChessboardCorners(img, PatternSize, corners2, ret)   
        cv.imshow('Image' + str(ImageCount),img)
        cv.waitKey(0)

    ImageCount+=1
cv.destroyAllWindows()

# Calibrating the camera

# height and width of the image
h,w = img.shape[:2]

"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
print('\nCalibrating...')
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1)
roi = np.array(roi).astype(int)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("new_camera_matrix : \n")
print(new_camera_matrix)