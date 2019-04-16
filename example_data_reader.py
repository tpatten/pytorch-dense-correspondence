from PIL import Image
import numpy as np
import math
import yaml
from yaml import CLoader

""" SET DATA PATH AND FILE NAME """
dataset_path = '/home/tpatten/Data/pdc/logs_proto/2018-04-16-14-25-19/processed/'
index = '000008'
""" --- """

def homogenous_transform_from_dict(d):
    pos = [0]*3
    pos[0] = d['translation']['x']
    pos[1] = d['translation']['y']
    pos[2] = d['translation']['z']

    quat = [0]*4
    quat[0] = d['quaternion']['w']
    quat[1] = d['quaternion']['x']
    quat[2] = d['quaternion']['y']
    quat[3] = d['quaternion']['z']

    transform_matrix = quaternion_matrix(quat)
    transform_matrix[0:3,3] = np.array(pos)

    return transform_matrix

def quaternion_matrix(quaternion):
    q = np.array(quaternion, dtype=np.float64, copy=True)
    n = np.dot(q, q)
    _EPS = np.finfo(float).eps * 4.0
    if n < _EPS:
        return np.identity(4)
    q *= math.sqrt(2.0 / n)
    q = np.outer(q, q)
    return np.array([
        [1.0-q[2, 2]-q[3, 3],     q[1, 2]-q[3, 0],     q[1, 3]+q[2, 0], 0.0],
        [    q[1, 2]+q[3, 0], 1.0-q[1, 1]-q[3, 3],     q[2, 3]-q[1, 0], 0.0],
        [    q[1, 3]-q[2, 0],     q[2, 3]+q[1, 0], 1.0-q[1, 1]-q[2, 2], 0.0],
        [                0.0,                 0.0,                 0.0, 1.0]])

def main():
    rgb_filename = dataset_path + 'images/' + index + '_rgb.png'
    rgb = Image.open(rgb_filename).convert('RGB')
    rgb_numpy = np.asarray(rgb)
    print "RGB image"
    print 'Type:', type(rgb_numpy)
    print 'Shape:', rgb_numpy.shape
    print 'Dtype:', rgb_numpy.dtype
    print 'Range:', rgb_numpy.flatten().min(0), rgb_numpy.flatten().max(0), '\n'

    depth_filename = dataset_path + 'rendered_images/' + index + '_depth.png'
    dep = Image.open(depth_filename)
    dep_numpy = np.asarray(dep)
    print "DEPTH image"
    print 'Type:', type(dep_numpy)
    print 'Shape:', dep_numpy.shape
    print 'Dtype:', dep_numpy.dtype
    print 'Range:', dep_numpy.flatten().min(0), dep_numpy.flatten().max(0), '\n'

    mask_filename = dataset_path + 'image_masks/' + index + '_mask.png'
    mask = Image.open(mask_filename)
    mask_numpy = np.asarray(mask)
    print "MASK image"
    print 'Type:', type(mask_numpy)
    print 'Shape:', mask_numpy.shape
    print 'Dtype:', mask_numpy.dtype
    print 'Range:', mask_numpy.flatten().min(0), mask_numpy.flatten().max(0), '\n'

    pose_data_filename = dataset_path + 'images/pose_data.yaml'
    pose_data = yaml.load(file(pose_data_filename), Loader=CLoader)
    pose_data = pose_data[int(index)]['camera_to_world']
    print "POSE data"
    print pose_data, '\n'
    transform = homogenous_transform_from_dict(pose_data)
    print "TRANSFORM"
    print transform, '\n'
    

if __name__== "__main__":
  main()
