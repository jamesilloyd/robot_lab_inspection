import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import thresholding
import part
from mpl_toolkits.mplot3d import Axes3D


def partClassification(img_bgr, show = False, isCurves = True):    

    # Prepare the position results to be returned
    results = {"0":{'QCPassed': False, 'reason' : 'part missing'},
                "1":{'QCPassed': False, 'reason' : 'part missing'},
                "2":{'QCPassed': False, 'reason' : 'part missing'},
                "3":{'QCPassed': False, 'reason' : 'part missing'},
                "4":{'QCPassed': False, 'reason' : 'part missing'},
                "5":{'QCPassed': False, 'reason' : 'part missing'},
                "6":{'QCPassed': False, 'reason' : 'part missing'},
                "7":{'QCPassed': False, 'reason' : 'part missing'},
                "8":{'QCPassed': False, 'reason' : 'part missing'},
                "9":{'QCPassed': False, 'reason' : 'part missing'},
                "10":{'QCPassed': False, 'reason' : 'part missing'},
                "11":{'QCPassed': False, 'reason' : 'part missing'}}

    # prepare variables for graph title
    passedCount = 0
    failedCount = 0

    # Change to rgb for plotting purposes
    img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)

    # Get the image height and width to help map part positions to results grid
    imageHeight , imageWidth = img_bgr.shape[:2]

    # Convert the image to gray prepare for thresholding
    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    # Carry out otsu thrsholding on the cropped gray image
    parts = thresholding.otsuThresholding(img_gray, isCurved = isCurves)
    
    # Sort parts by position in the grid (Top left to right)
    # TODO: may not need this
    parts.sort(key=lambda x: x.centreXY[0], reverse=False)
    parts.sort(key=lambda x: x.centreXY[1], reverse=False)

    # Iterate through the list of parts
    for j, piece in enumerate(parts):

        # If we are showing results, plot the contours, part number, and centre point
        if show:
            cv2.drawContours(img_rgb, [piece.contour], -1, (0,0,255), 2)
            cv2.drawContours(img_rgb,piece.childContours,-1,(0,0,255), 1)
            cv2.putText(img_rgb ,str(j),piece.centreXYText,cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 
            cv2.circle(img_rgb,piece.centreXY, 3, (255,0,0), -1)
            # Get the bounding rectangle to be plotted after we have identified the part as good or bad
            rect = cv2.minAreaRect(piece.contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)


        # This code finds the part index within the results grid dictionary to be marked as good 
        resultIndex = 0
        # Find the correct index the piece corresponds to
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

        # The object is automatically QC checked on initialisation
        # Mark the QC result on the output dictionary
        results[str(resultIndex)]["QCPassed"] = piece.isQCPassed
        results[str(resultIndex)]["reason"] = piece.reasonForFailure


        if piece.isQCPassed:
            if show: cv2.drawContours(img_rgb,[box],0,(0,255,0),1)
            passedCount += 1
        
        else:
            if show: cv2.drawContours(img_rgb,[box],0,(255,0,0),1)
            failedCount += 1

    # Show results
    if(show):
        plt.figure(figsize = (7,7))
        plt.title('Count: {0} - {1} Passed - {2} Failed'.format(len(parts),passedCount,failedCount))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()

    return results, parts
