import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('10mm_4.avi',fourcc, 20.0, (640,480))

#out = cv2.VideoWriter('10mm_1.avi',fourcc, 20.0)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #frame = cv2.flip(frame,0)
        #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()