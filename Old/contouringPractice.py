
import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import random 
import math
import thresholding



def adaptiveThresholdingParameterFinder(img_gray,partCount,library,image_no):

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
    for k in range(len(images)):
        for l in range(len(thresholdTypes)):
            for i in range(150):
        
                if((i % 2 == 1) and (i > 1)):
            
                    for j in range(30):

                    
                        thresh = cv2.adaptiveThreshold(images[k], 255, thresholdTypes[l], cv2.THRESH_BINARY,i,j)

                        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        contour_filter=[]
                        count = 0
                        img_contour= cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
                        for m, contour in enumerate(contours):
                            if hierarchy[0][m][3]==0:
                                count += 1
                                cv2.drawContours(img_contour, [contour], -1, (0,0,255), 2)  
                                contour_filter.append(contour)

                        print('image {0} b_{1},c_{2},{3},{4}'.format(image_no,i,j,images_number[k],threshold_number[l]))
                        print(abs(count-partCount))

                        if 'b_{0},c_{1},{2},{3}'.format(i,j,images_number[k],threshold_number[l]) in library:
                            library['b_{0},c_{1},{2},{3}'.format(i,j,images_number[k],threshold_number[l])] += abs(count-partCount)
                        else:
                            library['b_{0},c_{1},{2},{3}'.format(i,j,images_number[k],threshold_number[l])] = abs(count-partCount)

                        # print(count)
                        # if count == partCount:
                        #     cv2.drawContours(img_contour, contours, -1, (0,0,255), 1)
                        #     plt.figure(figsize = (7,7)) 
                        #     plt.title('blocksize {0} and constant {1}. {2} , {3}'.format(i,j,images_number[k],threshold_number[l]))
                        #     plt.imshow(img_contour)
                        #     plt.axis('off')
                        #     plt.show()
    return library

def adaptiveThresholding(img_gray,imageNum,ThresholdNum,blocksize,constant):

    ksize = 5
    img_blur = cv2.blur(img_gray,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
    img_median = cv2.medianBlur(img_gray,ksize)
    images = [img_blur, img_gaussian, img_median]
    thresholdTypes = [cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C]

    images_number = {0:"Blur", 1: "Guas", 2:"Median"}
    threshold_number = {0: "Mean",1:"Gaus"}

    thresh = cv2.adaptiveThreshold(images[imageNum], 255, thresholdTypes[ThresholdNum], cv2.THRESH_BINARY,blocksize,constant)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_filter=[]
    count = 0
    img_contour= cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
    for m, contour in enumerate(contours):
        if hierarchy[0][m][3] == 0:
            print(hierarchy[0][m])
            print('hello')
            # print(contour)
            count += 1
            # cv2.drawContours(img_contour, [contour], -1, (0,0,255), 1)  
            cv2.drawContours(img_contour, [contours[hierarchy[0][m][0]]], -1, (0,0,255), 2)  
            contour_filter.append(contour)

    # cv2.drawContours(img_contour, contours[1], -1, (0,0,255), 1)
    plt.figure(figsize = (7,7)) 
    plt.title('blocksize {0} and constant {1}. {2} , {3}. Count: {4}'.format(blocksize,constant,images_number[imageNum],threshold_number[ThresholdNum],count))
    plt.imshow(img_contour)
    plt.axis('off')
    plt.show()




part_numbers = [12,

                12,
                12,
                12,
                12,
                12,

                11,
                11,
                12,
                12,
                12,

                12,
                12,
                12,
                12,
                12,
                
                12,
                12,
                12,
                11,
                12,
                
                12,
                12,
                12,
                12,
                12,
                
                9,
                9,
                9,
                10,
                11,
                
                12,
                12,
                12,
                11,
                12,
                
                10,
                12,
                11,
                11,
                7,
                
                7,
                7,
                8]




values = {}

for i in range(37):
    imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/straights/opencv_frame_{0}.png'.format(i)
    img_bgr = cv2.imread(imageLocation)

    # ADD IN THE RIGHT CROPPED DIMENSIONS 
    # y1 = 45
    # x1 = 34

    # y2 = 434
    # x2 = 614

    y1 = 40
    x1 = 80

    y2 = 420
    x2 = 590

    img_bgr = img_bgr[y1:y2,x1:x2]

    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    adaptiveThresholding(img_gray,2,0,9,19)


# values = {k: v for k, v in sorted(values.items(), key=lambda item: item[1],reverse= True)}

# print(values)
