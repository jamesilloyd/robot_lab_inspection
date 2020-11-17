import cv2
import numpy as np
from matplotlib import pyplot as plt

#img_rgb = cv2.imread('opencv_frame_0.png')
img_bgr = cv2.imread('opencv_frame_33.png')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
template = cv2.imread('opencv_frame_temp.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.9
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    print(pt)

cv2.imwrite('res.png',img_rgb)

ds=5
plt.figure(figsize = (ds,ds))
plt.imshow(img_rgb)
plt.axis('off')
plt.show()