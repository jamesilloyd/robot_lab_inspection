from cv2 import cv2
import numpy as np 
from frame_capture import FrameCapture
from matplotlib import pyplot as plt
from TemplateMatching import template_matching 
import templates
import thresholding
import classification
from save_results import ResultsSave
import os

'''
This is the file used for classifying the moving video footage
'''

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('10mm_4.avi',fourcc, 20.0, (640,480))

# Incrament this variable each time you re run the program (used for saving results)
testRun = 0
if not os.path.exists('results/moving_images_{0}'.format(testRun)):
    os.makedirs('results/moving_images_{0}'.format(testRun))

my_results = ResultsSave('results/moving_images_{0}/group4_moving_vision_result.csv'.format(testRun),'results/moving_images_{0}/group4_moving_plc_result.csv'.format(testRun))

capture = cv2.VideoCapture(0)
foundCorrectFrame = False
curved = False
dotCount = 0
trayNum = 0
pieceType = 'unknown'
expectingTray = False

while(capture.isOpened()):

    ret, frame_bgr = capture.read()

    # Display the image on screen
    cv2.imshow("frame", frame_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Cancel key pressed, ending recording')
        break
    
    try:
        #Following function returns a bool, int and bool corresponding to:
        #   -whether the correct tray has been found
        #   -how many dots
        #   -whether it has found a dot at all
        # This allows us to expect a frame to be captured, if not we have missed it and need to report that.
        foundCorrectFrame, dotCount, foundGreenDot = FrameCapture(frame_bgr,show=False)

        # If we have found a green dot we know we are expecting a tray
        if(foundGreenDot):
            expectingTray = True

        # Else if we have now lost the green dot but we are still expecting a tray something has going wrong
        elif(not foundGreenDot and expectingTray):
            
            expectingTray = False
            # Raise error to report failure
            raise ValueError('Error: Missed the tray')
            

        if(foundCorrectFrame):
            # Found the tray! 
            print('Found the tray')
            expectingTray = False
            trayNum += 1
            if(dotCount == 1):
                pieceType = "straight"
                curved = False
            elif(dotCount == 2):
                pieceType = "curve_left"
                curved = True
            elif(dotCount == 3):
                pieceType = "curve_right"
                curved = True
            else:
                pieceType = "unknown"
                raise ValueError('Error: found invalid number of dots')
            

            template_location = 'templates/template_moving_{0}.png'.format(pieceType)
            img_template = cv2.imread(template_location,0)

            foundTemplate = False

            match_list, foundTemplate = template_matching.templateMatching(frame_bgr,img_template,show=False)

            if(foundTemplate):

                # Use the templates to crop the image
                img_crop_bgr = template_matching.imageCropping(frame_bgr, img_template, match_list,show=False)

                resultsVision, resultsPLC, img_classified = classification.partClassification(img_crop_bgr,show=True,isCurves=curved,isMoving=True)

                # Display image on screen
                cv2.imshow('result{0}'.format(trayNum),img_classified)
                cv2.waitKey(100)
                
                # Write result
                cv2.imwrite('results/moving_images_{0}/classified_moving_tray_{1}.png'.format(testRun, trayNum),img_classified)

                for j in range(len(resultsVision)):
                    my_results.insert_vision(str(trayNum),str(j),str(resultsVision[str(j)]["QCPassed"]),resultsVision[str(j)]["reason"])

            else:
                print('There was an error templating the image')

    except Exception as error:
        print(error)
        print('Except block was triggered, tell plc we could not classify the tray')


# Release everything if the cancel key was pressed
capture.release()
#out.release()
cv2.waitKey(0)
cv2.destroyAllWindows()


