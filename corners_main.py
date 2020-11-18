import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import thresholding
import part
from mpl_toolkits.mplot3d import Axes3D


def curvedPieces(img_bgr, show = False):

    results = {"0":0,
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "8":0,
                "9":0,
                "10":0,
                "11":0}


    img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)

    imageHeight , imageWidth = img_bgr.shape[:2]

    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    parts = thresholding.otsuThresholding(img_gray)
    
    # Sort parts by position in the grid (Top left to right)
    parts.sort(key=lambda x: x.centreXY[0], reverse=False)
    parts.sort(key=lambda x: x.centreXY[1], reverse=False)

    for j, piece in enumerate(parts):
        
        cv2.drawContours(img_rgb, [piece.contour], -1, (0,0,255), 2)
        cv2.drawContours(img_rgb,piece.childContours,-1,(0,0,255), 1)
        img = cv2.putText(img_rgb ,str(j),piece.centreXY,cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 
        img = cv2.circle(img_rgb,piece.centreXY, 3, (255,0,0), -1)

        rect = cv2.minAreaRect(piece.contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Classifying using parameters
        if(piece.aspectRatio > 0.43 and piece.aspectRatio < 0.47 and piece.solidity > 0.80 and piece.solidity < 0.84 and piece.area / piece.perimeter > 16.2 and piece.area / piece.perimeter < 17.1):
            piece.isQCPassed = True
            if show: img = cv2.drawContours(img_rgb,[box],0,(0,255,0),1)
        else:
            piece.isQCPassed = False
            if show: img = cv2.drawContours(img_rgb,[box],0,(255,0,0),1)

        resultIndex = 0
        # Find the correct index to mark as good
        if(piece.centreXY[0]/imageWidth < 0.33):
            # print('x1')
            resultIndex += 0
        
        elif(piece.centreXY[0]/imageWidth < 0.66):
            # print('x2')
            resultIndex += 1
        
        else:
            # print('x3')
            resultIndex += 2


        if(piece.centreXY[1]/imageHeight < 0.25):
            # print('y1')
            resultIndex += 0
        
        elif(piece.centreXY[1]/imageHeight < 0.5):
            # print('y2')
            resultIndex += 3

        elif(piece.centreXY[1]/imageHeight < 0.75):
            # print('y3')
            resultIndex += 6
        
        else:
            # print('y4')
            resultIndex += 9

        if piece.isQCPassed:
            results[str(resultIndex)] = 1 
        
        else:
            results[str(resultIndex)] = 0

    if(show):
        plt.figure(figsize = (7,7))
        plt.title('Count: {0}'.format(len(parts)))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()

    return results


# imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/Corners/group6/opencv_frame_{0}.png'.format(i)
imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Dock Images/curve_right/group4/opencv_frame_29.png'
img_bgr = cv2.imread(imageLocation)

# ADD IN THE RIGHT CROPPED DIMENSIONS 
y1 = 45
x1 = 34

y2 = 434
x2 = 614

img_bgr = img_bgr[y1:y2,x1:x2]
print(curvedPieces(img_bgr, show = False))