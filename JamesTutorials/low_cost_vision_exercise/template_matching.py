from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt 


imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/JamesTutorials/low_cost_vision_exercise/example2.png'
img_gray = cv2.imread(imageLocation,0)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


button_template = [][236:248,240:252]
flag_template = [][63:138,250:301]
lhObject_template = [][165:271,13:47]



def multipleTemplateMatch(img_gray, template):

    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

    
    for threshold in range(100):
        print(threshold/100)
        img = img_gray.copy()
        loc = np.where( res >= threshold/100)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        cv2.imshow('res.png',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



def singleTemplateMatch(img_gray, template):

    img2 = img_gray.copy()
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    # The best ones are NORMED and both SQDIFFs

    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()



