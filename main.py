from cv2 import cv2
import numpy as np 
from frame_capture import FrameCapture
from matplotlib import pyplot as plt
from TemplateMatching import template_matching 
import templates
import thresholding

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

templateLocation = 'templates/template_moving_straight.png'
templateImage = cv2.imread(templateLocation)

for i in range(1,29):

    imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Videos/test{0}.avi'.format(i)
    capture = cv2.VideoCapture(imageLocation)
    
    
    while (capture.isOpened()):

        ret, frame_bgr = capture.read()

        # Video is finished
        if(frame_bgr is None):
            # TODO: change this to boolean var foundFrame
            break

        # Video is running
        elif(FrameCapture(frame_bgr,show = True)):
            break

        #  TODO: also add in code here for allow manual cancellation.

        # TOOD: failure code in case the frame wasn't detected????

        

    # Release everything if the frame is found
    capture.release()
    cv2.destroyAllWindows()

    # Insert selected frame into cropping function
    match_list = template_matching.templateMatching(frame_bgr,templateImage)
    img_crop_bgr = template_matching.imageCropping(frame_bgr,templateImage,match_list)

    plt.imshow(img_crop_bgr, "gray")
    plt.show()

    # thresholding.otsuThresholding(img_gray,isCurved=False)
    




    # Chuck into the template cropping function
    # match_list = template_matching.templateMatching(frame_bgr,img_template)
    # img_crop_bgr = template_matching.imageCropping(frame_bgr,img_template,match_list)

    # Chuck into the thresholding function
    # Chuck into the classification function (will need to modify outputs)
    # Save results to vision csv and plc csv
    # Also save a copy of the classified image (where) (imwrite)



    # Show restuls
    # img_rgb = cv2.cvtColor(img_crop_bgr, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_rgb)
    # plt.show()