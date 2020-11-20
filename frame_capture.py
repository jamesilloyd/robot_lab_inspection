from cv2 import cv2
from matplotlib import pyplot as plt 
import numpy as np

capture = cv2.VideoCapture('test5.avi')

# TODO: how do we make this bit more robust
greenDotColor = np.uint8([[[40,89,24]]])

minArea = 100
# Init dot position variables
cx = 0
cy = 0

def filterOutColoredObjects(img_bgr, colorArray, show = False):

    # img_rgb = cv2.cvtColor(img_bgr, cv2.COlOR_BGR2RGB)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

     # define range of color in HSV
    hsvColor = cv2.cvtColor(colorArray,cv2.COLOR_BGR2HSV)
    hsvColorValue = hsvColor[0][0][0]
    lower = np.array([hsvColorValue - 10,75,75])
    upper = np.array([hsvColorValue + 10,255,255])
    # Threshold the HSV image to get only that color
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img_bgr,img_bgr, mask = mask)

    if(show):

        plt.figure(figsize = (7,7))
        plt.imshow(mask)
        plt.axis('off')
        plt.show()

        # cv2.imshow('img_bgr',img_bgr)
        # cv2.imshow('mask',mask)
        # cv2.imshow('res',res)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # Invert the mask to be used for contouring
    mask_inv = 255 - mask

    return mask_inv

while (capture.isOpened()):

    ret, frame_bgr = capture.read()
    
    # Imshow not working 

    # Video is finished
    if(frame_bgr is None):
        break
    # Video is running
    else:
        imageHeight , imageWidth = frame_bgr.shape[:2]
        # Convert to rgb for plotting
        img_rgb = cv2.cvtColor(frame_bgr,cv2.COLOR_BGR2RGB)
        # Use above function to create a mask for any green coloured objects
        mask_inv = filterOutColoredObjects(frame_bgr,greenDotColor,show=False)
        # Get the contours from the mask
        contours, hierarchy = cv2.findContours(mask_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Loop through the contours
        for i, contour in enumerate(contours):
            
            if(hierarchy[0][i][3]==0):
                if(cv2.contourArea(contour) > minArea):
                    # Found a contour that is inside the outer edge and is not of negliglbe size
                    dotContour = contour
                    # Get the coordinates of the coordinate centre
                    M = cv2.moments(dotContour)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])   
                    # if the x position is over 90% of image width you have found the right frame
                    if(cx > imageWidth*0.9): 


                        # Plot the image centre and contours
                        cv2.circle(img_rgb,(cx,cy), 3, (255,0,0), -1)
                        cv2.drawContours(img_rgb, contours, -1, (0,0,255), 2)
                        plt.figure(figsize = (7,7))
                        plt.imshow(img_rgb)
                        plt.title(len(contours))
                        plt.axis('off')
                        plt.show()

            
            # take the contours of the inverted mask
            
            # Identify the centre point of the dot
            
            # img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            #  # Apply a gaussion blur to the grey image
            # blur = cv2.GaussianBlur(img_gray,(5,5),0)
            # # Apply otsu thresholding to the blurred image
            # ret3 , thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            

            # cv2.drawContours(img_rgb, contours, -1, (0,0,255), 1)

            # plt.figure(figsize = (7,7))
            # plt.imshow(img_rgb)
            # plt.axis('off')
            # plt.show()
            # plt.imshow(thresh,'gray')
            # plt.axis('off')
            # plt.show()


        # cv2.imshow('Video',frame)

        # plt.imshow(frame)
        # plt.axis('off')
        # plt.show()

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break 

capture.release()
cv2.destroyAllWindows()

