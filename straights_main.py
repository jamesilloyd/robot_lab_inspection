import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import part
from TemplateMatching import template_matching
import classification

'''
This file is for classifying static straight trays 
'''


if __name__ == "__main__":

    # getting the template part
    templateLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/TemplateMatching/template_straight.png'
    img_template = cv2.imread(templateLocation,0)

    for i in range(46):
        # Getting the image to test on
        imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Dock Images/straight/group4/opencv_frame_{0}.png'.format(i)
        img_bgr = cv2.imread(imageLocation)

        # Carry out template matching on the image 
        match_list = template_matching.templateMatching(img_bgr, img_template)

        print(match_list)

        # Use the templates to crop the image
        img_crop_bgr = template_matching.imageCropping(img_bgr, img_template, match_list)

        # Use the cropped image to classify the parts
        results, parts = classification.partClassification(img_crop_bgr, show = True,isCurves=False)

        print(results)