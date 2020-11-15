import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import random 
import math


#This method used belows presents the colored object surrounded by a black background 
# The other method (in code_example.py) presents the image as a distored color based on the hsv image


def filterOutBlueObjects(img_bgr):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

     # define range of blue color in HSV
    blue = np.uint8([[[160,60,0]]])
    hsvBlue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)
    hsvBlueValue = hsvBlue[0][0][0]
    lower_blue = np.array([hsvBlueValue - 10,100,100])
    upper_blue = np.array([hsvBlueValue + 10,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img_bgr,img_bgr, mask= mask)

    cv2.imshow('img_bgr',img_bgr)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def filterOutBrownObjects(img_bgr):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

     # define range of color in HSV
    color = np.uint8([[[80,123,155]]])
    hsvColor = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
    hsvValue = hsvColor[0][0][0]
    lower = np.array([hsvValue - 10,100,100])
    upper = np.array([hsvValue + 10,255,255])
    # Threshold the HSV image to get only color
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img_bgr,img_bgr, mask= mask)

    cv2.imshow('img_bgr',img_bgr)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def filterOutGreenObjects(img_bgr):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    lower = np.array([36,100,100])
    upper = np.array([70,255,255])
    # Threshold the HSV image to get only color
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img_bgr,img_bgr, mask= mask)

    cv2.imshow('img_bgr',img_bgr)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def filterOutRedObjects(img_bgr):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    color = np.uint8([[[51,51,216]]])
    hsvColor = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
    hsvValue = hsvColor[0][0][0]
    lower = np.array([hsvValue - 10,100,100])
    upper = np.array([hsvValue - 10,255,255])
    # Threshold the HSV image to get only color
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img_bgr,img_bgr, mask= mask)

    cv2.imshow('img_bgr',img_bgr)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
