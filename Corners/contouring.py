
import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import random 
import math

# ADD IN THE CORRECT IMAGE LOCATION
imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/Corners/4/opencv_frame_0.png'
img_bgr = cv2.imread(imageLocation)

# ADD IN THE RIGHT CROPPED DIMENSIONS 
y1 = 40
x1 = 34

y2 = 434
x2 = 614

img_bgr = img_bgr[y1:y2,x1:x2]

img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)
# cv2.imshow('img',img_gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def adaptiveThresholding(img_gray):

    ksize = 5
    img_blur = cv2.blur(img_gray,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
    img_median = cv2.medianBlur(img_gray,ksize)
    images = [img_blur, img_gaussian, img_median]
    thresholdTypes = [cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C]

    images_number = {0:"Blur", 1: "Guas", 2:"Median"}
    threshold_number = {0: "Mean",1:"Gaus"}

    # Adaptive thesholding
    # Penultimate variable is the size of the matrix to create the adaptive thresh mean / guas
    # Choosing between gaussian and median will vary between image types, need to play around with them
    # Using an iterative approach to identify which block size and constant that contours the correct number of objects
    for i in range(150):
        
        if((i % 2 == 1) and (i > 1)):
            
            for j in range(30):

                for k in range(len(images)):
                    
                    for l in range(len(thresholdTypes)):
                        # Trial with different blur types
                        # print('blocksize {0} and constant {1}. {2} , {3}'.format(i,j,images_number[k],threshold_number[l]))


                        thresh = cv2.adaptiveThreshold(images[k], 255, thresholdTypes[l], cv2.THRESH_BINARY,i,j)
                        # cv2.imshow('{0}_{1}'.format(i,j),thresh)

                        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        contour_filter=[]
                        count = 0
                        img_contour= cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
                        for m, contour in enumerate(contours):
                            if hierarchy[0][m][3]==0:
                                count += 1
                                cv2.drawContours(img_contour, [contour], -1, (0,0,255), 2)  
                                contour_filter.append(contour)

                        print(count)
                        if count == 12:
                            cv2.drawContours(img_contour, contours, -1, (0,0,255), 1)
                            plt.figure(figsize = (7,7)) 
                            plt.title('blocksize {0} and constant {1}. {2} , {3}'.format(i,j,images_number[k],threshold_number[l]))
                            plt.imshow(img_contour)
                            plt.axis('off')
                            plt.show()


# Not needed for now
def findCannyContoursParameters(img_bgr):
    # This function varies the input parameters to the canny
    # edge detection to see which combination yields the correct number of contours
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # METHOD 1 using Canny
    ksize = 3
    img_blur = cv2.blur(gray,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(gray,(ksize,ksize),0)
    img_median = cv2.medianBlur(gray,ksize)

    for i in range(20):
        for j in range(25):
            # Try this with different blur types
            canny = cv2.Canny(gray,j*10*(1-i*0.05),min(j*10*(1+i*0.05),255))
            cv2.imshow('canny',canny)

            # cv2.imshow('Canny_orig_{0}_{1}'.format(i*0.05,j*10), canny)

            contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contour_filter=[]
            count = 0
            img_contour= cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            for i,contour in enumerate(contours):
                if hierarchy[0][i][3]==0:
                    count += 1
                    cv2.drawContours(img_contour, [contour], -1, (0,0,255), 2)  
                    contour_filter.append(contour)
            
            print(hierarchy)

            print(count)
            # Want to see which combination of thresholds identifies the correct number of objects  
            if count == 12:

                print(contours)

                print(hierarchy)

                print('Threshold {0} and variance {1}'.format(i,j))
                print(i)
                print(j)
                cv2.drawContours(img_contour, contours, -1, (0,0,255), 1)

                plt.figure(figsize = (5,5))
                plt.imshow(img_contour)
                plt.axis('off')
                plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()



adaptiveThresholding(img_gray)

# findCannyContoursParameters(img_bgr)