"""
Inspection file used for classification of static images and integration with PLC
"""

# Import modules
import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import part
from TemplateMatching import template_matching
import classification
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
import time

# Define GPIO I/O connections
inp1 = 37
inp2 = 38
inp3 = 40
out1 = 29
out2 = 32
out3 = 31
out4 = 33 #has an issue with the current board
out5 = 35
out6 = 36

GPIO.setup(inp1, GPIO.IN)
GPIO.setup(inp2, GPIO.IN)
GPIO.setup(inp3, GPIO.IN)
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.setup(out4, GPIO.OUT)
GPIO.setup(out5, GPIO.OUT)
GPIO.setup(out6, GPIO.OUT)

# Reverse logic used on RPi to give standard logic input to PLC
GPIO.output(out1, 1)
GPIO.output(out2, 1)
GPIO.output(out3, 1)
GPIO.output(out4, 1)
GPIO.output(out5, 1)
GPIO.output(out6, 1)

# Set template image locations for template matching
straightTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_straight.png'
leftTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_curve_left.png'
rightTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_curve.png'

#pair_results = [1, 1, 0, 0, 1, 0]

# Main loop of program for each image inspection
while True:

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("static_inspection")

    while True:

        ret, frame = cam.read()

        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("static_inspection", frame)
        
        # Checking for input from PLC defining the type of tray (may be replaced by green dots/template matching layer
        if GPIO.input(inp1) == 0 and GPIO.input(inp2) == 0:
            pass
        else:
            GPIO.output(out1, 0)
            img_bgr = frame
            if GPIO.input(inp1) == 0 and GPIO.input(inp2) == 1:
                curve = False
                img_template = cv2.imread(straightTemplateLocation,0)
            elif GPIO.input(inp1) == 1 and GPIO.input(inp2) == 0:
                curve = True
                img_template = cv2.imread(leftTemplateLocation,0)
            elif GPIO.input(inp1) == 1 and GPIO.input(inp2) == 1:
                curve = True
                img_template = cv2.imread(rightTemplateLocation,0)
            break
            
        """
        #simulating tray type straight/curve_left/curve_right
        k = cv2.waitKey(1)
        if k%256 == 49:
            img_bgr = frame
            curve = False
            img_template = cv2.imread(straightTemplateLocation,0)
            break
        elif k%256 == 50:
            img_bgr = frame
            curve = True
            img_template = cv2.imread(leftTemplateLocation,0)
            break
        elif k%256 == 51:
            img_bgr = frame
            curve = True
            img_template = cv2.imread(rightTemplateLocation,0)
            break
        """

    cam.release()
    cv2.destroyAllWindows()

    # Carry out template matching to produce a list of matched locations
    match_list = template_matching.templateMatching(img_bgr, img_template)

    print(match_list)

    # Use the templates to crop the image
    img_crop_bgr = template_matching.imageCropping(img_bgr, img_template, match_list)

    # Use the cropped image to classify the parts
    results, parts = classification.partClassification(img_crop_bgr, show = True,isCurves=curve)

    print(results)
    
    """
    ADD CODE TO GENERATE PAIRED RESULTS LIST FROM RESULTS DICTIONARY
    """
    
    # Handshake with PLC to output pair results in sequence waiting for confirmation from PLC each time
    GPIO.output(out1, 1)
    
    for pair in range len(pair_results):
        GPIO.output(out2, 1)
        while True:
            if GPIO.input(inp1) == 1:
                GPIO.output(out3, 1 - pair_results[pair])
                GPIO.output(out2, 0)
                time.sleep(0.1)
                break
            else:
                pass
            
    GPIO.output(out1, 0)

