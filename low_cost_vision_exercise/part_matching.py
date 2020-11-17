import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt


# INPUTs {contour, cx, cy

'''
Below is an example of how this would work:
    -find the single contour of an object you have identified
    -find the centre of the contour to get a point
    -get the list of contours you want to match the point to
    -loop through the list checking whether the point is inside the any of the contours
    -if it is inside one of the contours return the contour it is inside
        -you can use this to match the contours up
'''


    # contour_filter_all = ZhengyangContourSolution(img_bgr,show = True)

    # part_objects = []
    # for i,contour in enumerate(contour_filter_all):
    #     part_objects.append(Part(contour))


    # mask_inv = colorFiltering.filterOutColoredObjects(img_bgr,colorFiltering.blue,False)
    # cv2.imshow('mask_inv',mask_inv)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # mask_contours, hierarchy = cv2.findContours(mask_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # contour_filter=[]
    # count = 0
    # for i,contour in enumerate(mask_contours):
    #     if hierarchy[0][i][3]==0:
    #         count += 1
    #         contour_filter.append(contour)

    # contour = contour_filter[0]
    # bluePart = Part(contour_filter[0])

    # for i, part in enumerate(part_objects):
    #     if(cv2.pointPolygonTest(part.contour,bluePart.centreXY,False)==1):
    #         part.isIdentified = True
    #         part.colour = "blue"


    # for i,part in enumerate(part_objects):
    #     print("Color: {0}, isIdentified: {1}".format(part.colour,part.isIdentified))

    
# OUTPUTS {bool is same object}
