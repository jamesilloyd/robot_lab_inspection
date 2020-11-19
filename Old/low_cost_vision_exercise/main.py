#!/usr/bin/env python
# coding: utf-8

# #Exercise: Automated Visual Inspection 

# Zhengyang Ling ZL461@cam.ac.uk

import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import random 
import math
import colorFiltering
import smoothing
import feature_extraction
import thresholding
import contouring
from part import Part

# mean brightness is 202.1570612244898


def main():
    imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/JamesTutorials/low_cost_vision_exercise/example2.png'
    img_bgr = cv2.imread(imageLocation)

    # knn = cv2.ml.KNearest_create()
    originalCode(img_bgr)




def showImageSection(y,h,x,w,img):
    img_roi = img[y:y+h,x:x+w]
    plt.imshow(img_roi,'section')
    plt.show()


def ZhengyangContourSolution(img_bgr, show = True):

    # Change color space
    img_grey = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    if(show):
        plt.imshow(img_grey,'gray')
        plt.show()

    # Apply blur to remove noise
    ksize = 3
    img_gausBlur = cv2.GaussianBlur(img_grey,(ksize,ksize),0)

    if(show):
        plt.imshow(img_gausBlur,'gray')
        plt.show()

    # Apply thresholding to find 
    img_thresh = cv2.adaptiveThreshold(img_gausBlur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,127,11)

    if(show): cv2.imshow('Adaptive Gaus Threshold', img_thresh)

    # He doesn't choose to actually apply any morphological transformations
    
    # Find contours
    contours, hierarchy = cv2.findContours(img_thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # (3)display
    count = 0
    contour_filter = []
    img_contour = img_rgb.copy()
    for i, contour in enumerate(contours):
        if hierarchy[0][i][3] == 0:
            count += 1
            cv2.drawContours(img_contour, [contour], -1, (0,0,255), 2)  
            contour_filter.append(contour)


    if(show):
        print(count)

        plt.figure(figsize = (5,5))
        plt.imshow(img_contour)
        plt.axis('off')
        plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return contour_filter


def originalCode(img_bgr):
    ds=5

    #Change colours
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    plt.imshow(img_grey)
    plt.show()


    # DONE
    # (4)color filter
    lower = np.array([36,25,25])
    upper = np.array([70,255,255])
    img_color = cv2.inRange(img_hsv, lower, upper)

    f, axarr = plt.subplots(1,2)
    axarr[0].imshow(img_rgb)
    axarr[1].imshow(img_color)
    plt.show()

    #Image Pre-Process: Smoothing
    #Image Pre-Process: Smoothing
    #(1)region of image
    y1=140
    h=150
    x1=10
    w=40
    img_roi=img_grey[y1:y1+h,x1:x1+w]
    plt.imshow(img_roi,'gray')
    plt.show()


    # (2)filter size 

    # ksize=5
    ksize = 3


    # (3)blur,gaussian_blur,median

    img_blur = cv2.blur(img_roi,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(img_roi,(ksize,ksize),0)
    img_median = cv2.medianBlur(img_roi,ksize)

    # (4)display
    img_up = np.concatenate((img_roi, img_blur), axis=1)
    img_down = np.concatenate((img_gaussian, img_median), axis=1)
    img_all = np.concatenate((img_up, img_down), axis=0)
    plt.figure(figsize = (ds,ds))
    plt.imshow(img_all,'gray')
    plt.text(w, h, "blur",fontsize=40)
    plt.text(0, h*2, "gaussian",fontsize=40)
    plt.text(w, h*2, "median",fontsize=40)
    plt.axis('off')
    plt.show()

    img_pro = cv2.GaussianBlur(img_grey,(ksize,ksize),0)


    # #Image Pre-Process: Thresholding

    # (1)global,adaptive,otsu 
    ret,img_global = cv2.threshold(img_pro,100,255,cv2.THRESH_BINARY)
    img_adaptive = cv2.adaptiveThreshold(img_pro,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,127, 11)
    # img_adaptive = cv2.adaptiveThreshold(img_pro,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    ret2,img_otsu = cv2.threshold(img_pro,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


    # (2)display

    h,w=img_grey.shape
    img_up = np.concatenate((img_grey, img_global), axis=1)
    img_down = np.concatenate((img_adaptive, img_otsu), axis=1)
    img_all = np.concatenate((img_up, img_down), axis=0)
    plt.figure(figsize = (ds,ds))
    plt.imshow(img_all,'gray')
    plt.text(w, h, "global=100",fontsize=40)
    plt.text(0, h*2, "adaptive",fontsize=40)
    plt.text(w, h*2, "otsu",fontsize=40)
    plt.axis('off')
    plt.show()


    # img_pro=img_otsu.copy()
    img_pro= img_adaptive.copy()

    # #Image Pre-Process: Morphological Transformations

    # (1)region of image

    y1=140
    h=150
    x1=10
    w=40
    img_roi=img_pro[y1:y1+h,x1:x1+w]


    # (2)kernel size and iterative number

    ksize=3
    itern=2
    kernel = np.ones((ksize,ksize),np.uint8)


    # (3)erode,dilate,open

    img_erode = cv2.erode(img_roi,kernel,itern)
    img_dilate = cv2.dilate(img_roi,kernel,itern)
    img_open = cv2.morphologyEx(img_roi, cv2.MORPH_OPEN, kernel)


    # (4)display

    img_up = np.concatenate((img_roi, img_erode), axis=1)
    img_down = np.concatenate((img_dilate, img_open), axis=1)
    img_all = np.concatenate((img_up, img_down), axis=0)
    plt.figure(figsize = (ds,ds))
    plt.imshow(img_all,'gray')
    plt.text(w, h, "erode",fontsize=40)
    plt.text(0, h*2, "dilate",fontsize=40)
    plt.text(w, h*2, "open",fontsize=40)
    plt.axis('off')
    plt.show()



    img_pro=img_adaptive.copy()


    # #Segmentation: Contours

    # (1)contours calculation

    #TREE = hierarchical , LIST = all, EXTERNAL = external 
    #APPROX_NONE = returns all, APPROX_SIMPLE = compresses contours into two points on a line
    contours, hierarchy = cv2.findContours(img_pro,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )


    # (2)filter contours

    print('hierarchy',hierarchy)


    contour_filter=[]
    img_contour=img_rgb.copy()
    for i,contour in enumerate(contours):
        if hierarchy[0][i][3]==0:
            cv2.drawContours(img_contour, [contour], -1, (0,0,255), 2)  
            # THIS IS THE MAIN LIST THAT STORES THE OBJECTS
            contour_filter.append(contour)


    # (3)display
    plt.figure(figsize = (ds,ds))
    plt.imshow(img_contour)
    plt.axis('off')
    plt.show()



    # #Feature Extraction
    # Using a contour you can get the centre, area, perimeter

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
        img = cv2.rectangle(img_feature,(x,y),(x+w,y+h),(0,255,0),2)
        img = cv2.putText(img_feature ,"aspect_ratio: "+str(aspect_ratio),(cx-50,cy+35),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 

        #The area of an object
        area = cv2.contourArea(contour)
        img = cv2.putText(img_feature ,"area: "+str(int(area)),(cx-50,cy+25),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 

        #The perimeter of an object
        perimeter = cv2.arcLength(contour,True)
        img = cv2.putText(img_feature ,"perimeter: "+str(int(perimeter)),(cx-50,cy+15),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 
        img = cv2.putText(img_feature ,"number: "+str(i),(cx-50,cy+5),cv2.FONT_HERSHEY_SIMPLEX ,0.3,(0,0,255),1,cv2.LINE_AA) 

        area_list.append(area)
        aspect_ratio_list.append(aspect_ratio)



    plt.figure(figsize = (ds,ds))
    plt.imshow(img_feature)
    plt.axis('off')
    plt.show()


    # #Classification:train model

    # (1)tag the data

    # How do we make this tag array ?
    tag=['wheel','axle','disk','axle','wheel','flag','wheel','chasis','wheel']
    tag_color={'wheel':'m','axle':'c','disk':'y','chasis':'g','flag':'r'}
    tag_number={'wheel':'0','axle':'1','disk':'2','chasis':'3','flag':'4'}
    number_tag={'0':'wheel','1':'axle','2':'disk','3':'chasis','4':'flag'}

    newcomer_area=2000
    newcomer_aspect_ratio=1.5
    newcomer=[newcomer_area,newcomer_aspect_ratio]


    # (2)plot features space
    plt.figure(figsize = (ds,ds))

    for i,t in enumerate(tag):
        plt.scatter(area_list[i],aspect_ratio_list[i],marker='o',color=tag_color[tag[i]])
        plt.text(area_list[i],aspect_ratio_list[i],t, fontsize=20)

        plt.xlabel('area',fontsize=40)
        plt.ylabel('aspect_ratio',fontsize=40)
        
        
    plt.scatter(newcomer[0],newcomer[1],marker='*',s=1000,color='r')
    plt.text(newcomer[0],newcomer[1],'an unknown part?', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.show()  


    # (3)normalize 
    trainData_x_norm = [float(i)/max(area_list) for i in area_list]
    trainData_y_norm = [float(i)/max(aspect_ratio_list) for i in aspect_ratio_list]
    newcomer=[newcomer[0]/max(area_list),newcomer[1]/max(aspect_ratio_list)]

    # (2)plot features space
    plt.figure(figsize = (ds,ds))

    for i,t in enumerate(tag):
        plt.scatter(trainData_x_norm[i],trainData_y_norm[i],marker='o',color=tag_color[tag[i]])
        plt.text(trainData_x_norm[i],trainData_y_norm[i],t, fontsize=20)

        plt.xlabel('area',fontsize=40)
        plt.ylabel('aspect_ratio',fontsize=40)
        
        
    plt.scatter(newcomer[0],newcomer[1],marker='*',s=1000,color='r')
    plt.text(newcomer[0],newcomer[1],'an unknown part?', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.show()  


    # #Classification: prediction

    # (1)Load data
    f=open('/Users/heisenberg/RobotLab/robot_lab_inspection/JamesTutorials/low_cost_vision_exercise/train_model.txt',"r")
    lines=f.readlines()

    trainData_x=[]
    trainData_y=[]
    respones=[]

    for x in lines:
        x=x.strip("\n")
        trainData_x.append(float(x.split(' ')[0]))
        trainData_y.append(float(x.split(' ')[1]))
        respones.append(x.split(' ')[2])
            
    f.close()



    plt.figure(figsize = (ds,ds))

    for i in range(len(trainData_x)):    
        num=str(int(float(respones[i])))
        plt.scatter(trainData_x[i],trainData_y[i],marker='o',color=tag_color[number_tag[num]])

    plt.xlabel('area',fontsize=40)
    plt.ylabel('aspect_ratio',fontsize=40)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.show() 


    # (2)train model

    trainData=[ [trainData_x[i],trainData_y[i]] for i in range(len(trainData_x))]
    train_arr = np.array(trainData).astype('float32')
    respones_arr = np.array(respones).astype('float32')


    # Exciting stuff here, need to checkout how this works.
    knn=cv2.ml.KNearest_create()
    knn.train(train_arr,cv2.ml.ROW_SAMPLE,respones_arr)


    # (3)prediction
    parts_list=[]
    for i,contour in enumerate(contour_filter):

        M = cv2.moments(contour)
        # Get the centre of each contour
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        # Creates an array of the contour's normalised area and aspect ratio
        newcomer=[area_list[i]/max(area_list),aspect_ratio_list[i]/max(aspect_ratio_list)]   
        newcomer_arr = np.array([newcomer]).astype(np.float32)
        
        # Using the newcome it find's the nearest value using the trained knn
        # TODO: look at what format the results are in
        ret,results,neighbour,dist = knn.findNearest(newcomer_arr, 5)

        # Indexes the number tag array to assign the result back to a part value
        img_new = cv2.putText(img_rgb ,number_tag[str(int(results[0][0]))],(cx+12,cy-12),cv2.FONT_HERSHEY_SIMPLEX ,0.5,(0,0,255),1,cv2.LINE_AA) 
        parts_list.append(number_tag[str(int(results[0][0]))])

    plt.figure(figsize = (ds,ds))
    plt.imshow(img_new)
    plt.axis('off')
    plt.show()  


    #Post-process
    count={'wheel':0,'axle':0,'disk':0,'flag':0,'chasis':0}
    for part in parts_list:
        count[part]=count[part]+1


    print('result',count)
    print('Pass!')


if __name__ == '__main__':
    main()