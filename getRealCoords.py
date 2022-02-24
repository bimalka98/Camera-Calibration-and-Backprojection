import  yaml
import numpy as np


with open('./LogitechC310.yaml', 'r') as stream:
    try:
        calib_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# get the camera matrix
camera_matrix = np.array(calib_params['mtx']).reshape(3,3)
print("Camera Matrix: \n", camera_matrix)

# calculates mean of the focal lengths
mean_focul_length = (camera_matrix[0,0] + camera_matrix[1,1]) / 2

# Focul length in mm as specified in the product technical specification
focul_length_in_mm = 4.4

# Calculate pixles per mm
pixles_per_mm = round(mean_focul_length / focul_length_in_mm)

# Assume pixels per mm is the same for x and y 
mx = pixles_per_mm
my = pixles_per_mm
sacling_matrix = np.array([[mx, 0, 0], [0, my, 0], [0, 0, 1]])
