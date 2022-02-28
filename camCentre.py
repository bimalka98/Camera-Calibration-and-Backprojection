import  yaml
import numpy as np
import cv2 as cv

# read the _3Dto2Dtransformation from the yaml file
with open('./transformations_image36.yaml', 'r') as stream2:
    try:
        transform_params = yaml.safe_load(stream2)
    except yaml.YAMLError as exc:
        print(exc)

_3Dto2Dtransformation = np.array(transform_params['_3Dto2Dtransformation']).reshape(3,4)

## get the rotation and translation vectors corresponding to the static camera field of view
rotation_vector = np.array([2.10602313, 2.15303455, -0.19642816])
translation_vector = np.array([-122.22738712, -117.38511046, 656.31453705]).T

## P = K[R | t] (6.8) where from (6.7) t = −RC. 
## where C represents the coordinates of the camera centre in the world coordinate frame, 
## and R is a 3 × 3 rotation matrix representing the orientation of the camera coordinate frame

# findin the camera centre C

## get the rotation matrix from rotation vector
rotation_matrix, _ = cv.Rodrigues(rotation_vector)

## camera centre C = -R^(-1).t
C = - np.linalg.inv(rotation_matrix) @ translation_vector
print("Camera Centre in world coordinate: \n", C)


## We know two points on the ray. These are the camera centre C (where PC = 0)
## and the point P+x, where P+ is the pseudo-inverse of P. The pseudo-inverse of P is the
## matrix P+ = P.T(PP.T)−1, for which PP+ = I

## express caemra centre C as a homogeneous vector
C = np.concatenate((C.reshape(3,1), np.ones((1,1))), axis=0)
print("Camera Centre in homogeneous coordinates: \n", C)

## get the product PC to check if the camera centre C is correct
PC = _3Dto2Dtransformation @ C
print("Product PC: \n", np.round(PC, 3))