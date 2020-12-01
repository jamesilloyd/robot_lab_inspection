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
def templateMatching(img_bgr, img_template,show = False):

	foundTemplate = False

	# TODO: NEED TO ACCOUNT FOR A BLANK TRAY

	img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
	img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

	temp_h, temp_w = img_template.shape[:2]
	#print(temp_w, temp_h)

	temp_ratio = temp_w / temp_h
	if temp_ratio < 1.9:
		threshold = 0.9
	else:
		threshold = 0.9

	res = cv2.matchTemplate(img_gray,img_template,cv2.TM_CCOEFF_NORMED)
	#threshold = 0.95
	loc = np.where( res >= threshold)

	loc_arr = []
	pt_list = []
	
	for pt in zip(*loc[::-1]):
		loc_arr.append(pt)

	if(loc_arr == []):
		foundTemplate = False
	else:
		foundTemplate = True

	if(foundTemplate):

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

		if(show):
			for pt in pt_list:
				cv2.rectangle(img_rgb, pt, (pt[0] + temp_w, pt[1] + temp_h), (0,0,255), 2)

			ds=7
			plt.figure(figsize = (ds,ds))
			plt.imshow(img_rgb)
			plt.title('Templates found')
			plt.axis('off')
			plt.show()

	return pt_list , foundTemplate

#image cropping function crops image to matched template locations
# Returns the cropped image to be used by contouring
def imageCropping(img_bgr, img_template, match_list, show = False):

	temp_h, temp_w = img_template.shape[:2]
	img_h, img_w = img_bgr.shape[:2]

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

	if x_min < img_w*0.25:
		sub_x = 0
	elif x_min < img_w*0.5:
		sub_x = 1
	else:
		sub_x = 2

	if y_min < img_h*0.208:
		sub_y = 0
	elif y_min < img_h*0.417:
		sub_y = 1
	elif y_min < img_h*0.625:
		sub_y = 2
	else:
		sub_y = 3

	if x_max > img_w*0.5:
		add_x = 0
	elif x_max > img_w*0.25:
		add_x = 1
	else:
		add_x = 2

	if y_max > img_h*0.625:
		add_y = 0
	elif y_max > img_h*0.417:
		add_y = 1
	elif y_max > img_h*0.208:
		add_y = 2
	else: 
		add_y = 3

	x_min = int(x_min - sub_x*total_temp_w - 5)
	y_min = int(y_min - sub_y*total_temp_h - 5)
	x_max = int(x_max + add_x*total_temp_w + temp_w + 5)
	y_max = int(y_max + add_y*total_temp_h + temp_h + 5)

	#print(x_min, y_min, x_max, y_max)

	if x_min < 0:
		x_min = 0
	if y_min < 0:
		y_min = 0
	if x_max > img_w:
		x_max = img_w
	if y_max > img_h:
		y_max = img_h

	img_crop = img_bgr[y_min:y_max, x_min:x_max]

	# TODO: come back to this
	# cv2.imwrite('img_crop.png',img_crop)

	# Change from bgr to rgb for matplot lib
	img_crop_rgb = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)

	if(show):
		ds=7
		plt.figure(figsize = (ds,ds))
		plt.imshow(img_crop_rgb)
		plt.axis('off')
		plt.title('Cropped image')
		plt.show()

	# Return the cropped image to be used in the next function
	return img_crop

"""
if __name__ == "__main__":


    templateLocation = '../templates/template_static_curve_right.png'
    img_template = cv2.imread(templateLocation,0)

    for i in range(2):
        # Getting the image to test on
        print(i)
        imageLocation = 'Dock Images/curve_right/group6/opencv_frame_{0}.png'.format(i)
        img_bgr = cv2.imread(imageLocation)

        # Carry out template matching on the image 
        # TODO: how do we know which template to use?
        match_list, foundTemplate = templateMatching(img_bgr, img_template,show=True)

        if(foundTemplate): 
            
            print(match_list)

            # Use the templates to crop the image
            img_crop_bgr = imageCropping(img_bgr, img_template, match_list,show=True)
"""