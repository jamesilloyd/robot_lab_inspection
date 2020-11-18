import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import thresholding
import part
from mpl_toolkits.mplot3d import Axes3D




total_part_number = 0

correct_part_tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1]

# fig = plt.figure()
# ax = Axes3D(fig)

aspectRatioRange = [0.5396824839373978, 0.5612188032263316]
solidityRange = [0.8258002560819462, 0.8425492651420287]
areaPerimeterRange = [13.984231658690996, 14.375006235699498]


for i in range(36):

    # imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/straights/opencv_frame_{0}.png'.format(i)
    imageLocation = '/Users/heisenberg/University of Cambridge/Taba Gibb - Track and Train/Inspection/Data/Straight/group4/opencv_frame_{0}.png'.format(i)
    img_bgr = cv2.imread(imageLocation)

    # ADD IN THE RIGHT CROPPED DIMENSIONS 
    y1 = 40
    x1 = 80

    y2 = 420
    x2 = 590

    img_bgr = img_bgr[y1:y2,x1:x2]

    

    show = False

    img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)

    imageHeight , imageWidth = img_bgr.shape[:2]

    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    parts = thresholding.otsuThresholding(img_gray)

    # Sort parts by position in the grid (Top left to right)
    parts.sort(key=lambda x: x.centreXY[0], reverse=False)
    parts.sort(key=lambda x: x.centreXY[1], reverse=False)

    for j, piece in enumerate(parts):
        
        if show:
            cv2.drawContours(img_rgb, [piece.contour], -1, (0,0,255), 2)
            cv2.drawContours(img_rgb,piece.childContours,-1,(0,0,255), 1)
            img = cv2.putText(img_rgb ,str(total_part_number),piece.centreXY,cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 
            
            img = cv2.circle(img_rgb,piece.centreXY, 3, (255,0,0), -1)
            rect = cv2.minAreaRect(piece.contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

        # Classifying using parameters
        # if(piece.solidity < 0.85 and piece.area > 6300):
        # if(piece.aspectRatio > 0.43 and piece.aspectRatio < 0.47 and piece.solidity > 0.80 and piece.solidity < 0.84 and piece.area / piece.perimeter > 16.2 and piece.area / piece.perimeter < 17.1):
        if correct_part_tags[total_part_number] == 1:
            if show: img = cv2.drawContours(img_rgb,[box],0,(0,255,0),1)
            # ax.scatter(piece.solidity, piece.aspectRatio,piece.area/piece.perimeter, c = 'g')

            if piece.solidity < solidityRange[0]:
                solidityRange[0] = piece.solidity
            if piece.solidity > solidityRange[1]:
                solidityRange[1] = piece.solidity

            if piece.aspectRatio < aspectRatioRange[0]:
                aspectRatioRange[0] = piece.aspectRatio
            if piece.aspectRatio > aspectRatioRange[1]:
                aspectRatioRange[1] = piece.aspectRatio

            if piece.area / piece.perimeter < areaPerimeterRange[0]:
                areaPerimeterRange[0] = piece.area / piece.perimeter
            if piece.area / piece.perimeter > areaPerimeterRange[1]:
                areaPerimeterRange[1] = piece.area / piece.perimeter
            

        else:
            if show: img = cv2.drawContours(img_rgb,[box],0,(255,0,0),1)
            # ax.scatter(piece.solidity, piece.aspectRatio,piece.area/piece.perimeter, c = 'r')

        total_part_number += 1

    if show:
        plt.figure(figsize = (7,7))
        plt.title('Count: {0} Image: {1}'.format(len(parts),i))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()


# Plot the data 3D
    
print(aspectRatioRange)
print(solidityRange)
print(areaPerimeterRange)
# plt.xlabel('Solidity'),plt.ylabel('Aspect Ratio')
# ax.set_zlabel('Area/Perim')
# plt.show()

    # Plot data 2D
    # plt.xlabel('Solidity',fontsize=40)
    # plt.ylabel('Extent',fontsize=40)
    # plt.xticks(fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.show()  




            # print(piece.perimeter)
            
            # # using labels to mark pieces as good or bad
            # if(correct_part_tags[total_part_number] == 1):
            #     img = cv2.drawContours(img_rgb,[box],0,(0,255,0),1)
            #     # plt.scatter(piece.solidity,piece.extent,marker ='o', c = 'g')
            #     ax.scatter(piece.solidity, piece.aspectRatio,piece.area/piece.perimeter, c = 'g')
            

            # else:
            #     img = cv2.drawContours(img_rgb,[box],0,(255,0,0),1)
            #     # plt.scatter(piece.solidity,piece.extent,marker ='o', c = 'r')
            #     ax.scatter(piece.solidity, piece.aspectRatio,piece.area/piece.perimeter, c = 'r')
            #     # if(piece.area > 8000):
            #     #     print('Image: {0} Part: {1}'.format(i,j))




