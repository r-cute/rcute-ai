import cv2
from cv2 import aruco
import numpy as np

class ArUcoDetector:

    def __init__(self, dictionary=aruco.DICT_4X4_50):
        """ArUco marker detector"""
        self.aruco_dict = aruco.Dictionary_get(dictionary)
        self.parameters = aruco.DetectorParameters_create()

    def center(self, points):
        """return center point (x, y) of the 4 corners of a detected marker"""
        return tuple(np.average(points.reshape((4,-1)), axis=0))

    def detect(self, img, *, annotate=False):
        """return the first 2 elements from cv2.aruco.detectMarkers(img)"""
        # mean_c =  cv2.adaptiveThreshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,65,2)
        r= aruco.detectMarkers(img, self.aruco_dict, parameters=self.parameters)[:2]
        annotate and self.annotate(img, *r)
        return r

    def annotate(self, img, corners, ids):
        """draw detected markers on img"""
        aruco.drawDetectedMarkers(img, corners, ids)