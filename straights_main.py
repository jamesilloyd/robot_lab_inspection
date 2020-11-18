import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import thresholding
import part
from mpl_toolkits.mplot3d import Axes3D

# TODO: finish writing code to send back results.


total_part_number = 0

correct_part_tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1]

# fig = plt.figure()
# ax = Axes3D(fig)

aspectRatioRange = [0.5396824839373978, 0.5612188032263316]
solidityRange = [0.8258002560819462, 0.8425492651420287]
areaPerimeterRange = [13.984231658690996, 14.375006235699498]
show = True



for i in range(36):

    imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Data/Straight/group4/opencv_frame_{0}.png'.format(i)
    img_bgr = cv2.imread(imageLocation)
    
    
    # ADD IN THE RIGHT CROPPED DIMENSIONS 
    y1 = 40
    x1 = 80

    y2 = 420
    x2 = 590

    img_bgr = img_bgr[y1:y2,x1:x2]

    img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)

    imageHeight , imageWidth = img_bgr.shape[:2]

    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    parts = thresholding.otsuThresholding(img_gray)

    # Sort parts by position in the grid (Top left to right)
    parts.sort(key=lambda x: x.centreXY[0], reverse=False)
    parts.sort(key=lambda x: x.centreXY[1], reverse=False)

    for j, piece in enumerate(parts):

        if total_part_number == 154 or total_part_number == 374:
            print(piece.area)
            print(piece.area/piece.perimeter)
            print(piece.solidity)
            print(piece.aspectRatio)
        
        if show:
            cv2.drawContours(img_rgb, [piece.contour], -1, (0,0,255), 2)
            cv2.drawContours(img_rgb,piece.childContours,-1,(0,0,255), 1)
            img = cv2.putText(img_rgb ,str(total_part_number),piece.centreXY,cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 
            
            img = cv2.circle(img_rgb,piece.centreXY, 3, (255,0,0), -1)
            rect = cv2.minAreaRect(piece.contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

        # Classifying using parameters
        if(piece.aspectRatio > 0.52 and piece.aspectRatio < 0.57 and piece.solidity > 0.80 and piece.solidity < 0.85 and piece.area / piece.perimeter > 13.6 and piece.area / piece.perimeter < 14.5):
            if show: img = cv2.drawContours(img_rgb,[box],0,(0,255,0),1)

        else:
            if show: img = cv2.drawContours(img_rgb,[box],0,(255,0,0),1)

        total_part_number += 1

    if show:
        plt.figure(figsize = (7,7))
        plt.title('Count: {0} Image: {1}'.format(len(parts),i))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()