from cv2  import cv2
import numpy as np
from matplotlib import pyplot as plt


def findContours(img_bgr):
    # This function is varies the input parameters to the canny 
    # edge detection to see which combination yields the correct number of contours
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # METHOD 1 using Canny
    ksize = 3
    img_blur = cv2.blur(gray,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(gray,(ksize,ksize),0)
    img_median = cv2.medianBlur(gray,ksize)

    for i in range(20):
        print("Threshold 1: {0}".format(i*0.05))
        for j in range(25):
            print("Variance: {0}".format(j*10))
            # Try this with different blur types
            canny = cv2.Canny(img_gaussian,j*10*(1-i*0.05),min(j*10*(1+i*0.05),255))

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

            print(count)
            # Want to see which combination of thresholds identifies the correct number of objects  
            # if count == 13 or count == 12:
            if count == 9:
                print(i)
                print(j)
                cv2.drawContours(img_contour, contours, -1, (0,0,255), 1)

                plt.figure(figsize = (5,5))
                plt.imshow(img_contour)
                plt.axis('off')
                plt.show()