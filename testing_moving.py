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
for i in range(1,4):
    # Need to take frame after for moving images
    # video_location = 'capture/fast_long_1.avi'
    video_location = 'TemplateMatching/Videos/group6/test_{0}.avi'.format(i)

    

    capture = cv2.VideoCapture(video_location)
    foundFrame = False
    curved = False
    count = 0
    pieceType = 'unknown'

    while(capture.isOpened()):

        ret, frame_bgr = capture.read()

        # Video is finished
        if(frame_bgr is None):
            # TODO: change this to boolean var foundFrame
            print('Video Finished')
            if(not foundFrame):
                print("Did not find a frame")
            break

        # cv2.imshow('frame',frame_bgr)
        # cv2.waitKey(1)
        
        # TODO: make this code output another check for seeing if it's found the green dot at all (then it know's if it missed it or not)
        foundFrame, count = FrameCapture(frame_bgr,show=False)

        if(foundFrame):
            num += 1
            if(count == 1):
                pieceType = "straight"
                curved = False
            elif(count == 2):
                pieceType = "curveLeft"
                curved = True
            elif(count == 3):
                pieceType = "curveRight"
                curved = True
            else:
                #TODO: RAISE ERROR
                pieceType = "unknown"
            # break


            # if(curved):
            #     frame_cropped = frame_bgr[0:390,0:600]
            # else:
            #     frame_cropped = frame_bgr[0:390,]

            frame_cropped = frame_bgr

            resultsVision, resultsPLC, img_classified = classification.partClassification(frame_cropped,show=True,isCurves=curved,isMoving=True)
            
            cv2.imwrite('results/images/classified_moving_tray_{0}.png'.format(num),img_classified)

            for j in range(len(resultsVision)):
                my_results.insert_vision(str(num),str(j),str(resultsVision[str(j)]["QCPassed"]),resultsVision[str(j)]["reason"])

        #  TODO: also add in code here for allow manual cancellation.

        # TODO: failure code in case the frame wasn't detected????
            

    # Release everything if the frame is found
    capture.release()
    cv2.destroyAllWindows()


