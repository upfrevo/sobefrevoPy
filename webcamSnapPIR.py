import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
import pygame
import pygame.camera
import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
from datetime import datetime
import sys
import random


print("Init - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
GPIO.setmode(GPIO.BCM)
#set GPIO Pins
GPIO_TRIGGER = 22
GPIO_ECHO = 24
GPIO_PIR = 23
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_PIR, GPIO.IN) #PIR

pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1920,1080))
cam.start()
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='e4b5f0635c00ae28629571bfadebdb651f00b4f2')

def distance():    
    GPIO.output(GPIO_TRIGGER, False)
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = TimeElapsed * 34029 / 2

    return distance

def capture(count, flip):    
    print("Capturing... - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    filename = './samples/sample{}.jpg'.format(count)
    img = cam.get_image()
    if flip == True:
        img = pygame.transform.flip(img,False,True)
    pygame.image.save(img,filename)
    print("Saving image {}... - {}".format(filename,strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    
    send_to_watson(filename)
    
def send_to_watson(image):
    print("Retrieving image file... - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    with open(image, 'rb') as image_file:
        print("Sending to Watson... - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        result = visual_recognition.classify(images_file=image_file)
        print(json.dumps(result, indent=2))
        print("Recieving from Watson... - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        return result;

try:
    time.sleep(2)
    count = 1
    while True:
        if GPIO.input(GPIO_PIR):
            print("Motion Detected - " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist >=30 and dist <= 100:
                capture(count, False)                
                count = count+1
            time.sleep(1)

except:
    GPIO.cleanup()
    cam.stop()
