import  yaml
import numpy as np
import cv2 as cv

# get the camera matrix from the yaml file
with open('./LogitechC310.yaml', 'r') as stream:
    try:
        calib_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

camera_matrix = np.array(calib_params['mtx']).reshape(3,3)

## add column of zeros to the camera matrix
camera_matrix = np.concatenate((camera_matrix, np.zeros((3,1))), axis=1)
print("Camera Matrix: \n", camera_matrix)

## get the rotation and translation vectors corresponding to the static camera field of view
rotation_vector = np.array([2.10602313, 2.15303455, -0.19642816])
translation_vector = np.array([-122.22738712, -117.38511046, 656.31453705]).T

## get rotation matrix from rotation vector
rotation_matrix, _ = cv.Rodrigues(rotation_vector)

## get the 4x4 homogeneous transformation matrix (translate and rotate)
transformation_matrix = np.zeros((4,4))
transformation_matrix[:3,:3] = rotation_matrix
transformation_matrix[:3,3] = translation_vector
transformation_matrix[3,3] = 1
print("Transformation Matrix: \n", transformation_matrix)


## multiply the camera matrix with the transformation matrix to get the complete
## transformation matrix from real world to image plane

_3Dto2Dtransformation =  camera_matrix @ transformation_matrix

#################################################################
#                                                               #
#            Real world to Image plane mapping                  #
#                                                               #
#################################################################

RealWorldPoints = np.array([[0,0,0], [0,1,0], [0,2,0], [0,3,0]]) *30 # 30mm is the distance between the chessboard corners

# convert into homogeneous coordinates
RealWorldPoints = np.concatenate((RealWorldPoints, np.ones((RealWorldPoints.shape[0], 1))), axis=1)
print("Real World Points: \n", RealWorldPoints)

scale_lambda = 0
# Transform the real world points to image plane
for point in RealWorldPoints:
    imagepoint = _3Dto2Dtransformation @ point.T # [lambda*x, lambda*y, lambda]
    print("Lambda: ", imagepoint[-1]); scale_lambda = imagepoint[-1]
    imagepoint = imagepoint/imagepoint[-1]  # devide by lambda to get the image plane coords
    print(imagepoint)

# Target image plane coords to compare with the output of the above code
# [ 173.54767, 91.62902 ]
# [ 210.7686, 92.32755 ]
# [ 247.47551, 92.77607 ]
# [ 284.47098, 93.51474 ]

# save transformation matrix and other useful vectors to a yaml file
data = {'rotation_vector': rotation_vector.tolist(), 
        'translation_vector':translation_vector.tolist(),  
        'transformation_matrix': transformation_matrix.tolist(),
        '_3Dto2Dtransformation': _3Dto2Dtransformation.tolist()}

with open('./transformations_image36.yaml', 'w') as outfile:
    yaml.dump(data, outfile)