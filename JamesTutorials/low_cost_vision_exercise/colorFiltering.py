import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import random 
import math


#This method used belows presents the colored object surrounded by a black background 
# The other method (in code_example.py) presents the image as a distored color based on the hsv image

blue = np.uint8([[[160,60,0]]])
brown = np.uint8([[[80,123,155]]])
# Red isn't quite working atm
red = np.uint8([[[21,36,102]]])
green = np.uint8([[[3,197,148]]])

def filterOutColoredObjects(img_bgr, colorArray, show = False):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

     # define range of color in HSV
    hsvColor = cv2.cvtColor(colorArray,cv2.COLOR_BGR2HSV)
    hsvColorValue = hsvColor[0][0][0]
    lower = np.array([hsvColorValue - 10,100,100])
    upper = np.array([hsvColorValue + 10,255,255])
    # Threshold the HSV image to get only that color
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img_bgr,img_bgr, mask = mask)

    if(show):
        cv2.imshow('img_bgr',img_bgr)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Invert the mask to be used for contouring
    mask_inv = 255 - mask

    return mask_inv