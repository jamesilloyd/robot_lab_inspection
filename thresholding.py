from cv2 import cv2
import numpy as np 
from matplotlib import pyplot as plt
import part


'''
This file has functions for different thresholding techniques.

The one we are using our function is otsuThresholding. 
Others were only used for testing during development phase.
'''

def otsuThresholding(img_gray, isCurved = True,isMoving = False):

    # Is this too high?
    # The minimum area is used to remove any contours that should be neglected
    minArea = 160
    maxArea = 30000

    # Apply a gaussion blur to the grey image
    blur = cv2.GaussianBlur(img_gray,(5,5),0)
    # Apply otsu thresholding to the blurred image
    ret3 , thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # plt.imshow(thresh, "gray")
    # plt.show()

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Prepare a list for the part objects corresponding to contours
    parts = []

    # This check ensures that the tray isn't empty (and a silly amount of contours have been detected)
    if(len(contours) < 30):
        # Iterate through contours found
        for m, contour in enumerate(contours):
            # If the contour is on the outside, you have found a part
            if hierarchy[0][m][3] == -1:
                # Check that the part has a non negligble area
                if (maxArea > cv2.contourArea(contour) > minArea):
                    # YOU HAVE FOUND A PART
                    # Create a list to add the contour's child contours to
                    child_contours = []
                    
                    # Check if the contour has a child
                    if hierarchy[0][m][2] != -1:
                        # Get the index of the child contour
                        index = hierarchy[0][m][2]
                        foundLastChild = False

                        while foundLastChild is False:
                            # Use recurrsion to get all the child contours (this is not actually recurssion)
                            child_contours, index, foundLastChild = addChildContoursToList(child_contours,contours,hierarchy,index)
                            
                    # Create a part object for each contour found
                    if(isCurved):
                        if(isMoving):
                            piece = part.MovingCurvedPart(contour)
                        else:
                            piece = part.CurvedPart(contour)

                    else:
                        if(isMoving):
                            piece = part.MovingStraightPart(contour)
                        else:
                            piece = part.StraightPart(contour)
                    # Add the child contours to the object
                    piece.childContours = child_contours
                    # Add the part object to the list to be returned
                    parts.append(piece)

    # Return the list of part objects to be classified
    return parts


def addChildContoursToList(childContourList,contours,hierarchy,index):
    # Add child to list
    childContourList.append(contours[index])
    # Check if there is another child
    if hierarchy[0][index][0] != -1:
        # Get the new child index
        newIndex = hierarchy[0][index][0]
        # Return the updated contour list, the index for the the next countour
        # If there is another child return False to indicate calling the function again
        return childContourList, newIndex, False
    else:
        # Return the completed contour list, same index as before, and true to indicate we have found the last child
        return childContourList, index, True

    




# --------------NOT USED--------------NOT USED--------------NOT USED--------------NOT USED-------------- #

# This function needs to take a blurred / smoothed image
def simpleThresholding(img_gray):
    #want to first put a blur on it
    # img = cv2.medianBlur(img_bgr,5)
    
    threshold = 127
    maxValue = 255

    ret, thresh1 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_TOZERO_INV)


    titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [img_gray, thresh1, thresh2, thresh3, thresh4, thresh5]

    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()


def adaptiveThresholding(img_gray):


    ksize = 5
    img_blur = cv2.blur(img_gray,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
    img_median = cv2.medianBlur(img_gray,ksize)

    # Adaptive thesholding
    # Penultimate variable is the size of the matrix to create the adaptive thresh mean / guas
    # Choosing between gaussian and median will vary between image types, need to play around with them
    blockSize = 127
    constant = 11

    # Trialling different blurs and adaptive types

    # thresh1 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # thresh3 = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh4 = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # thresh5 = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh6 = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # thresh7 = cv2.adaptiveThreshold(img_median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh8 = cv2.adaptiveThreshold(img_median, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows() 


    # titles = ['Original Image','Mean_bin','Gaus_bin']
    # images = [img_gray, thresh1, thresh2]

    # for i in range(len(images)):
    #     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])

    # plt.show()


    # Using an iterative approach to identify which block size and constant that contours the correct number of objects
    for i in range(150):
        
        if((i % 2 == 1) and (i > 1)):
            
            for j in range(30):
                
                # Trial with different blur types
                thresh = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,i,j)
                # cv2.imshow('{0}_{1}'.format(i,j),thresh)

                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                contour_filter=[]
                count = 0
                img_contour= cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
                for k,contour in enumerate(contours):
                    if hierarchy[0][k][3]==0:
                        count += 1
                        cv2.drawContours(img_contour, [contour], -1, (0,0,255), 2)  
                        contour_filter.append(contour)

                print(count)
                if count < 10 and count > 3 :
                    print('blocksize {0} and constant {1}'.format(i,j))

                    cv2.drawContours(img_contour, contours, -1, (0,0,255), 1)

                    plt.figure(figsize = (5,5))
                    plt.imshow(img_contour)
                    plt.axis('off')
                    plt.show()
