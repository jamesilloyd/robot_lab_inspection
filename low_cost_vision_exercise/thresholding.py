from cv2 import cv2
import numpy as np 
from matplotlib import pyplot as plt



# This function needs to take a blurred / smoothed image
def simpleThresholding(img_gray):
    #want to first put a blur on it
    # img = cv2.medianBlur(img_bgr,5)
    
    threshold = 127
    maxValue = 255


    ret, thresh1 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(img_gray,threshold,maxValue,cv2.THRESH_TOZERO_INV)


    titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [img_gray, thresh1, thresh2, thresh3, thresh4, thresh5]

    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()




def adaptiveThresholding(img_gray):


    ksize = 5
    img_blur = cv2.blur(img_gray,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
    img_median = cv2.medianBlur(img_gray,ksize)

    # Adaptive thesholding
    # Penultimate variable is the size of the matrix to create the adaptive thresh mean / guas
    # Choosing between gaussian and median will vary between image types, need to play around with them
    blockSize = 127
    constant = 11

    # Trialling different blurs and adaptive types

    # thresh1 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # thresh3 = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh4 = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # thresh5 = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh6 = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # thresh7 = cv2.adaptiveThreshold(img_median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize,constant)
    # thresh8 = cv2.adaptiveThreshold(img_median, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize,constant)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows() 


    # titles = ['Original Image','Mean_bin','Gaus_bin']
    # images = [img_gray, thresh1, thresh2]

    # for i in range(len(images)):
    #     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])

    # plt.show()


    # Using an iterative approach to identify which block size and constant that contours the correct number of objects
    for i in range(150):
        
        if((i % 2 == 1) and (i > 1)):
            
            for j in range(30):
                
                # Trial with different blur types
                thresh = cv2.adaptiveThreshold(img_gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,i,j)
                # cv2.imshow('{0}_{1}'.format(i,j),thresh)

                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                contour_filter=[]
                count = 0
                img_contour= cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
                for k,contour in enumerate(contours):
                    if hierarchy[0][k][3]==0:
                        count += 1
                        cv2.drawContours(img_contour, [contour], -1, (0,0,255), 2)  
                        contour_filter.append(contour)

                # if count == 12 or count == 13:
                print(count)
                if count < 10 and count > 3 :
                    print('blocksize {0} and constant {1}'.format(i,j))

                    cv2.drawContours(img_contour, contours, -1, (0,0,255), 1)

                    plt.figure(figsize = (5,5))
                    plt.imshow(img_contour)
                    plt.axis('off')
                    plt.show()


    


# Otsu doesn't work for this image type
def otsuThresholding(img):
    

    # global thresholding
    ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    # Otsu's thresholding
    ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # plot all the idmages and their histograms
    images = [img, 0, th1,
            img, 0, th2,
            blur, 0, th3]
    titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
            'Original Noisy Image','Histogram',"Otsu's Thresholding",
            'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]

    for i in range(3):
        plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
        plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
        plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
        plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
    plt.show()
