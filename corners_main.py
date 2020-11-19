import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import part
from TemplateMatching import template_matching
import classification



if __name__ == "__main__":

    templateLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/TemplateMatching/template_curve.png'
    img_template = cv2.imread(templateLocation,0)

    for i in range(63):
        imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Dock Images/curve_right/group6/opencv_frame_{0}.png'.format(i)
        img_bgr = cv2.imread(imageLocation)

        match_list, temp_w, temp_h = template_matching.templateMatching(img_bgr, img_template)

        print(match_list)

        img_crop_bgr = template_matching.imageCropping(img_bgr, match_list, temp_w, temp_h)

        print(classification.curvedPieces(img_crop_bgr, show = True))