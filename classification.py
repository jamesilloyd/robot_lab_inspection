import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import thresholding
import part
from mpl_toolkits.mplot3d import Axes3D


'''
partClassification is used to classify all the parts within a cropped image.
It's inputs are:
-img_bgr = the cropped image to be classified
-show = whether to show results using matplotlib (for debugging)
-isCurves = to create the correct part type object that will inherit the correct classification metric ranges
-isMoving = same as above (can have different part objects: static straight, static curve, moving straight, moving curve)
'''

def partClassification(img_bgr, show = False, isCurves = True,isMoving = False):    

    # Prepare the position results to be used to save in csv
    resultsVision = {"0":{'QCPassed': False, 'reason' : 'No part found'},
                "1":{'QCPassed': False, 'reason' : 'No part found'},
                "2":{'QCPassed': False, 'reason' : 'No part found'},
                "3":{'QCPassed': False, 'reason' : 'No part found'},
                "4":{'QCPassed': False, 'reason' : 'No part found'},
                "5":{'QCPassed': False, 'reason' : 'No part found'},
                "6":{'QCPassed': False, 'reason' : 'No part found'},
                "7":{'QCPassed': False, 'reason' : 'No part found'},
                "8":{'QCPassed': False, 'reason' : 'No part found'},
                "9":{'QCPassed': False, 'reason' : 'No part found'},
                "10":{'QCPassed': False, 'reason' : 'No part found'},
                "11":{'QCPassed': False, 'reason' : 'No part found'}}

    # Prepare the position results to be sent to plc
    resultsPLC = {"0":False,
                "1":False,
                "2":False,
                "3":False,
                "4":False,
                "5":False,
                "6":False,
                "7":False,
                "8":False,
                "9":False,
                "10":False,
                "11":False}

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
    parts = thresholding.otsuThresholding(img_gray, isCurved = isCurves,isMoving = isMoving)
    
    # Sort parts by position in the grid (Top left to right)
    parts.sort(key=lambda x: x.centreXY[0], reverse=False)
    parts.sort(key=lambda x: x.centreXY[1], reverse=False)

    # Iterate through the list of parts
    for j, piece in enumerate(parts):

        # This code finds the part index within the results grid dictionary to be marked as good 
        resultIndex = 0
        PLCIndex = 0
        # This variable is used to capture any contours we may have accidentally captured on the edge of the image
        validPart = True
        
        # Find the correct index the piece corresponds to (PLC indexes columns then rows)
        if(piece.centreXY[0]/imageWidth < 0.05):
            validPart = False

        elif(piece.centreXY[0]/imageWidth < 0.33):
            # print('x1')
            resultIndex += 0
            PLCIndex += 0
        
        elif(piece.centreXY[0]/imageWidth < 0.66):
            # print('x2')
            resultIndex += 1
            PLCIndex += 4
        
        elif(piece.centreXY[0]/imageWidth < 0.95):
            # print('x3')
            resultIndex += 2
            PLCIndex += 8
        else:
            validPart = False

        if(piece.centreXY[1]/imageHeight < 0.05):
            validPart = False

        elif(piece.centreXY[1]/imageHeight < 0.25):
            # print('y1')
            resultIndex += 0
            PLCIndex += 0
        
        elif(piece.centreXY[1]/imageHeight < 0.5):
            # print('y2')
            resultIndex += 3
            PLCIndex += 1

        elif(piece.centreXY[1]/imageHeight < 0.75):
            # print('y3')
            resultIndex += 6
            PLCIndex += 2
        
        elif(piece.centreXY[1]/imageHeight < 0.95):
            # print('y4')
            resultIndex += 9
            PLCIndex += 3
        else:
            validPart = False

        if(validPart):
            # The object is automatically QC checked on initialisation
            # Mark the QC result on the output dictionary
            resultsVision[str(resultIndex)]["QCPassed"] = piece.isQCPassed
            resultsVision[str(resultIndex)]["reason"] = piece.reasonForFailure
            resultsPLC[str(PLCIndex)] = piece.isQCPassed
        else:
            resultIndex = 'N/A'

        # Plot the contours, part number, and centre point
        cv2.drawContours(img_rgb, [piece.contour], -1, (0,0,255), 2)
        cv2.drawContours(img_rgb,piece.childContours,-1,(0,0,255), 1)
        # TODO: edit this to just show the part number after debugging
        cv2.putText(img_rgb ,"{0} - {1}".format(resultIndex,piece.reasonForFailure),piece.centreXYText,cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,255,0),1,cv2.LINE_AA) 
        cv2.circle(img_rgb,piece.centreXY, 3, (255,0,0), -1)
        # Get the bounding rectangle to be plotted after we have identified the part as good or bad
        rect = cv2.minAreaRect(piece.contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)


        if piece.isQCPassed:
            cv2.drawContours(img_rgb,[box],0,(0,255,0),1)
            passedCount += 1
            # This is for debugging
            print('Part {3}, Aspect Ratio {0}, Solidity {1}, Area/Perimeter {2}, Reason {4}'.format(piece.aspectRatio,piece.solidity,piece.areaPerimeterSqr,resultIndex,piece.reasonForFailure))
        
        elif(validPart):
            cv2.drawContours(img_rgb,[box],0,(255,0,0),1)
            failedCount += 1
            # This is for debugging
            print('Part {3}, Aspect Ratio {0}, Solidity {1}, Area/Perimeter {2}, Reason {4}'.format(piece.aspectRatio,piece.solidity,piece.areaPerimeterSqr,resultIndex,piece.reasonForFailure))
        
        # Only use this line for debugging
            #if(piece.reasonForFailure == "Unknown Failure Reason"): show = True

    # Show resuts
    if(show):
        plt.figure(figsize = (7,7))
        plt.title('Count: {0} - {1} Passed - {2} Failed'.format(len(parts),passedCount,failedCount))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()

    # Send back the classified image to also save for assessment
    img_classified = cv2.cvtColor(img_rgb,cv2.COLOR_RGB2BGR)

    return resultsVision, resultsPLC, img_classified