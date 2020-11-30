import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import part
from TemplateMatching import template_matching
import classification

'''
IT IS NO LONGER USED, JUST USED FOR REFERENCE
This file is for classifying static curved trays.
'''

if __name__ == "__main__":
    # getting the template part
    leftTemplateLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/TemplateMatching/template_curve_left.png'
    rightTemplateLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/TemplateMatching/template_curve.png'
    img_template = cv2.imread(leftTemplateLocation,0)

    for i in range(14):
        # Getting the image to test on
        imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Dock Images/curve_left/group1/opencv_frame_{0}.png'.format(i)
        # imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Data/Corner/4/opencv_frame_{0}.png'.format(i)
        img_bgr = cv2.imread(imageLocation)
        
        # Carry out template matching on the image 
        match_list = template_matching.templateMatching(img_bgr, img_template)

        print(match_list)
        # Use the templates to crop the image
        img_crop_bgr = template_matching.imageCropping(img_bgr, img_template, match_list)
        
        # Use the cropped image to classify the parts
        results, parts = classification.partClassification(img_crop_bgr, show = True,isCurves=True)

        print(results)
        print()