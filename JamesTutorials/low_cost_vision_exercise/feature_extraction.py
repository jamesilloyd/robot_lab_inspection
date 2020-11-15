
from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt 



def featureExtraction(img_rgb,contour_filter):

    area_list=[]
    aspect_ratio_list=[]

    img_feature=img_rgb.copy()
    for i,contour in enumerate(contour_filter):
        #center of an object
        M = cv2.moments(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        # Put a red dot on the image to represent the centre of mass
        img = cv2.circle(img_feature,(cx,cy), 3, (255,0,0), -1)
        
        #The aspect ratio, which is the width divided by the height of the bounding rectangle
        x,y,w,h = cv2.boundingRect(contour)
        aspect_ratio = round(float(w)/h, 2)
        img = cv2.rectangle(img_feature,(x,y),(x+w,y+h),(0,255,0),1)
        img = cv2.putText(img_feature ,"aspect_ratio: "+str(aspect_ratio),(cx-50,cy+35),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 

        #The area of an object
        area = cv2.contourArea(contour)
        img = cv2.putText(img_feature ,"area: "+str(int(area)),(cx-50,cy+25),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 

        #The perimeter of an object
        perimeter = cv2.arcLength(contour,True)
        img = cv2.putText(img_feature ,"perimeter: "+str(int(perimeter)),(cx-50,cy+15),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 
        img = cv2.putText(img_feature ,"number: "+str(i),(cx-50,cy+5),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 


        # Can also create a rotated rectangle (more accurate to the actual area of the object)
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        img = cv2.drawContours(img_feature,[box],0,(0,0,255),1)

        # Can also apply other shapes as well
        # Regardless, the information is generated from the contour not the shape you put around it

        area_list.append(area)
        aspect_ratio_list.append(aspect_ratio)



    plt.figure(figsize = (5,5))
    plt.imshow(img_feature)
    plt.axis('off')
    plt.show()