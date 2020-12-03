from cv2 import cv2
import numpy as np 
from frame_capture import FrameCapture
from matplotlib import pyplot as plt
from TemplateMatching import template_matching 
import templates
import thresholding
import classification
from save_results import ResultsSave

'''
This is the file used for classifying the moving video footage
'''

"""
capture = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('10mm_4.avi',fourcc, 20.0, (640,480))
"""

num = 0
my_results = ResultsSave('results/group4_moving_vision_result.csv','results/group4_moving_plc_result.csv')
for i in range(1,14):

    print(i)

    video_location = 'capture/fast_{0}.avi'.format(i)
    capture = cv2.VideoCapture(video_location)
    foundCorrectFrame = False
    curved = False
    count = 0
    pieceType = 'unknown'

    expectingTray = False

    while(capture.isOpened()):

        ret, frame_bgr = capture.read()

        # Video is finished
        if(frame_bgr is None):
            print('Video Finished')
            break
    
        try:
            #Following function returns a bool, int and bool corresponding to:
            #   -whether the correct tray has been found
            #   -how many dots
            #   -whether it has found a dot at all
            # This allows us to expect a frame to be captured, if not we have missed it and need to report that.
            foundCorrectFrame, count, foundGreenDot = FrameCapture(frame_bgr,show=False)

            # If we have found a green dot we know we are expecting a tray
            if(foundGreenDot):
                expectingTray = True
            
            # Else if we have now lost the green dot but we are still expecting a tray something has going wrong
            elif(not foundGreenDot and expectingTray):
                expectingTray = False
                # Raise error to report failure
                raise ValueError('Error: Missed the tray')
                

            # If we have found the correct frame, see how many dots are on the tray and then run the analysis
            if(foundCorrectFrame):
                expectingTray = False
                num += 1
                if(count == 1):
                    pieceType = "straight"
                    curved = False
                elif(count == 2):
                    pieceType = "curve_left"
                    curved = True
                elif(count == 3):
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

                    resultsVision, resultsPLC, img_classified = classification.partClassification(img_crop_bgr,show=False,isCurves=curved,isMoving=True)
                    
                    cv2.imwrite('results/moving_images/classified_moving_tray_{0}.png'.format(num),img_classified)

                    for j in range(len(resultsVision)):
                        my_results.insert_vision(str(num),str(j),str(resultsVision[str(j)]["QCPassed"]),resultsVision[str(j)]["reason"])

                else:
                    raise ValueError('Error: There was an error templating the image')

        except Exception as error:
            print(error)
            print('except block was triggered, tell plc we could not classify the tray')
            


    # Video is finished so release the camera and start again
    capture.release()
    #out.release()
    cv2.destroyAllWindows()


