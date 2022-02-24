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

# preparing object points as follows: Z comes out from the plane of the chessboard
#  _ _ Y(9)
# |
# |
# X(7)
# (0,0,0), (0,1,0), (0,2,0) ....,(0,8,0)
# (1,0,0), (1,1,0), (1,2,0) ....,(1,8,0)
# (2,0,0), (2,1,0), (2,2,0) ....,(2,8,0)
# ....
# (6,0,0), (6,1,0), (6,2,0) ....,(6,8,0)

ObjectPoints = []
for x in range(PatternSize[1]):
    for y in range(PatternSize[0]):
        ObjectPoints.append([x * SquareSize, y * SquareSize, 0])
ObjectPoints = np.array(ObjectPoints, dtype=np.float32)
# print(ObjectPoints)
# breakpoint()

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
        # cv.imshow('Image' + str(ImageCount),img)
        # cv.waitKey(0)

         # save the processed image
        cv.imwrite('./processed_images/' + 'image'+ str(ImageCount) +'.jpg', img)
    
    else:
        print("No Chessboard Detected in" + _filename)
    
    ImageCount+=1
    print("-"*50)

cv.destroyAllWindows()

# ++++++++++++++Calibrating the camera++++++++++++++

# height and width of the image: (480, 640, 3)
h,w = img.shape[:2]

print('\nCalibrating...')
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(RealPoints, ImagePoints, gray.shape[::-1], None, None)
print("\nCalibration Successful!")

# Saving the calibration parameters in a yaml file
calibration = {'ret': ret, 'mtx': mtx.tolist(), 'dist': dist.tolist()}

with open('LogitechC310.yaml', 'w') as outfile:
        yaml.dump(calibration, outfile)

# print the camera calibration matrix and distortion coefficients
print("-"*60, "\nCamera Matrix: \n", mtx)
print("-"*60, "\nDistortion Coefficients: \n", dist)
