import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
import pygame
import pygame.camera

print("Init - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) #PIR
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1920,1080))
cam.start()

def capture(count):    
    print("Capturing... - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    filename = './samples/sample{}.jpg'.format(count)
    img = cam.get_image()
    img = pygame.transform.flip(img,False,True)
    pygame.image.save(img,filename)
    print("Saving image {}... - {}".format(filename,strftime("%Y-%m-%d %H:%M:%S", gmtime())))

try:
    time.sleep(2)
    count = 1
    while True:
        if GPIO.input(23):
            print("Motion Detected - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            capture(count)
            count = count+1

except:
    GPIO.cleanup()
    cam.stop()
