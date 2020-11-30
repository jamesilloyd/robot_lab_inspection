from cv2 import cv2
import numpy as np 
from frame_capture import FrameCapture
from matplotlib import pyplot as plt
from TemplateMatching import template_matching 
import templates

# TODO: THIS IS TEMPORARY
templateLocation = 'templates/template_moving_curve_left.png'
img_template = cv2.imread(templateLocation,0)



cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('10mm_1.avi',fourcc, 20.0, (640,480))

#out = cv2.VideoWriter('10mm_1.avi',fourcc, 20.0)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #frame = cv2.flip(frame,0)
        #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    else:
        break


# TODO: change input type to video recording
#for image in range(1,8):
#    image_location = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Videos/grp23/test{0}.avi'.format(image)
    capture = cv2.VideoCapture(image_location)
    
    while (capture.isOpened()):

        ret, frame_bgr = capture.read()

        # Video is finished
        if(frame_bgr is None):
            # TODO: change this to boolean var foundFrame
            break

        # Video is running
        elif(FrameCapture(frame_bgr,show = False)):
            break

        # TODO: also add in code here for allow manual cancellation.

        # TOOD: failure code in case the frame wasn't detected????

        

    # Release everything if the frame is found
    cap.release()
    out.release()
    cv2.destroyAllWindows()


    '''FOR NOW THIS CODE ISN'T FINISHED, JUST SIMULATE THE OUTPUT IN THE WAY THAT PLC WANTS TO RECIEVE IT'''

    # Chuck into the template cropping function
    # match_list = template_matching.templateMatching(frame_bgr,img_template)
    # img_crop_bgr = template_matching.imageCropping(frame_bgr,img_template,match_list)

    # Chuck into the thresholding function
    # Chuck into the classification function (will need to modify outputs)
    # Save results to vision csv and plc csv
    # Also save a copy of the classified image (where) (imwrite)



    #Show restuls
    img_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()