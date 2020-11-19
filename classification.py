import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import thresholding
import part
from mpl_toolkits.mplot3d import Axes3D


def partClassification(img_bgr, show = False, isCurves = True):

    # Choose the correct ranges depending on whether the function is called for straight or curved pieces
    if isCurves:
        # Curved piece classification ranges
        aspectRatioRange = [0.43,0.47]
        solidityRange = [0.8,0.94]
        areaPerimeterRange = [16.2,17.1]

    else:
        # Straight piece classification ranges
        aspectRatioRange = [0.52,0.57]
        solidityRange = [0.80,0.85]
        areaPerimeterRange = [13.6,14.5]
    

    # Prepare the position results to be returned
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

    # Change to rgb for plotting purposes
    img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)

    # Get the image height and width to help map part positions to results grid
    imageHeight , imageWidth = img_bgr.shape[:2]

    # Convert the image to gray prepare for thresholding
    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    # Carry out otsu thrsholding on the cropped gray image
    parts = thresholding.otsuThresholding(img_gray)
    
    # Sort parts by position in the grid (Top left to right)
    parts.sort(key=lambda x: x.centreXY[0], reverse=False)
    parts.sort(key=lambda x: x.centreXY[1], reverse=False)

    # Iterate through the list of parts
    for j, piece in enumerate(parts):

        # If we are showing results, plot the contours, part number, and centre point
        if show:
            cv2.drawContours(img_rgb, [piece.contour], -1, (0,0,255), 2)
            cv2.drawContours(img_rgb,piece.childContours,-1,(0,0,255), 1)
            cv2.putText(img_rgb ,str(j),piece.centreXY,cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 
            cv2.circle(img_rgb,piece.centreXY, 3, (255,0,0), -1)
            # Get the bounding rectangle to be plotted after we have identified the part as good or bad
            rect = cv2.minAreaRect(piece.contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

        # Classifying using parameters of aspect ratio, solidity and area / perimeter
        if(piece.aspectRatio > aspectRatioRange[0] and piece.aspectRatio < aspectRatioRange[1] and piece.solidity > solidityRange[0] and piece.solidity < solidityRange[1] and piece.area / piece.perimeter > areaPerimeterRange[0] and piece.area / piece.perimeter < areaPerimeterRange[1]):
            # The part has passed QC and can be marked as good
            piece.isQCPassed = True
            # Draw a green box
            if show: cv2.drawContours(img_rgb,[box],0,(0,255,0),1)
        else:
            # The part has failed QC and can be marked as bad
            piece.isQCPassed = False
            # Draw a red box
            if show: cv2.drawContours(img_rgb,[box],0,(255,0,0),1)

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

        # Mark the piece as good or bad
        if piece.isQCPassed:
            results[str(resultIndex)] = 1 
        
        else:
            results[str(resultIndex)] = 0

    # Show results
    if(show):
        plt.figure(figsize = (7,7))
        plt.title('Count: {0}'.format(len(parts)))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()

    return results, parts

# For group 4 straight pieces images
# correct_part_tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1]