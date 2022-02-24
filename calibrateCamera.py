# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 15:31:40 SLST 2022

@author: Bimalka Piyaruwan
@script: calibrateCamera.py
@description: This script calibrates the camera and saves the calibration parameters in the specified directory.
"""

# Importing the required libraries
import cv2 as cv
import numpy as np
import glob
import yaml

# define Number of <<inner>> corners per a chessboard row and column
PatternSize = (9,7)
SquareSize = 30 # size of the PatternSize square in mm

# termination criteria
TerminationCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
ObjectPoints = np.zeros((PatternSize[0] * PatternSize[1], 3), np.float32)
ObjectPoints[:,:2] = np.mgrid[0:PatternSize[0], 0:PatternSize[1]].T.reshape(-1, 2)
ObjectPoints = ObjectPoints * SquareSize # multiply by 30mm to get the real world coordinates
#print(ObjectPoints)

# Arrays to store object points and image points from all the images.
RealPoints = []  # 3d point in real world space
ImagePoints = [] # 2d points in image plane.

# Extracting path of individual image stored in a given directory
Images = glob.glob('./raw_images/*.jpg')

ImageCount = int(Images[0][-5])
WindowSize = (5,5) # Half of the side length of the search window for cornerSubPix()

for _filename in Images:

    # Read the image
    img = cv.imread(_filename)
    print("Reading image " + _filename)

    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, PatternSize, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
    
    # If desired number of corners are found in the image then ret = true
    if ret == True:
        print("Corners found in image " + _filename)

        # Append real world object points to the array
        RealPoints.append(ObjectPoints)

        # refining pixel coordinates for given 2d points.
        corners2 = cv.cornerSubPix(gray, corners, WindowSize, (-1,-1), TerminationCriteria)

        # Append image points to the array
        ImagePoints.append(corners2)

        # Draw and display the corners
        img = cv.drawChessboardCorners(img, PatternSize, corners2, ret)   
        cv.imshow('Image' + str(ImageCount),img)
        cv.waitKey(0)

         # save the processed image
        cv.imwrite('./processed_images/' + 'image'+ str(ImageCount) +'.jpg', img)
    
    else:
        print("No Chessboard Detected in" + _filename)
    
    ImageCount+=1
    print("-"*50)

cv.destroyAllWindows()

# camera calibration

