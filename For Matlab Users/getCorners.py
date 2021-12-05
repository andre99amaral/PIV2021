"""
This script receives an image as input and outputs a .mat file with the Aruco markers' coordinates (in pixels)
and ids. The order of the coordinates is the same as the order of the ids. Example: if ids[0] has value 2 then
corners[0] has corners of Aruco marker with id=2.
"""

import sys
import numpy as np
import cv2
from cv2 import aruco as aruco
from scipy.io import savemat
import argparse

def initArucoPos(template, aruco_dict, arucoParameters):
    """
    Returns the corners of the Aruco markers in the template image. Note that the corners sequence is the same as
    the ids sequence. Example: if ids[0] has value 2 then corners[0] has corners of Aruco marker with id=2.

    :param template: template image
    :param aruco_dict: dictionary of Aruco codes used in the template image
    """
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray_template, aruco_dict, parameters=arucoParameters)

    if len(corners) == 0:
        print("Could not detect Aruco markers. Exiting.")
        exit(0)

    print("Detected {} Aruco markers.".format(np.size(corners,0)))

    return corners, ids


def run(img_path):
    
    img_template = cv2.imread(img_path)
    if img_template is None:
        print("Unable to read the template.")
        exit(-1)

    #The arucos in the template must be the ones in this dictionary
    dict4_7by7 = aruco.getPredefinedDictionary(aruco.DICT_7X7_50)

    arucoParameters = aruco.DetectorParameters_create()
    corners, ids = initArucoPos(img_template, dict4_7by7, arucoParameters)

    dict = {"corners": corners, "ids": ids}
    #savemat("cornersIds.mat", dict)
    return dict
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Receives an image with some Aruco markers and outputs their \
                                                  coordinates and ids.')
    parser.add_argument('img', metavar='image_path',
                        help='Path to image, with extension (.png, .jpg, ...)')

    args = parser.parse_args()
    return run(args.img)
