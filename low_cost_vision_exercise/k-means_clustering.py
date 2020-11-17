from matplotlib import pyplot as plt
from cv2 import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# When training the model, check whether the original data matches the output from the kmeans function

def kMeansClustering2D():

    f = open('/Users/heisenberg/RobotLab/robot_lab_inspection/JamesTutorials/low_cost_vision_exercise/train_model.txt', "r")
    lines = f.readlines()

    trainData_x = []
    trainData_y = []
    responses = {0: [],
                1: [],
                2: [],
                3: [],
                4: [],}


    for x in lines:
        x = x.strip("\n")
        response = int(float(x.split(' ')[2]))
        x_data = float(x.split(' ')[0])
        y_data = float(x.split(' ')[1])
        trainData_x.append(x_data)
        trainData_y
        responses[response].append([x_data, y_data])


    f.close()

    Z = np.vstack((responses[0], responses[1],
                responses[2], responses[3], responses[4]))

    # # convert to np.float32
    Z = np.float32(Z)


    # # define criteria and apply kmeans()
    #TODO: Need to have a play around with different criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(
        Z, 5, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    # # Now separate the data, Note the flatten()
    A = Z[label.ravel() == 0]
    B = Z[label.ravel() == 1]
    C = Z[label.ravel() == 2]
    D = Z[label.ravel() == 3]
    E = Z[label.ravel() == 4]


    # Plot the data (outputted form kmeans)
    plt.scatter(A[:,0], A[:,1], c = 'k')
    plt.scatter(B[:,0], B[:,1], c = 'c')
    plt.scatter(C[:,0], C[:,1], c = 'b')
    plt.scatter(D[:,0], D[:,1], c = 'y')
    plt.scatter(E[:,0], E[:,1], c = 'g')

    # Plot original data
    # number_tag={0:'b',1:'c',2:'y',3:'g',4:'r'}

    # for i in range(5):
    #     print(i)
    #     for j in range(len(responses[i])):
    #         plt.scatter(responses[i][j][0],responses[i][j][1],marker='o',color=number_tag[i])
    
    plt.scatter(center[:,0],center[:,1],s = 80,c = 'm', marker = 's')
    plt.xlabel('Area'),plt.ylabel('Aspect Ratio')
    plt.show()

    # TODO: so how do we use this for prediction purposes?
    # Calculate the distance to each of the cluster centers, the cluser with the lowest distance is the predicted class


def kMeansClustering3D():

    f = open('/Users/heisenberg/RobotLab/robot_lab_inspection/JamesTutorials/low_cost_vision_exercise/train_model.txt', "r")
    lines = f.readlines()


    trainData_x = []
    trainData_y = []
    responses = {0: [],
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
                6: [],
                7: [],
                8: [],
                9: []}
    


    for x in lines:
        x = x.strip("\n")
        response = int(float(x.split(' ')[2]))
        x_data = float(x.split(' ')[0])
        y_data = float(x.split(' ')[1])
        responses[response].append([x_data, y_data, 0])
        responses[response+5].append([x_data, y_data, 1])


    f.close()

    Z = np.vstack((responses[0], responses[1],
                responses[2], responses[3], 
                responses[4], responses[5], 
                responses[6], responses[7], 
                responses[8], responses[9]))


    # # convert to np.float32
    Z = np.float32(Z)

    # # define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, 10, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    # # Now separate the data, Note the flatten()
    A = Z[label.ravel() == 0]
    B = Z[label.ravel() == 1]
    C = Z[label.ravel() == 2]
    D = Z[label.ravel() == 3]
    E = Z[label.ravel() == 4]
    F = Z[label.ravel() == 5]
    G = Z[label.ravel() == 6]
    H = Z[label.ravel() == 7]
    I = Z[label.ravel() == 8]
    J = Z[label.ravel() == 9]


    fig = plt.figure()
    ax = Axes3D(fig)

    # Plot the data
    ax.scatter(A[:,0],A[:,1],A[:,2], c = 'k')
    ax.scatter(B[:,0],B[:,1],B[:,2], c = 'c')
    ax.scatter(C[:,0],C[:,1],C[:,2], c = 'b')
    ax.scatter(D[:,0],D[:,1],D[:,2], c = 'y')
    ax.scatter(E[:,0],E[:,1],E[:,2], c = 'g')

    ax.scatter(F[:,0],F[:,1],F[:,2], c = 'r')
    ax.scatter(G[:,0],G[:,1],G[:,2], c = 'b')
    ax.scatter(H[:,0],H[:,1],H[:,2],c = 'y')
    ax.scatter(I[:,0],I[:,1],I[:,2], c = 'm')
    ax.scatter(J[:,0],J[:,1],J[:,2], c = 'k')
    ax.scatter(center[:,0],center[:,1],center[:,2],s = 80,c = 'm', marker = 's')
    plt.xlabel('Area'),plt.ylabel('Aspect Ratio')
    ax.set_zlabel('3rd Variable')
    plt.show()


    # TODO: so how do we use this for prediction purposes?
    # Calculate the distance to each of the cluster centers, the cluser with the lowest distance is the predicted class

