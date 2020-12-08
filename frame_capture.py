from cv2 import cv2
from matplotlib import pyplot as plt 
import numpy as np





'''
The FrameCapture function is used to determine whether the correct frame has been found and 
also report back on how many green dots are show in the frame (if any).
To do this it calls the filterOutColoredObjects function that takes an image and a BGR color array to filter. 
'''

# Establish the green dot color that will be used for filtering the correct colour
greenDotColor = np.uint8([[[40,89,24]]])

def filterOutColoredObjects(img_bgr, colorArray, show = False):

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

     # define range of color in HSV
    hsvColor = cv2.cvtColor(colorArray,cv2.COLOR_BGR2HSV)
    hsvColorValue = hsvColor[0][0][0]
    lower = np.array([hsvColorValue - 10,75,75])
    upper = np.array([hsvColorValue + 10,255,255])
    # Threshold the HSV image to get only that color
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img_bgr,img_bgr, mask = mask)

    if(show):
        plt.figure(figsize = (7,7))
        plt.imshow(mask)
        plt.axis('off')
        plt.show()

    # Invert the mask to be used for contouring
    mask_inv = 255 - mask

    return mask_inv


def FrameCapture(frame_bgr, show = False):

    # Establish the minimum area a dot can have to be valid
    minDotArea = 100
    # Initialise variables to be outputted
    foundCorrectFrame = False
    foundGreenDot = False
    # Init dot variables
    cx = 0
    cy = 0
    count = 0

    # Get the height and width of the frame
    imageHeight , imageWidth = frame_bgr.shape[:2]
    # Convert to rgb for plotting
    img_rgb = cv2.cvtColor(frame_bgr,cv2.COLOR_BGR2RGB)
    # Use above function to create a mask for any green coloured objects
    mask_inv = filterOutColoredObjects(frame_bgr,greenDotColor,show=False)
    # Get the contours from the mask
    contours, hierarchy = cv2.findContours(mask_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours
    for i, contour in enumerate(contours):
        
        if(hierarchy[0][i][3]==0):
            if(cv2.contourArea(contour) > minDotArea):
                # Found a contour that is inside the outer edge and is not of negliglbe size
                # Have found at least one dot on the screen
                foundGreenDot = True
                dotContour = contour
                # Get the coordinates of the coordinate centre
                M = cv2.moments(dotContour)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])   
                # if the x position is over 93% of image width you have found the right frame
                if(cx > imageWidth*0.93): 
                    foundCorrectFrame = True
                    count += 1
                     # Plot the dot centre point and contours
                    cv2.circle(img_rgb,(cx,cy), 3, (255,0,0), -1)
                    cv2.drawContours(img_rgb, contours, -1, (0,0,255), 2)


    if(show and foundCorrectFrame):
        plt.figure(figsize = (7,7))
        plt.imshow(img_rgb)
        plt.title("Count {0}".format(count))
        plt.axis('off')
        plt.show()

    
    return foundCorrectFrame, count, foundGreenDot
