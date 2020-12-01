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
        if(self.aspectRatioRange[0] < self.aspectRatio < self.aspectRatioRange[1] and self.solidityRange[0] < self.solidity < self.solidityRange[1] and self.areaPerimeterRange[0] < self.areaPerimeterSqr < self.areaPerimeterRange[1]):
            return True
        else:
            return False

    @property
    def reasonForFailure(self):
        if(self.isQCPassed):
            return ""
        else:
            return "Unknown Failure Reason"
            # return "QC Failed"
            

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
    def areaPerimeterSqr(self):
        return self.area / (self.perimeter ** 2)

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
    # areaPerimeterRange = [13.6,14.5]
    areaPerimeterRange = [0.028,0.032]

    # These are the ranges of the defect part types 
    holeInMiddle = Defect([0.52,0.56],[0.76,0.80],[0.019,0.023],"Hole in the middle")
    filledHole = Defect([0.53,0.565],[0.89,0.91],[0.037,0.047],"The hole is filled")
    onlyNotch = Defect([0.64,0.74],[0.91,0.93],[0.053,0.06],"Notch on its own")
    missingNotchHoleFilled = Defect([0.7,0.74],[0.96,1.0],[0.057,0.061],"Notch is missing and hole is filled")
    missingNotch = Defect([0.71,0.74],[0.88,0.92],[0.037,0.05],"Notch is missing")
    halfWidthWithHoleFilled = Defect([0.77,0.79],[0.96,0.99],[0.0540,0.0570],"Half split by width with hole filled")
    halfWidthWithHole = Defect([0.75,0.84],[0.82,0.88],[0.031,0.035],"Half split by width including hole")
    halfWidthWithNotch = Defect([0.93,0.99],[0.80,0.84],[0.038,0.042],"Half split by width including notch")


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
                if(reason.aspectRatio[0] < self.aspectRatio < reason.aspectRatio[1] and reason.solidity[0] < self.solidity < reason.solidity[1] and reason.areaPerimeter[0] < self.areaPerimeterSqr < reason.areaPerimeter[1]):
                    failureReason = reason.reason
                
            return failureReason
                

# TODO: CHECK IF ANY OF THE STRAIGHT PART AND CURVE PART DEFECT RANGES OVERLAP, IF NOT THEN YOU CAN PUT THEM TOGETHER
class CurvedPart(Part):

    # These are the ranges used to classify a good straight part
    aspectRatioRange = [0.43,0.47]
    solidityRange = [0.8,0.85]
    areaPerimeterRange = [0.027,0.031]

    
    # These are the ranges of the defect part types 
    halfLengthWithNotch = Defect([0.21,0.25],[0.75,0.79],[0.022,0.027],"Half split by length with notch")
    halfLengthWithoutNotch = Defect([0.22,0.27],[0.92,0.96],[0.033,0.037],"Half split by length without notch")
    holeInMiddle = Defect([0.43,0.47],[0.77,0.81],[0.021,0.024],"Hole in the middle")
    filledHole = Defect([0.43,0.48],[0.85,0.91],[0.029,0.041],"The hole is filled")
    
    missingNotchHoleFilled = Defect([0.48,0.52],[0.89,0.93],[0.037,0.051],"Notch is missing and hole is filled")
    missingNotch = Defect([0.48,0.51],[0.85,0.89],[0.033,0.037],"Notch is missing")
    straightPiece = Defect([0.52,0.57],[0.8,0.85],[0.028,0.032],"Straight piece")
    onlyNotch = Defect([0.62,0.74],[0.91,0.94],[0.053,0.06],"Notch on its own")
    
    halfWidthWithHoleFilled = Defect([0.77,0.90],[0.93,0.98],[0.041,0.060],"Half split by width with hole filled")
    halfWidthWithNotch = Defect([0.72,0.82],[0.82,0.87],[0.039,0.043],"Half split by width including notch")
    halfWidthWithHole = Defect([0.77,0.89],[0.82,0.89],[0.033,0.037],"Half split by width including hole")
    


    # List that contains all the defected parts
    failureReasons = [missingNotch,
                    halfWidthWithNotch,
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
                if(reason.aspectRatio[0] < self.aspectRatio < reason.aspectRatio[1] and reason.solidity[0] < self.solidity < reason.solidity[1] and reason.areaPerimeter[0] < self.areaPerimeterSqr < reason.areaPerimeter[1]):
                    failureReason = reason.reason
                
            return failureReason
                

# TBF
class MovingStraightPart(Part):

    aspectRatioRange = [0.48,0.55]
    solidityRange = [0.83,0.89]
    areaPerimeterRange = [0.031,0.037]


# TBF
class MovingCurvedPart(Part):

    aspectRatioRange = [0.41,0.45]
    solidityRange = [0.85,0.90]
    areaPerimeterRange = [0.030,0.036]


