import numpy as np 
from cv2 import cv2
from matplotlib import pyplot as plt

# These functions need to take a grey image

# Have LPF and HPF
# LPF is used to remove noise or to blur the image
# HPF is used for finding edges in an image

#Guassian filters are good for removing noise, however they also remove edges



def smoothing(img):

    # Kernal size is the matrix size that you want you apply to the central pixel
    # ksize=5
    ksize = 3

    print(img.shape)

    w = img.shape[0]
    h = img.shape[1]

    # (3)blur,gaussian_blur,median

    img_blur = cv2.blur(img,(ksize,ksize))
    img_gaussian = cv2.GaussianBlur(img,(ksize,ksize),0)
    img_median = cv2.medianBlur(img,ksize)
    # img_bilateral = cv2.bilateralFilter(img,5,15,15)

    # plt.imshow(img_bilateral)
    # plt.show()

    # # (4)display
    img_up = np.concatenate((img, img_blur), axis=1)
    img_down = np.concatenate((img_gaussian, img_median), axis=1)
    img_all = np.concatenate((img_up, img_down), axis=0)


    plt.figure(figsize = (5,5))
    plt.imshow(img_all,'gray')
    plt.text(w, h, "blur",fontsize=40)
    plt.text(0, h*2, "gaussian",fontsize=40)
    plt.text(w, h*2, "median",fontsize=40)
    plt.axis('off')
    plt.show()