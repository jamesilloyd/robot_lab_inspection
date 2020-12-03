"""
Inspection file used for classification of static images and integration with PLC
"""

# Import modules
from cv2 import cv2
from matplotlib import pyplot as plt
from TemplateMatching import template_matching
import classification
from save_results import ResultsSave
import RPi.GPIO as GPIO
import time
#import part

if __name__ == "__main__":

    # Initialisation
    print ("Initialising setup")

    # Set GPIO mode and warnings false
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    # Define GPIO I/O connections
    inp0 = 37
    inp1 = 38
    inp2 = 40
    out0 = 29
    out1 = 32
    out2 = 31
    #out3 = 33 #has an issue with the current board
    #out4 = 35 #not currently in use
    #out5 = 36 #not currently in use

    # Define GPIO pins as inputs and outputs respectively 
    GPIO.setup(inp0, GPIO.IN)
    GPIO.setup(inp1, GPIO.IN)
    GPIO.setup(inp2, GPIO.IN)
    GPIO.setup(out0, GPIO.OUT)
    GPIO.setup(out1, GPIO.OUT)
    GPIO.setup(out2, GPIO.OUT)

    # Set template image locations for template matching
    straightTemplateLocation = '/home/pi/robot_lab_inspection/templates/template_static_straight.png'
    leftTemplateLocation = '/home/pi/robot_lab_inspection/templates/template_static_curve_left.png'
    rightTemplateLocation = '/home/pi/robot_lab_inspection/templates/template_static_curve_right.png'

    # Initialise results saving object
    my_results=ResultsSave('results/group4_static_vision_result.csv','results/group4_static_plc_result.csv')

    # Start count for images inspected
    count = 0

    # Main loop of program for each image inspection

    while True:

        # Reverse logic used on RPi to give standard logic input to PLC
        # Reset all outputs at start of each loop
        GPIO.output(out0, 1)
        GPIO.output(out1, 1)
        GPIO.output(out2, 1)

        print("Initialising new window for image capture")
        print(count)
        
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("static_inspection")

        while True:

            ret, frame = cam.read()

            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("static_inspection", frame)

            cv2.waitKey(1) #check where this should be
            
            # Checking for input from PLC defining the type of tray
            if GPIO.input(inp0) == 0:
                pass
            else:
                ###Record input PLC bit
                print("PLC Go flag received to start inspection")
                GPIO.output(out0, 0)
                ###Record output bit
                print("RPi Busy flag set high")
                img_bgr = frame
                if GPIO.input(inp1) == 1 and GPIO.input(inp2) == 0:
                    ###Record input PLC bits
                    print("Straight tracks in dock")
                    curve = False
                    img_template = cv2.imread(straightTemplateLocation,0)
                elif GPIO.input(inp1) == 0 and GPIO.input(inp2) == 1:
                    ###Record input PLC bits
                    print("Left curve tracks in dock")
                    curve = True
                    img_template = cv2.imread(leftTemplateLocation,0)
                elif GPIO.input(inp1) == 1 and GPIO.input(inp2) == 1:
                    ###Record input PLC bits
                    print("Right curve tracks in dock")
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

        print("Starting static image inspection")

        # Carry out template matching to produce a list of matched locations
        match_list, foundTemplate = template_matching.templateMatching(img_bgr, img_template, show=False)

        if(foundTemplate):
            print("Templates found successfully")

            # Use the templates to crop the image
            img_crop_bgr = template_matching.imageCropping(img_bgr, img_template, match_list, show=False)

            # Use the cropped image to classify the parts
            resultsVision, resultsPLC, img_classified = classification.partClassification(img_crop_bgr, show = False, isCurves=curve)

            # Display the image on screen
            cv2.imshow('result{0}'.format(i),img_classified)
            cv2.waitKey(100)

            # Store image of classified tray for assessment
            cv2.imwrite('results/static_images/classified_tray_{0}.png'.format(count),img_classified)

            # Store results in csv file for assessment
            for j in range(len(resultsVision)):
                my_results.insert_vision(str(count),str(j),str(resultsVision[str(j)]["QCPassed"]),resultsVision[str(j)]["reason"])

            #### TODO: do something with plc results csv output

            results_order = [0, 1, 4, 5, 8, 9, 2, 3, 6, 7, 10, 11]

            results_list = []
            for i in results_order:
                result = resultsPLC[str(i)]
                if result == True:
                    results_list.append(1)
                else:
                    results_list.append(0)

            print("Inspection Results:")
            print(results_list)
            
            # Handshake with PLC to output individual results in sequence waiting for confirmation from PLC each time
            GPIO.output(out0, 1)
            print("RPi Busy flag set low")
            ###add one second delay here for PLC to ensure go-flag down
            time.sleep(2)
            
            for result in range(len(results_list)):
                while True:
                    if GPIO.input(inp0) == 1:
                        print("PLC Go flag received to send next result")
                        GPIO.output(out0, 0)
                        print("RPi Busy flag set high")
                
                        GPIO.output(out1, 1 - results_list[result])
                        print("RPi Part status flag set")
                        GPIO.output(out0, 1)
                        print("RPi Busy flag set low")
                        while GPIO.input(inp0) == 1:
                            pass
                        
                        #time.sleep(1)   #TODO check if this time needed, likely at least 1 second
                        break
                    else:
                        pass
                    
            #GPIO.output(out1, 0)
   

        else:
            print("No templates found")

            # Store image of unclassified tray for assessment
            cv2.imwrite('results/static_images/unclassified_tray_{0}.png'.format(count),img_bgr)

            GPIO.output(out2, 0)
            print("RPi Error flag set high")

            # Time to allow PLC to read error flag
            time.sleep(0.5)

        count += 1
