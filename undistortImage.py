"""
Created on Mon Feb 21 10:08:05 2022

@author: Bimalka Piyaruwan
@script: captureImages.py
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
#                   'ncm': new_camera_matrix.tolist(), 
#                   'roi': roi.tolist()}
with open('./LogitechC310.yaml', 'r') as stream:
    try:
        calib_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

images = glob.glob('./images/*.jpg')
ImageCount = 0

for fname in images:
    img = cv.imread(fname)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(np.array(calib_params['mtx']), np.array(calib_params['dist']), (w,h), 1, (w,h))
    dst = cv.undistort(img, calib_params['mtx'], calib_params['dist'], None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imshow('Undistorted Image', dst)
    cv.imwrite('./undistorted_images/' + 'image'+ str(ImageCount) +'.jpg', dst)
    ImageCount += 1
