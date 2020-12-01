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

# templateLocation = 'templates/template_moving_straight.png'
# templateImage = cv2.imread(templateLocation,0)

# untouchables = [14,16,18]
# for i in range(20):
#     print(i)

#     # image_location = 'capture/10mm_{0}.avi'.format(i)
#     image_location = 'TemplateMatching/Videos/group4/test{0}.avi'.format(i)

# Need to take frame after for moving images

video_location = 'capture/10mm_1.avi'

capture = cv2.VideoCapture(0)
foundFrame = False
count = 0
pieceType = 'unknown'

while (capture.isOpened()):

    ret, frame_bgr = capture.read()

    cv2.imshow(frame_bgr)
    cv2.waitKey(1)

    # curved = False

    # Video is finished
    if(frame_bgr is None):
        # TODO: change this to boolean var foundFrame
        print('DID NOT FIND FRAME')
        break

    # cv2.imshow('frame',frame_bgr)
    # cv2.waitKey(1)


    # # Video is running
    # # TODO: make this code output another check for seeing if it's found the green dot at all (then it know's if it missed it or not)
    # foundFrame, count = FrameCapture(frame_bgr,show=False)

    # if(foundFrame):
    #     if(count == 1):
    #         pieceType = "straight"
    #         curved = False
    #     elif(count == 2):
    #         pieceType = "curveLeft"
    #         curved = True
    #     elif(count == 3):
    #         pieceType = "curveRight"
    #         curved = True
    #     else:
    #         #TODO: RAISE ERROR
    #         pieceType = "unknown"
    #     break


    #     #  TODO: also add in code here for allow manual cancellation.

    #     # TODO: failure code in case the frame wasn't detected????
        

# Release everything if the frame is found
capture.release()
cv2.destroyAllWindows()

print(count)
# Find a better way of cropping these 
if(curved):
    frame_cropped = frame_bgr[0:600,0:600]
else:
    frame_cropped = frame_bgr[0:385,60:600]
'''
frame_cropped = frame_bgr
'''
# resultsVision, resultsPLC, img_classified = classification.partClassification(frame_cropped,show=True,isCurves=curved,isMoving=True)



        # plt.imshow(cv2.cvtColor(frame_cropped,cv2.COLOR_BGR2RGB))

    # plt.show()

