import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
import cv2
#GPIO.setmode(GPIO.BCM)

out1 = 29
out2 = 32
out3 = 31
out4 = 33 #has an issue
out5 = 35
out6 = 36
inp1 = 37
inp2 = 38
inp3 = 40
#inp1 = 26
#inp2 = 20
#inp3 = 21


GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.setup(out4, GPIO.OUT)
GPIO.setup(out5, GPIO.OUT)
GPIO.setup(out6, GPIO.OUT)
GPIO.setup(inp1, GPIO.IN)
GPIO.setup(inp2, GPIO.IN)
GPIO.setup(inp3, GPIO.IN)

while True:
    in1 = GPIO.input(inp1)
    in2 = GPIO.input(inp2)
    in3 = GPIO.input(inp3)
    print(in1, in2, in3)


"""
GPIO.output(out1, 0)
GPIO.output(out2, 1)
GPIO.output(out3, 0)
GPIO.output(out4, 1)
GPIO.output(out5, 1)
GPIO.output(out6, 0)
"""
"""
while True:
        k = cv2.waitKey(1)
        if k%256 == 49:
            GPIO.output(out1, 0)
            GPIO.output(out2, 1)
            GPIO.output(out3, 1)
            GPIO.output(out4, 1)
            GPIO.output(out5, 1)
            GPIO.output(out6, 1)
            print ("1 high")
        elif k%256 == 50:
            GPIO.output(out1, 1)
            GPIO.output(out2, 0)
            GPIO.output(out3, 1)
            GPIO.output(out4, 1)
            GPIO.output(out5, 1)
            GPIO.output(out6, 1)
        elif k%256 == 51:
            GPIO.output(out1, 1)
            GPIO.output(out2, 1)
            GPIO.output(out3, 0)
            GPIO.output(out4, 1)
            GPIO.output(out5, 1)
            GPIO.output(out6, 1)
        elif k%256 == 52:
            GPIO.output(out1, 1)
            GPIO.output(out2, 1)
            GPIO.output(out3, 1)
            GPIO.output(out4, 0)
            GPIO.output(out5, 1)
            GPIO.output(out6, 1)
        elif k%256 == 53:
            GPIO.output(out1, 1)
            GPIO.output(out2, 1)
            GPIO.output(out3, 1)
            GPIO.output(out4, 1)
            GPIO.output(out5, 0)
            GPIO.output(out6, 1)
        elif k%256 == 54:
            GPIO.output(out1, 1)
            GPIO.output(out2, 1)
            GPIO.output(out3, 1)
            GPIO.output(out4, 1)
            GPIO.output(out5, 1)
            GPIO.output(out6, 0)
            """