from cv2 import cv2
import numpy as np

# Want to use this class to initiate objects that can be added to a list and identified 
class Part:

    # Initialise parameters that don't need to be passed on init
    name = 'unnamed'
    colour = "colourless"
    childContours = []

    aspectRatioRange = []
    solidityRange = []
    areaPerimeterRange = []


    def __init__(self, contour):
        self.contour = contour 


    @property
    def isQCPassed(self):
        if(self.aspectRatio > self.aspectRatioRange[0] and self.aspectRatio < self.aspectRatioRange[1] and self.solidity > self.solidityRange[0] and self.solidity < self.solidityRange[1] and self.area / self.perimeter > self.areaPerimeterRange[0] and self.area / self.perimeter < self.areaPerimeterRange[1]):
            return True
        else:
            return False

    @property
    def reasonForFailure(self):
        reason = ""
        if(self.isQCPassed):
            return "QC Passed"
        else:
            return "QC Failed"
            

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

    # TODO may need to only take external perimeter
    @property
    def perimeter(self):
        outerPerimeter = cv2.arcLength(self.contour,True)
        innerPerimeter = 0
        if self.childContours:
            for i in range(len(self.childContours)):
                innerPerimeter += cv2.arcLength(self.childContours[i],True)

        return innerPerimeter + outerPerimeter



class Defect():

    def __init__(self, aspectRatio, solidity,areaPerimeter, reason):
        self.aspectRatio = aspectRatio
        self.solidity = solidity
        self.areaPerimeter = areaPerimeter
        self.reason = reason

    

class StraightPart(Part):

    # These are the ranges used to classify a good straight part
    aspectRatioRange = [0.52,0.57]
    solidityRange = [0.80,0.85]
    areaPerimeterRange = [13.6,14.5]

    # This needs testing more (see how much you can extend ranges so that they don't interfere), maybe add in a 4th dimension
    # These are the ranges of the defect part types 
    holeInMiddle = Defect([0.52,0.56],[0.76,0.80],[10.7,11.6],"Hole in the middle")
    filledHole = Defect([0.53,0.565],[0.89,0.91],[16.5,18.1],"The hole is filled")
    onlyNotch = Defect([0.64,0.72],[0.91,0.93],[4.7,5.1],"Notch on it's own")
    missingNotchHoleFilled = Defect([0.7,0.74],[0.96,1.0],[18.8,20.2],"Notch is missing and hole is filled")
    missingNotch = Defect([0.71,0.73],[0.88,0.92],[14.8,15.7],"Notch is missing")
    halfWidthWithHoleFilled = Defect([0.77,0.79],[0.97,0.99],[14.2,14.9],"Half split by width with hole filled")
    halfWidthWithHole = Defect([0.77,0.84],[0.82,0.88],[10.0,10.7],"Half split by width including hole")
    halfWidthWithNotch = Defect([0.93,0.99],[0.80,0.84],[11.3,11.8],"Half split by width including notch")


    # List that contains all the defect types
    failureReasons = [missingNotch,
                    halfWidthWithNotch,
                    halfWidthWithHole,
                    filledHole,

                    onlyNotch,
                    halfWidthWithHoleFilled,
                    holeInMiddle,
                    missingNotchHoleFilled
                    ]
    


    # Assign a reason for failure if the part did not pass QC
    @property
    def reasonForFailure(self):
        failureReason = "Unknown Failure Reason"
        if(self.isQCPassed):
            return ""
        else:
            for i,reason in enumerate(self.failureReasons):
                # TODO: may need a more robust threshold
                if(reason.aspectRatio[0] < self.aspectRatio < reason.aspectRatio[1] and reason.solidity[0] < self.solidity < reason.solidity[1] and reason.areaPerimeter[0] < self.area/self.perimeter < reason.areaPerimeter[1]):
                    failureReason = reason.reason
                
            return failureReason
                


class CurvedPart(Part):

    # These are the ranges used to classify a good straight part
    aspectRatioRange = [0.43,0.47]
    solidityRange = [0.8,0.85]
    areaPerimeterRange = [16.2,17.1]

    
    # These are the ranges of the defect part types 
    halfLengthWithNotch = Defect([0.21,0.25],[0.75,0.78],[9.8,10.5],"Half split by length with notch")
    halfLengthWithoutNotch = Defect([0.22,0.27],[0.92,0.96],[13.1,13.6],"Half split by length without notch")
    holeInMiddleWithHoleFilled = Defect([0.42,0.47],[0.80,0.85],[15.3,15.9],"Hole in the middle and other hole filled")
    holeInMiddle = Defect([0.43,0.47],[0.77,0.81],[13.8,14.2],"Hole in the middle")
    filledHole = Defect([0.43,0.48],[0.85,0.91],[16.5,19.8],"The hole is filled")
    
    missingNotchHoleFilled = Defect([0.48,0.52],[0.89,0.93],[18.5,21.2],"Notch is missing and hole is filled")
    missingNotch = Defect([0.48,0.51],[0.85,0.89],[17.8,18.3],"Notch is missing")
    straightPiece = Defect([0.52,0.57],[0.8,0.85],[13.3,14.5],"Straight piece")
    onlyNotch = Defect([0.61,0.73],[0.91,0.93],[4.4,5.1],"Notch on it's own")
    
    halfWidthWithHoleFilled = Defect([0.77,0.81],[0.93,0.98],[14.1,14.9],"Half split by width with hole filled")
    halfWidthWithNotch = Defect([0.77,0.82],[0.82,0.87],[13.3,14.0],"Half split by width including notch")
    halfWidthWithHole = Defect([0.77,0.84],[0.82,0.89],[12.2,12.9],"Half split by width including hole")
    


    # List that contains all the defected parts
    failureReasons = [missingNotch,
                    halfWidthWithNotch,
                    holeInMiddleWithHoleFilled,
                    halfWidthWithHole,
                    filledHole,

                    onlyNotch,
                    holeInMiddle,
                    missingNotchHoleFilled,
                    straightPiece,
                    
                    halfWidthWithHoleFilled,
                    halfLengthWithNotch,
                    halfLengthWithoutNotch
                    ]

    # Assign a reason for failure if the part did not pass QC
    @property
    def reasonForFailure(self):
        failureReason = "Unknown Failure Reason"
        if(self.isQCPassed):
            return ""
        else:
            for i,reason in enumerate(self.failureReasons):
                # TODO: may need a more robust threshold
                if(reason.aspectRatio[0] < self.aspectRatio < reason.aspectRatio[1] and reason.solidity[0] < self.solidity < reason.solidity[1] and reason.areaPerimeter[0] < self.area/self.perimeter < reason.areaPerimeter[1]):
                    failureReason = reason.reason
                
            return failureReason
                

# TBF
class MovingStraightPart(Part):

    aspectRatioRange = [0.52,0.57]
    solidityRange = [0.80,0.85]
    areaPerimeterRange = [13.6,14.5]


# TBF
class MovingCurvedPart(Part):

    aspectRatioRange = [0.43,0.47]
    solidityRange = [0.8,0.94]
    areaPerimeterRange = [16.2,17.1]


