from cv2 import cv2
import numpy as np

# Want to use this class to initiate objects that can be added to a list and identified 
class Part:

    # Initialise parameters that don't need to be passed on init
    name = 'unnamed'
    isIdentified = False
    isQCPassed = False
    colour = "colourless"
    childContours = []


    # Choose the correct ranges depending on whether the function is called for straight or curved pieces
    # if isCurves:
    #     # Curved piece classification ranges
    #     aspectRatioRange = [0.43,0.47]
    #     solidityRange = [0.8,0.94]
    #     areaPerimeterRange = [16.2,17.1]

    # else:
    #     # Straight piece classification ranges
    #     aspectRatioRange = [0.52,0.57]
    #     solidityRange = [0.80,0.85]
    #     areaPerimeterRange = [13.6,14.5]


    def __init__(self, contour, isCurvePiece):
        self.contour = contour 


    @property
    def centreXY(self):
        M = cv2.moments(self.contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return (cx,cy)

    @property
    def centreXYText(self):
        M = cv2.moments(self.contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return (cx + 10,cy)
    
    
    # This method uses a rotated rectange that is more in line with the object's actual shape
    @property 
    def aspectRatio(self):
        # rect[0] = top-left corner
        # rect[1] = (width, height)
        # rect[2] = angle of rotation
        # Below is used for mapping the box
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        rect = cv2.minAreaRect(self.contour)
        (x,y), (width, height), angle = rect
        return min(width,height) / max(width,height)


    @property
    def angleOfRotation(self):
        rect = cv2.minAreaRect(self.contour)
        return round(rect[2],2)


    @property
    def area(self):
        # Remove any child contour area from the parent contour
        negativeArea = 0
        if self.childContours:
            for i in range(len(self.childContours)):
                negativeArea += cv2.contourArea(self.childContours[i])

        return cv2.contourArea(self.contour) - negativeArea 


    @property
    def extent(self):
        # Ratio of contour area to bounding rectangle area
        rect = cv2.minAreaRect(self.contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        boxArea = cv2.contourArea(box)
        return self.area / boxArea

    

    @property 
    def solidity(self):
        # Ratio of contour area to it's convex hull area
        hull = cv2.convexHull(self.contour)
        hullArea = cv2.contourArea(hull)
        return float(self.area)/hullArea

    @property
    def perimeter(self):
        outerPerimeter = cv2.arcLength(self.contour,True)
        innerPerimeter = 0
        if self.childContours:
            for i in range(len(self.childContours)):
                innerPerimeter += cv2.arcLength(self.childContours[i],True)

        return innerPerimeter + outerPerimeter

