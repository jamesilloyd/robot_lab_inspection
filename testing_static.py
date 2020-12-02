from cv2 import cv2
from matplotlib import pyplot as plt
from TemplateMatching import template_matching
import classification
from save_results import ResultsSave



'''
THIS IS THE MOST UP TO DATE FUNCTION USED FOR CLASSIFYING STATIC IMAGES. 
'''
if __name__ == "__main__":

    # getting the template part
    templateLocation = 'templates/template_static_straight.png'
    img_template = cv2.imread(templateLocation,0)

    my_results=ResultsSave('results/group4_static_vision_result.csv','results/group4_static_plc_result.csv')


    for i in range(23):
        # Getting the image to test on
        print(i)
        imageLocation = 'TemplateMatching/Dock Images/straight/group3/opencv_frame_{0}.png'.format(i)
        img_bgr = cv2.imread(imageLocation)

        # Carry out template matching on the image 
        # TODO: how do we know which template to use?
        match_list, foundTemplate = template_matching.templateMatching(img_bgr, img_template,show=False)

        if(foundTemplate): 
            
            # print(match_list)

            # Use the templates to crop the image
            img_crop_bgr = template_matching.imageCropping(img_bgr, img_template, match_list,show=False)

            # Use the cropped image to classify the parts
            resultsVision, resultsPLC, img_classified = classification.partClassification(img_crop_bgr, show = False, isCurves=False) 

            # print(resultsPLC)

            # Store image of classified tray for assessment
            # TODO: need to add in incrementer to store file names
            cv2.imwrite('results/static_images/classified_tray_{0}.png'.format(i),img_classified)

            # Store results in csv file for assessment
            for j in range(len(resultsVision)):
                my_results.insert_vision(str(i),str(j),str(resultsVision[str(j)]["QCPassed"]),resultsVision[str(j)]["reason"])

            # TODO: do something with plc results