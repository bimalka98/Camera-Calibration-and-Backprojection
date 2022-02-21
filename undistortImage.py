"""
Created on Mon Feb 21 10:08:05 2022

@author: Bimalka Piyaruwan
@script: undistortImage.py
@description: This script captures images from the camera and saves them in the specified directory.
@sources: 
    https://github.com/smidm/video2calibration/blob/master/undistort.py
    
"""
# Importing the required libraries
import cv2 as cv
import numpy as np
import glob
import  yaml


# calibration = {   'ret': ret, 
#                   'mtx': mtx.tolist(), 
#                   'dist': dist.tolist(), 

with open('./LogitechC310.yaml', 'r') as stream:
    try:
        calib_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# path to distorted images
images = glob.glob('./images/*.jpg')
ImageCount = 0

for fname in images:
    # read the image
    img = cv.imread(fname)
    h,  w = img.shape[:2]

    # extract camera matrix and distortion coefficients from yaaml file
    mtx = np.array(calib_params['mtx']).reshape(3,3)
    dist = np.array(calib_params['dist']).reshape(1,5)

    # get the new camera matrix 
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    # undistort the image
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    
    # crop the image depending on the region of interest
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    # save the image
    cv.imwrite('./undistorted_images/' + 'image'+ str(ImageCount) +'.jpg', dst)

    # show the image
    cv.imshow('Undistorted Image' + str(ImageCount), dst)
    cv.waitKey(0)
    ImageCount += 1

# close all windows
cv.destroyAllWindows()  
