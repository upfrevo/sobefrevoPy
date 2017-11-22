import RPi.GPIO as GPIO, time, pygame, json, multiprocessing, sys
import pygame.camera

sys.path.insert(0, "libs")

import audio as AUDIO
import led as LED

import classificador_conteudo as CC

from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

#from datetime import datetime

print("Init - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#set GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 22
GPIO_ECHO = 24
GPIO_PIR = 23
GPIO_LED = 16
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)#ULTRASOUND TRIGGER
GPIO.setup(GPIO_ECHO, GPIO.IN)#ULTRASOUND ECHO
GPIO.setup(GPIO_PIR, GPIO.IN) #PIR
GPIO.setup(GPIO_LED, GPIO.OUT) #LED

pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1920,1080))
cam.start()
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='3c840f761086ca39e0a41c02bb8bf119f96f27ce')

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
    print("Taking Picture... - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    filename = './samples/sample{}.jpg'.format(count)
    img = cam.get_image()
    
    if flip == True:
        img = pygame.transform.flip(img,False,True)
        
    pygame.image.save(img,filename)
    print("Saving Image {}... - {}".format(filename,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    blink_led()
    
    return send_to_watson(filename)
    
def send_to_watson(image):    
    with open(image, 'rb') as image_file:
        parameters = json.dumps({'threshold': 0, 'classifier_ids': ['Grupo_1351703499','Cores_741726174']})
        return visual_recognition.classify(images_file=image_file, parameters=parameters)
    
def turn_led_on():
    GPIO.output(GPIO_LED,True)

def blink_led():
    GPIO.output(GPIO_LED,False)
    time.sleep(0.1)
    GPIO.output(GPIO_LED,True)

#try:
time.sleep(2)
turn_led_on()
AUDIO.init(8)
th = None
count = 1
while True:
    if GPIO.input(GPIO_PIR):
        print("Motion Detected - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        #dist = distance()
        #print ("Measured Distance = %.1f cm" % dist)
        #if dist >=30 and dis,t <= 100:
        watson_json = capture(count, True)
        classificador = CC.getKey(watson_json)
        print("Conteúdo Selecionado - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        #try:
        LED.off()
        if (th != None):
            th.terminate()
        
        AUDIO.stop_all()
        AUDIO.prepare(classificador[0], classificador[1])
        time.sleep(2)
        AUDIO.play_trilha(True)

        th = multiprocessing.Process(target=LED.run, args = (classificador[2],))
        th.start()

        AUDIO.play_ruido(0, True)
        count = count + 1
        time.sleep(2)           
            

#except:
    #print("Ending... - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
GPIO.cleanup()
cam.stop()
