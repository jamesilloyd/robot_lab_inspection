import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import thresholding
import part


for i in range(44):

    imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/Corners/4/opencv_frame_{0}.png'.format(i)
    img_bgr = cv2.imread(imageLocation)

    # ADD IN THE RIGHT CROPPED DIMENSIONS 
    y1 = 45
    x1 = 34

    y2 = 434
    x2 = 614

    # y1 = 40
    # x1 = 80

    # y2 = 420
    # x2 = 590

    img_bgr = img_bgr[y1:y2,x1:x2]

    img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)

    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    parts = thresholding.otsuThresholding(img_gray)

    print(len(parts))

    for i, piece in enumerate(parts):
        # print(piece.centreXY)
        # print(piece.area)
        print()
        cv2.drawContours(img_rgb, [piece.contour], -1, (0,0,255), 2)
        cv2.drawContours(img_rgb,piece.childContours,-1,(0,0,255), 1)
        img = cv2.circle(img_rgb,piece.centreXY, 3, (255,0,0), -1)
        rect = cv2.minAreaRect(piece.contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # print(piece.area / piece.perimeter)
        if(piece.area > 9050 and piece.area < 9350):
            img = cv2.drawContours(img_rgb,[box],0,(0,255,0),1)
        else:
            img = cv2.drawContours(img_rgb,[box],0,(255,0,0),1)

    plt.figure(figsize = (7,7))
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.show()

