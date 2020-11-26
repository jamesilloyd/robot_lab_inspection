import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import part
from TemplateMatching import template_matching
import classification
import automationhat
time.sleep(0.1) # Short pause after ads1015 class creation recommended

# Toggle channel.
#automationhat.output[channel].write(state)
#input check
#automationhat.input[channel].is_on()
#analog input
#automationhat.analog[channel].read()

#set 3 outputs high so PLC has signal low
state = 1
for channel in range(3):
    automationhat.output[channel].write(state)


straightTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_straight.png'
leftTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_curve_left.png'
rightTemplateLocation = '/home/pi/robot_lab_inspection/TemplateMatching/template_curve.png'

pair_results = [1, 1, 0, 0, 1, 0]

while True:

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("static_inspection")

    while True:

        ret, frame = cam.read()

        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("static_inspection", frame)
        
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

    cam.release()
    cv2.destroyAllWindows()

    match_list = template_matching.templateMatching(img_bgr, img_template)

    print(match_list)

    # Use the templates to crop the image
    img_crop_bgr = template_matching.imageCropping(img_bgr, img_template, match_list)

    # Use the cropped image to classify the parts
    results, parts = classification.partClassification(img_crop_bgr, show = True,isCurves=curve)

    print(results)
    """
    automationhat.output[0].write(0)
    
    for pair in range len(pair_results):
        automationhat.output[2].write(1)
        while True:
            if automationhat.input[0].is_off():
                pass
            else:
                automationhat.output[1].write(1 - pair_results[pair])
                automationhat.output[2].write(0)
                break
    
    automationhat.output[0].write(1)
    """
    
