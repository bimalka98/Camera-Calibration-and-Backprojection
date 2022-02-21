
"""
Created on Mon Feb 21 10:08:05 2022

@author: Bimalka Piyaruwan
@script: captureImages.py
@description: This script captures images from the camera and saves them in the specified directory.
@sources: 
    https://github.com/kevinam99/capturing-images-from-webcam-using-opencv-python/blob/master/webcam-capture-v1.01.py
    
"""
# Importing the required libraries
import cv2 as cv

# Initialize the usb camera
camera = cv.VideoCapture(1)

# Define the directory where the images will be saved
directory = "./images/"

# number of the image
image_number = 0

# capture the images
while True:
    # Capture the frame
    ret, frame = camera.read()
    # Display the frame
    cv.imshow('frame', frame)
    
    key = cv.waitKey(1)
    # Press 's' to save the image
    if key == ord('s'):
        # Save the image
        cv.imwrite(directory + 'image'+ str(image_number) +'.jpg', frame)
        print("Image {} saved".format(image_number))
        image_number += 1
    # Press 'q' to quit
    elif key == ord('q'):
        print("Released the camera")
        break
