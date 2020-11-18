#import modules
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

#read image and template
img_bgr = cv2.imread('opencv_frame_24.png')
img_template = cv2.imread('template_straight.png',0)


#template matching function returns list of matched locations
def templateMatching(img_bgr, img_template):

	img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
	img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

	temp_w, temp_h = img_template.shape[::-1]
	#print(w, h)

	res = cv2.matchTemplate(img_gray,img_template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.95
	loc = np.where( res >= threshold)


	loc_arr = []
	for pt in zip(*loc[::-1]):
		loc_arr.append(pt)

	pt_list = [loc_arr[0]]
	for loc in loc_arr:
		dist_list = []
		for pt in pt_list:
			dist = math.hypot(loc[0] - pt[0], loc[1] - pt[1])
			dist_list.append(dist)
		dist_array = np.array(dist_list)
		if ((dist_array >= temp_h/2).sum() == dist_array.size).astype(np.int):
			pt_list.append(loc)

	#print(pt_list)

	for pt in pt_list:
		cv2.rectangle(img_rgb, pt, (pt[0] + temp_w, pt[1] + temp_h), (0,0,255), 2)

	ds=5
	plt.figure(figsize = (ds,ds))
	plt.imshow(img_rgb)
	plt.axis('off')
	plt.show()

	return pt_list, temp_w, temp_h

#image cropping function crops image to matched template locations
def imageCropping(img_bgr, match_list, temp_w, temp_h):

	x_list = []
	y_list = []
	for match in match_list:
		x_list.append(match[0])
		y_list.append(match[1])

	#print(x_list, y_list)

	x_min = min(x_list) - 5
	x_max = max(x_list) + temp_w + 5
	y_min = min(y_list) - 5
	y_max = max(y_list) + temp_h + 5

	img_crop = img_bgr[y_min:y_max, x_min:x_max]

	cv2.imwrite('img_crop.png',img_crop)

	ds=5
	plt.figure(figsize = (ds,ds))
	plt.imshow(img_crop)
	plt.axis('off')
	plt.show()


if __name__ == "__main__":

	match_list, temp_w, temp_h = templateMatching(img_bgr, img_template)

	print(match_list)

	imageCropping(img_bgr, match_list, temp_w, temp_h)