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
num = 0
my_results = ResultsSave('results/group4_moving_vision_result.csv','results/group4_moving_plc_result.csv')
for i in range(1,14):
    print(i)
    # Need to take frame after for moving images
    video_location = 'capture/fast_{0}.avi'.format(i)
    # video_location = 'TemplateMatching/Videos/group4/test{0}.avi'.format(i)

    capture = cv2.VideoCapture(video_location)
    foundCorrectFrame = False
    curved = False
    count = 0
    pieceType = 'unknown'

    expectingTray = False

    while(capture.isOpened()):

        ret, frame_bgr = capture.read()

        # Video is finished (THIS WILL NEED TO BE CHANGED TO SOME OTHER OUTPUT AS THE VIDEO WILL ALWAYS BE RECORDING ON THE DAY)
        if(frame_bgr is None):
            # TODO: change this to boolean var foundFrame
            print('Video Finished')
            break

        # cv2.imshow('frame',frame_bgr)
        # cv2.waitKey(1)
        
        #Returns a bool, int and bool corresponding to:
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
            print('Did not find the tray')
            expectingTray = False
            # TODO: add in error handling here
            

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
                #TODO: RAISE ERROR
                pieceType = "unknown"
            # break

            template_location = 'templates/template_moving_{0}.png'.format(pieceType)
            img_template = cv2.imread(template_location,0)


            # if(curved):
            #     frame_cropped = frame_bgr[0:390,0:600]
            # else:
            #     frame_cropped = frame_bgr[0:390,]

            # frame_cropped = frame_bgr

            foundTemplate = False

            match_list, foundTemplate = template_matching.templateMatching(frame_bgr,img_template,show=False)

            if(foundTemplate):

                # Use the templates to crop the image
                img_crop_bgr = template_matching.imageCropping(frame_bgr, img_template, match_list,show=False)

                resultsVision, resultsPLC, img_classified = classification.partClassification(img_crop_bgr,show=True,isCurves=curved,isMoving=True)
                
                cv2.imwrite('results/moving_images/classified_moving_tray_{0}.png'.format(num),img_classified)

                for j in range(len(resultsVision)):
                    my_results.insert_vision(str(num),str(j),str(resultsVision[str(j)]["QCPassed"]),resultsVision[str(j)]["reason"])

            else:
                print('there was an error templating the image')

        #  TODO: also add in code here for allow manual cancellation.

            
    # Release everything if the frame is found
    capture.release()
    cv2.destroyAllWindows()


