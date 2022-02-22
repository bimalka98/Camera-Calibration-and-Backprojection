import  yaml
import numpy as np

# calibration = { 'ret': ret, 
#                 'mtx': mtx.tolist(), 
#                 'dist': dist.tolist(), 
with open('./LogitechC310_static_checkerboard.yaml', 'r') as stream:
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
# print('Pixles per mm: ', pixles_per_mm)

# Assume pixels per mm is the same for x and y 
mx = pixles_per_mm
my = pixles_per_mm
sacling_matrix = np.array([[mx, 0, 0], [0, my, 0], [0, 0, 1]])

# Calculate the new camera matrix in mm
new_camera_matrix = np.linalg.inv(sacling_matrix) @ camera_matrix
print('New camera matrix: \n', new_camera_matrix)

# sample image points in the range of (0,0) to (639, 479)
img_points = np.array([[256,256], [300, 300],[150, 200], [50, 450]])

# get homogeneous coordinates
homogeneous_points = np.ones((4,3))
homogeneous_points[:,:-1] = img_points
print('Homogeneous points: \n', homogeneous_points)

# multiply the homogeneous coordinates by the scaling factor Z (of world coordinates)
Z = 500 # mm
homogeneous_points = homogeneous_points* Z

# convert homogeneous coordinates to world coordinates
world_points = np.linalg.inv(new_camera_matrix) @ homogeneous_points.T
print('World points: \n', world_points.T/1000)