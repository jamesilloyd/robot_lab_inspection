import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while True:
    ret, frame = cam.read()
    #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)
    #out.write(frame)
            
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
#out.release()
cv2.destroyAllWindows()