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

# mask_inv = colorFiltering.filterOutColoredObjects(img_bgr,colorFiltering.blue,True)

#     contours, hierarchy = cv2.findContours(mask_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     contour_filter=[]
#     count = 0
#     for i,contour in enumerate(contours):
#         if hierarchy[0][i][3]==0:
#             count += 1
#             contour_filter.append(contour)

#     M = cv2.moments(contour_filter[0])
#     cx = int(M['m10']/M['m00'])
#     cy = int(M['m01']/M['m00'])

#     contour_filter_all = ZhengyangContourSolution(img_bgr,show = False)

#     for i, contour in enumerate(contour_filter_all):
#         result = cv2.pointPolygonTest(contour, (cx,cy), False)
#         if(result == 1):
#             print(i)

# OUTPUTS {bool is same object}
