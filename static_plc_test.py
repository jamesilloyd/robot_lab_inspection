"""
Test file used fpr handshaking with PLC to test outputs from inspection
"""

# Import modules
#import numpy as np
#from cv2 import cv2
#from matplotlib import pyplot as plt
#import part
#from TemplateMatching import template_matching
#import classification
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
#straightTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_straight.png'
#leftTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_curve_left.png'
#rightTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_curve.png'

results = [1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]
#results = [] #error result test

# Main loop of program for each image inspection
while True:

    while True:

        if GPIO.input(inp1) == 0:
            pass
        else:
            GPIO.output(out1, 0)
            if GPIO.input(inp2) == 0 and GPIO.input(inp3) == 1:
                print("straight")
            elif GPIO.input(inp1) == 1 and GPIO.input(inp2) == 0:
                print("curve left")
            elif GPIO.input(inp1) == 1 and GPIO.input(inp2) == 1:
                print("curve right")
            break
        
    """
    # Carry out template matching to produce a list of matched locations
    match_list = template_matching.templateMatching(img_bgr, img_template)

    print(match_list)

    # Use the templates to crop the image
    img_crop_bgr = template_matching.imageCropping(img_bgr, img_template, match_list)

    # Use the cropped image to classify the parts
    results, parts = classification.partClassification(img_crop_bgr, show = True,isCurves=curve)

    print(results)
    """
    print("simulating inspection")
    time.sleep(1)
    print("inspection complete")
    print(results)
    
    # Handshake with PLC to output pair results in sequence waiting for confirmation from PLC each time
    GPIO.output(out1, 1)
    
    for result in range(len(results)):
        GPIO.output(out2, 1)
        while True:
            if GPIO.input(inp1) == 1:
                GPIO.output(out3, 1 - results[result])
                GPIO.output(out2, 0)
                time.sleep(0.1)
                break
            else:
                pass
            
    GPIO.output(out1, 0)

