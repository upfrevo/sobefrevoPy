import RPi.GPIO as GPIO, time, pygame, json, multiprocessing, sys, pygame.camera, logging, logging.handlers, os
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

sys.path.insert(0, "libs")
#libs
import audio as AUDIO
import led as LED
import classificador_conteudo as CC
import beacon as BEACONS


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
estado_inicial = False
andar_atual = -1


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
    logging.info("Tirando Foto... - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    filename = './samples/sample{}.jpg'.format(count)
    img = cam.get_image()

    if flip == True:
        img = pygame.transform.flip(img,False,True)

    pygame.image.save(img,filename)
    logging.info("Salvando Imagem {}... - {}".format(filename,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
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

def setup_log():
    handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "logs/LOG{}.log".format(time.strftime("_%Y_%m_%d"))))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)

def callback_beacons(bt_addr, rssi, packet, additional_info):
    if packet.uuid == BEACONS.UUID_BLUE:
      print("Você está no terceiro andar")
      if andar_atual != 3:
        estado_incial = True
      andar_atual = 3
    elif packet.uuid == BEACONS.UUID_PURPLE:
      print("Você está no segundo andar")
      andar_atual = 2
    elif packet.uuid == BEACONS.UUID_GREEN:
      print("Você está no primeiro andar")
      if andar_atual != 1:
        estado_inicial = True
      andar_atual = 1
    elif packet.uuid == BEACONS.UUID_BISCUI:
      if andar_atual != 0:
        estado_inicial = True
      andar_atual = 0
      print("Você está no biscui")


try:
    time.sleep(2)
    turn_led_on()
    AUDIO.init(8)
   # BEACONS.init([BEACONS.UUID_BLUE,BEACONS.UUID_GREEN,BEACONS.UUID_PURPLE],callback_beacons)
    setup_log()
    th = None
    count = 1
    while True:
        if GPIO.input(GPIO_PIR) and estado_inicial:
            logging.info("Movimento Detectado - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            #dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            #if dist >=30 and dis,t <= 100:
            watson_json = capture(count, True)
            classificador = CC.getKey(watson_json)
            logging.info("Conteúdo Selecionado - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

            try:
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
            except:
                logging.exception('Erro ao executar exibição de conteúdo!')

except:
    logging.info("Fim... - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    logging.exception('Erro catastrófico')
    GPIO.cleanup()
    cam.stop()
    LED.off()
    #BEACONS.destroy()
