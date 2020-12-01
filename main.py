from cv2 import cv2
import numpy as np 
from frame_capture import FrameCapture
from matplotlib import pyplot as plt
from TemplateMatching import template_matching 
import templates
import thresholding
import classification

'''
This is going to be the main file used on the actual day. It is set up for moving classification. 
'''

'''FOR NOW THIS CODE ISN'T FINISHED, JUST SIMULATE THE OUTPUT IN THE WAY THAT PLC WANTS TO RECIEVE IT'''
# Look for signal from PLC
# When received start recording
# Look through frames and pass through frame capture function
# If it returns true then stop recording and run analysis
    # Chuck into the template cropping function
    # Chuck into the thresholding function
    # Chuck into the classification function (will need to modify outputs)
    # Save results to vision csv and plc csv
    # Also save a copy of the classified image (where) (imwrite)
    # Wait for signal from PLC for part positions and relay information to them
    # Either run the above on a different thread or end this program and go back to waiting for a signal from PLC to start recording again

# templateLocation = 'templates/template_moving_straight.png'
# templateImage = cv2.imread(templateLocation,0)

# untouchables = [14,16,18]
for i in range(20):
    print(i)

    # image_location = 'capture/10mm_{0}.avi'.format(i)
    image_location = 'TemplateMatching/Videos/group4/test{0}.avi'.format(i)

    capture = cv2.VideoCapture(image_location)
    foundFrame = False
    count = 0
    pieceType = 'unknown'

    while (capture.isOpened()):
    

        ret, frame_bgr = capture.read()


        # Video is finished
        if(frame_bgr is None):
            # TODO: change this to boolean var foundFrame
            print('DID NOT FIND FRAME')
            break

    
        # Video is running
        foundFrame, count = FrameCapture(frame_bgr,show=False)

        if(foundFrame):
            if(count == 1):
                pieceType = "straight"
            elif(count == 2):
                pieceType = "curveLeft"
            elif(count == 3):
                pieceType = "curveRight"
            else:
                #TODO: RAISE ERROR
                pieceType = "unknown"

            break

        #  TODO: also add in code here for allow manual cancellation.

        # TOOD: failure code in case the frame wasn't detected????
        

    # Release everything if the frame is found
    capture.release()
    cv2.destroyAllWindows()
    curved = False


    if(foundFrame): 
        
        if(i>15):
            curved = True
            frame_cropped = frame_bgr[0:400,0:600]
            
        else:
            curved = False
            frame_cropped = frame_bgr[0:385,60:600]


        resultsVision, resultsPLC, img_classified = classification.partClassification(frame_cropped,show=True,isCurves=curved,isMoving=True)



        # plt.imshow(cv2.cvtColor(frame_cropped,cv2.COLOR_BGR2RGB))

        # plt.show()









    # Insert selected frame into cropping function
    # match_list = template_matching.templateMatching(frame_bgr,templateImage)
    # img_crop_bgr = template_matching.imageCropping(frame_bgr,templateImage,match_list)
    # plt.imshow(img_crop_bgr, "gray")
    # plt.show()









    # Chuck into the template cropping function
    # match_list = template_matching.templateMatching(frame_bgr,img_template)
    # img_crop_bgr = template_matching.imageCropping(frame_bgr,img_template,match_list)

    # Chuck into the thresholding function
    # Chuck into the classification function (will need to modify outputs)
    # Save results to vision csv and plc csv
    # Also save a copy of the classified image (where) (imwrite)

