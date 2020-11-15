import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt

def main():
    loadColorImageInMatPlotLib()

    
def loadGreyImageInMatPlotLib():
    img = cv2.imread('image.jpeg',0)

    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)

    cv2.imshow('image',img)
    k = cv2.waitKey(0) & 0xFF
        
    if k == 27:
        cv2.destroyAllWindows()
    if k == ord('s'):
        cv2.imwrite('imageGrey.png',img)
        cv2.destroyAllWindows()

    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.show()


# Extra steps are needed to display an image in color mode
def loadColorImageInMatPlotLib():
    img = cv2.imread('image.jpeg')

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img2 = img[:,:,::-1] # Flip the color dimensions form BGR to RGB
    plt.subplot(121);plt.imshow(img) # expects distorted color
    plt.subplot(122);plt.imshow(img2) # expect true color
    plt.show()

    cv2.imshow('bgr image',img) # expects true color
    cv2.imshow('rgb image',img2) # expects distorted color
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    



# def easyLoadVideo():
#     capture = cv2.VideoCapture('video.mov')

#     while True:
#         isTrue, frame = capture.read()
#         cv2.imshow('Video',frame)

#         if cv2.waitKey(20) & 0xFF == ord('d'):
#             break 

#     capture.release()
#     cv2.destroyAllWindows()






if __name__ == "__main__":
    main()
