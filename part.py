from cv2 import cv2
import numpy as np

# Want to use this class to initiate objects that can be added to a list and identified 
class Part:

    name = 'unnamed'
    isIdentified = False
    isQCPassed = False
    colour = "colourless"
    childContours = []


    def __init__(self, contour):
        self.contour = contour 


    @property
    def centreXY(self):
        M = cv2.moments(self.contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return (cx,cy)
    

    # This method creates a bounding rectangle, however it isn't isn't orientated with the object
    # @property
    # def aspectRatio(self):
    #     x,y,w,h = cv2.boundingRect(self.contour)
    #     aspect_ratio = round(float(w)/h, 2)
    #     return aspect_ratio

    
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

