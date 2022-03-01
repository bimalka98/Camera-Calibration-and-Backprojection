###################################################################################
#                                                                                 #
#                 Real World Coordinate from Image Coordinate Using               #
#                 Single Calibrated Camera Based on Analytic Geometry             #
#                                                                                 #
###################################################################################   

# Joko Siswantoro 1,2, Anton Satria Prabuwono 1, and Azizi Abdullah 1
#   
# 1 Center For Artificial Intelligence Technology, Faculty of Information Science and
#   Technology, Universiti Kebangsaan Malaysia, 43600 UKM, Bangi, Selangor D.E., Malaysia
#   
# 2 Department of Mathematics and Sciences, Universitas Surabaya,
#   Jl. Kali Rungkut Tengilis, Surabaya, 60293, Indonesia

import  yaml
import numpy as np
import cv2 as cv

# ---------------------------------------------------------------------------------
# Step 1. Perform camera calibration to obtain extrinsic camera parameters R, T and
# intrinsic camera parameters fx, fy, cx, cy (done in calibrateCamera.py)

# get the camera matrix from the yaml file
with open('./LogitechC310.yaml', 'r') as stream:
    try:
        calib_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# extract camera matrix and distortion coefficients from yaaml file
camera_matrix = np.array(calib_params['mtx']).reshape(3,3)

# calculates mean of the focal lengths (in pixels)
fx = camera_matrix[0,0]
fy = camera_matrix[1,1]
mean_focul_length = (fx + fy) / 2

# Focul length in mm as specified in the product technical specification
focul_length_in_mm = 4.4

# Calculate pixles per mm
pixles_per_mm = round(mean_focul_length / focul_length_in_mm)
print('Pixles per mm: ', pixles_per_mm)

# Assume pixels per mm is the same for x and y 
sx = sy = pixles_per_mm

# principal point
cx = camera_matrix[0,2]
cy = camera_matrix[1,2]

# ---------------------------------------------------------------------------------
# Step 2. Find the coordinate of point p (xim, yim) in image coordinate system.
# done in object detection part; use dummy points for now.

# get set of dummy points
# image_points = np.array([[ 173.54767, 91.62902 ],
# [ 210.7686, 92.32755 ],
# [ 247.47551, 92.77607 ],
# [ 284.47098, 93.51474 ],
# [ 321.1669, 94.06741 ],
# [ 357.76126, 95.03036 ],
# [ 395.10233, 95.69413 ],
# [ 431.89203, 96.42651 ],
# [ 469.4813, 97.2708 ]])

image_points = np.array([[ 171.63728, 127.19049 ],
[ 209.06671, 127.80512 ],
[ 246.2503, 128.5212 ],
[ 283.181, 128.65028 ],
[ 320.31326, 129.6341 ],
[ 357.05832, 130.68134 ],
[ 394.54123, 131.55125 ],
[ 432.02014, 132.50407 ],
[ 469.7123, 133.17534 ]])

# convert the image points to homogeneous coordinates
image_points_hom = np.concatenate((image_points, np.ones((image_points.shape[0], 1))), axis=1)
print("Homogeneous image points: \n", image_points_hom)

# ---------------------------------------------------------------------------------
# Step 3. Find the coordinate of projection center Oc in real world coordinate 
# system using Eq. (3).

## get the rotation and translation vectors corresponding to the static camera field of view
rotation_vector = np.array([2.10602313, 2.15303455, -0.19642816]).reshape(3,1)
translation_vector = np.array([-122.22738712, -117.38511046, 656.31453705]).reshape(3,1)

# finding the camera centre Cc in real world coordinate system.
## get the rotation matrix from rotation vector
rotation_matrix, _ = cv.Rodrigues(rotation_vector)

## camera centre C = -R^(-1).t
C = - np.linalg.inv(rotation_matrix) @ translation_vector
print("Camera Centre in world coordinate: \n", C)


for point in image_points_hom:
    print('-'*50)
    print("Image point: ", point)

    # ---------------------------------------------------------------------------------
    # Step 4. Find the coordinate of p (ximw, yimw, zimw) in real world 
    # coordinate system using Eq. (7)

    # from eq. 4, 5, 6
    x_imc = (point[0] - cx)/sx
    y_imc = (point[1] - cy)/sy
    z_imc = 1* focul_length_in_mm
    
    point_in_camera_coordinate = np.array([x_imc, y_imc, z_imc]).reshape(3,1)
    # print("Point in camera coordinate: \n", point_in_camera_coordinate)

    # from eq. 7
    point_in_world_coordinate = np.linalg.inv(rotation_matrix) @ (point_in_camera_coordinate - translation_vector)
    # print("Point in world coordinate: \n", point_in_world_coordinate)

    # equation of the plane where the point lies in real world coordinate system
    # equa 10: Z = 0 plane. store it in an array in standard form ax+by+cz = d
    plane_equation = np.array([0, 0, 1, 0]) # a, b, c, d
    
    # calculate the parameter t using eq. 11 
    t = (plane_equation[-1] - np.dot(plane_equation[0:3], C)) / np.dot(plane_equation[0:3], (point_in_world_coordinate - C))
    # print("t: ", t)

    # ---------------------------------------------------------------------------------
    # Step 5. Approximate the coordinate of P in real world coordinate system using Eq.
    # (12), (13), and (14).

    # from eq. 12, 13, 14
    approximated_world_coord = C + t * (point_in_world_coordinate - C)
    print("Approx: world coord: ", np.round(approximated_world_coord.reshape(3,), decimals=2))
