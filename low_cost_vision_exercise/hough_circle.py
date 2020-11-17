from cv2 import cv2
import numpy as np

imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/JamesTutorials/low_cost_vision_exercise/example2.png'
img = cv2.imread(imageLocation,0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# Need to play around with these parameters
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,
                            param1=400,param2=50,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()