import  yaml
import numpy as np
import cv2 as cv


with open('./LogitechC310.yaml', 'r') as stream:
    try:
        calib_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# get the camera matrix
camera_matrix = np.array(calib_params['mtx']).reshape(3,3)
print("Camera Matrix: \n", camera_matrix)

## get the rotation and translation vectors
rotation_vector = np.array([2.10602313, 2.15303455, -0.19642816])
translation_vector = np.array([-122.22738712, -117.38511046, 656.31453705]).T

## get rotation matrix from rotation vector
rotation_matrix, _ = cv.Rodrigues(rotation_vector)

## get the 4x4 homogeneous transformation matrix
transformation_matrix = np.zeros((4,4))
transformation_matrix[:3,:3] = rotation_matrix
transformation_matrix[:3,3] = translation_vector
transformation_matrix[3,3] = 1
print("Transformation Matrix: \n", transformation_matrix)


# calculates mean of the focal lengths
mean_focul_length = (camera_matrix[0,0] + camera_matrix[1,1]) / 2

# Focul length in mm as specified in the product technical specification
focul_length_in_mm = 4.4

# Calculate pixles per mm
pixles_per_mm = mean_focul_length / focul_length_in_mm

# Assume pixels per mm is the same for x and y 
mx = pixles_per_mm
my = pixles_per_mm
sacling_matrix = np.array([[mx, 0, 0], [0, my, 0], [0, 0, 1]])
