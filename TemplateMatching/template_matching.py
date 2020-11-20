#import modules
# import cv2
from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

#read image and template

# imageLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/TemplateMatching/opencv_frame_24.png'
# templateLocation = '/Users/heisenberg/RobotLab/robot_lab_inspection/TemplateMatching/template_straight.png'
# img_bgr = cv2.imread(imageLocation)
# img_template = cv2.imread(templateLocation,0)
# img_bgr = cv2.imread('opencv_frame_24.png')
# img_template = cv2.imread('template_straight.png',0)


#template matching function returns list of matched locations
def templateMatching(img_bgr, img_template):

	img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
	img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

	temp_w, temp_h = img_template.shape[::-1]
	#print(temp_w, temp_h)

	temp_ratio = temp_w / temp_h
	if temp_ratio < 1.9:
		threshold = 0.9
	else:
		threshold = 0.95

	res = cv2.matchTemplate(img_gray,img_template,cv2.TM_CCOEFF_NORMED)
	#threshold = 0.95
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

	ds=7
	plt.figure(figsize = (ds,ds))
	plt.imshow(img_rgb)
	plt.title('Templates found')
	plt.axis('off')
	plt.show()

	return pt_list

#image cropping function crops image to matched template locations
# Returns the cropped image to be used by contouring
def imageCropping(img_bgr, img_template, match_list):

	temp_w, temp_h = img_template.shape[::-1]

	temp_ratio = temp_w / temp_h
	if temp_ratio < 1.9:
		total_temp_w = temp_w * 1.378
		total_temp_h = temp_h * 1.351
	else:
		total_temp_w = temp_w * 1.097
		total_temp_h = temp_h * 1.205

	x_list = []
	y_list = []
	for match in match_list:
		x_list.append(match[0])
		y_list.append(match[1])

	#print(x_list, y_list)

	x_min = min(x_list)
	y_min = min(y_list)
	x_max = max(x_list)
	y_max = max(y_list)

	#print(x_min, y_min, x_max, y_max)

	if x_min < 160:
		sub_x = 0
	elif x_min < 320:
		sub_x = 1
	else:
		sub_x = 2

	if y_min < 100:
		sub_y = 0
	elif y_min < 200:
		sub_y = 1
	elif y_min < 300:
		sub_y = 2
	else:
		sub_y = 3

	if x_max > 320:
		add_x = 0
	elif x_max > 160:
		add_x = 1
	else:
		add_x = 2

	if y_max > 300:
		add_y = 0
	elif y_max > 200:
		add_y = 1
	elif y_max > 100:
		add_y = 2
	else: 
		add_y = 3

	x_min = int(x_min - sub_x*total_temp_w - 5)
	y_min = int(y_min - sub_y*total_temp_h - 5)
	x_max = int(x_max + add_x*total_temp_w + temp_w + 5)
	y_max = int(y_max + add_y*total_temp_h + temp_h + 5)

	img_crop = img_bgr[y_min:y_max, x_min:x_max]

	# TODO: come back to this
	# cv2.imwrite('img_crop.png',img_crop)

	# Change from bgr to rgb for matplot lib
	img_crop_rgb = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)

	ds=7
	plt.figure(figsize = (ds,ds))
	plt.imshow(img_crop_rgb)
	plt.axis('off')
	plt.title('Cropped image')
	plt.show()

	# Return the cropped image to be used in the next function
	return img_crop