import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import part
from TemplateMatching import template_matching
import classification



if __name__ == "__main__":

    templateLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/TemplateMatching/template_straight.png'
    img_template = cv2.imread(templateLocation,0)

    for i in range(46):
        imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Dock Images/straight/group4/opencv_frame_{0}.png'.format(i)
        img_bgr = cv2.imread(imageLocation)

        match_list, temp_w, temp_h = template_matching.templateMatching(img_bgr, img_template)

        print(match_list)

        img_crop_bgr = template_matching.imageCropping(img_bgr, match_list, temp_w, temp_h)

        results, parts = classification.straightClassification(img_crop_bgr, show = True) 

        print(results)