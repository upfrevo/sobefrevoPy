import RPi.GPIO as GPIO, time, pygame, json, multiprocessing, sys, pygame.camera, os, datetime, gc
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

sys.path.insert(0, "libs")

#libs
import audio as AUDIO
import led as LED
import classificador_conteudo as CC
import beacon as BEACONS
import envio_email
import log_util

gc.enable()
log_util.init()

try:
    delay_f = float(sys.argv[1])
    tempo_d = int(sys.argv[2])
    espera_v = int(sys.argv[3])
    salva_i = sys.argv[4] == 'True'
    flip_i = sys.argv[5] == 'True'
    dist_m = int(sys.argv[6])
    canais = int(sys.argv[7])
except Exception as e:
    log_util.log_excecao("Erro: Você recisa passar todos os 7 argumentos: Delay de foto, Tempo de despedida, Tempo de espera elevador vazio, Salvar imagens, Inverter imagem, Distancia minima, Canais de audio")
    
    sys.exit()

log_util.log_info("Modo selecionado: \nDelay de foto: {}\nTempo de despedida: {}\nTempo de espera elevador vazio: {}\nSalvar imagens: {}\nInverter imagem: {}\nDistancia minima: {}\nCanais de audio: {}".format(delay_f, tempo_d, espera_v, salva_i, flip_i, dist_m, canais))
#print("Modo selecionado: \nDelay de foto: {}\nTempo de despedida: {}\nTempo de espera elevador vazio: {}\nSalvar imagens: {}\nInverter imagem: {}\nDistancia minima: {}\nCanais de audio: {}".format(delay_f, tempo_d, espera_v, salva_i, flip_i, dist_m, canais))

log_util.log_info("Init")
#print("Init - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
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
tempo_ultimo_beacon = datetime.datetime.now()

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

def capture(count, flip, salva_imagem):
    log_util.log_info("Tirando foto")
    #print("Tirando Foto... - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    i = count
    if not salva_imagem:
        i = 1 
    
    filename = './samples/sample{}.jpg'.format(i)
    img = cam.get_image()

    if flip == True:
        img = pygame.transform.flip(img,False,True)

    pygame.image.save(img,filename)
    log_util.log_info("Salvando Imagem")
    #print("Salvando Imagem {}... - {}".format(filename,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    blink_led()
    return send_to_watson(filename, count, flip, salva_imagem)

def send_to_watson(image, count, flip, salva_imagem):
    with open(image, 'rb') as image_file:
        parameters = json.dumps({'threshold': 0, 'classifier_ids': ['Grupo_1351703499','Cores_445328997', 'Vestimenta_1354780568']})
        try:
            return visual_recognition.classify(images_file=image_file, parameters=parameters)
        except:
            return None

def turn_led_on():
    GPIO.output(GPIO_LED,True)

def blink_led():
    GPIO.output(GPIO_LED,False)
    time.sleep(0.1)
    GPIO.output(GPIO_LED,True)

def callback_beacons(bt_addr, rssi, packet, additional_info):
  global andar_atual, estado_inicial, tempo_ultimo_beacon
  agora = datetime.datetime.now()
  dif = agora - tempo_ultimo_beacon
  delta = int(dif.total_seconds())

  if (packet.uuid == BEACONS.UUID_BLUE):
    dif = agora - tempo_ultimo_beacon
    if (andar_atual != 3) or (delta > 30):
      log_util.log_info("Voce chegou no terceiro andar")
      #print("Voce chegou no terceiro andar")
      estado_inicial = True
      tempo_ultimo_beacon = agora
      andar_atual = 3
      
  elif (packet.uuid == BEACONS.UUID_GREEN):    
    if (andar_atual != 2):
      print("Voce chegou no segundo andar")
      estado_inicial = False
      andar_atual = 2

  elif (packet.uuid == BEACONS.UUID_PURPLE):    
    if (andar_atual != 0) or (delta > 25):
      log_util.log_info("Voce chegou no terreo")
      #print("Voce chegou no terreo")
      estado_inicial = True
      tempo_ultimo_beacon = agora
      andar_atual = 0

def finaliza_experiencia(tempo, toca_despedida):
    tempo = tempo - 4
    
    freviana_tocando = AUDIO.freviana_tocando()
    time.sleep(1)
    LED.off()
    AUDIO.stop_all()
    if  freviana_tocando == 1 and toca_despedida:
        AUDIO.play_freviana("Saida")
        time.sleep(3)
    if tempo > 0:
        time.sleep(tempo)

def main(delay_foto, tempo_despedida, espera_vazio, salva_imagem, flip_imagem, distancia_minima, canais_de_som):
    global andar_atual, estado_inicial, tempo_ultimo_beacon
    andar_atual = -1
    estado_inicial = False
    time.sleep(1)
    turn_led_on()
    AUDIO.init(canais_de_som)
    BEACONS.init([BEACONS.UUID_BLUE,BEACONS.UUID_PURPLE],callback_beacons)
    count = 1
    distancia = -1
    cont_dist = 0
    ultimo_tempo_movimento = datetime.datetime.now()
    while True:
        if (count % 10 == 0)
            gc.collect()
        if estado_inicial == True:
            tempo_ultimo_beacon = datetime.datetime.now()
            finaliza_experiencia(tempo_despedida, True)
            
            if distancia_minima < 0:
                distancia = distancia_minima
            else:
                distancia = distance()
            
            if GPIO.input(GPIO_PIR) and distancia <= distancia_minima:
                log_util.log_info("Movimento Detectado")
                #print("Movimento Detectado - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
                AUDIO.play_freviana("Entrada")
                estado_inicial = False
                time.sleep(delay_foto)
                
                classificador = []
                
                try:
                    watson_json = capture(count, flip_imagem, salva_imagem)
                    #print("Recebeu json Watson - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
                    log_util.log_info("Recebeu json Watson")
                    if watson_json != None:
                        classificador = CC.getKey(watson_json, False)
                    else:
                        classificador = CC.getKey("", True)
                        log_util.log_info("Classificador randomico")
                        #print("Classificador randomico: {}".format(classificador))
                except Exception as e:                    
                    print(str(e))
                    classificador = CC.getKey("", True)
                    log_util.log_info("Classificador randomico")
                    log_util.log_excecao(str(e))
                
                log_util.log_info("Conteudo Selecionado")
                #print("Conteudo Selecionado - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

                try:
                    AUDIO.stop_all()
                    AUDIO.prepare(classificador[0], classificador[1])
                        
                    tempo_sleep = (AUDIO.freviana_tempo() / 1000)
                    if tempo_sleep > 0:
                        time.sleep(tempo_sleep)
                        
                    LED.run(classificador[2])
                    AUDIO.play_trilha(True)

                    for ruido in classificador[1]:
                        if classificador[3] == False and not ruido[2]:
                            AUDIO.play_ruido_random()
                        else:
                            AUDIO.play_ruido(AUDIO.get_indice_ruido(ruido), True)

                    ultimo_tempo_movimento = datetime.datetime.now()
                    count = count + 1
                except Exception as e:
                    s = str(e)
                    log_util.log_excessao(s)
                    #print('Erro ao executar exibicao de conteudo: ' + s)

        else:
            agora = datetime.datetime.now()
            dif = agora - ultimo_tempo_movimento
            delta = int(dif.total_seconds())
            if AUDIO.trilha_tocando():
                if (classificador[3] and not AUDIO.som_tocando(0)):
                    AUDIO.set_volume_trilha(1)
                
                if GPIO.input(GPIO_PIR):
                    ultimo_tempo_movimento = datetime.datetime.now()
                elif delta >= espera_vazio:
                    log_util.log_info("Finalizando por falta de movimento")
                    #print("Finalizando por falta de movimento - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
                    andar_atual = -1
                    finaliza_experiencia(tempo_despedida, True)
                    
def destroy():
    log_util.log_info("Fim...")
    #print("Fim... - " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    #print('Erro catastrofico')
    envio_email.envia_email("Destroy chamado", nsg)
    finaliza_experiencia(0, False)
    GPIO.cleanup()
    cam.stop()    
    BEACONS.destroy()

def restart():
    destroy()
    main(delay_foto = delay_f, tempo_despedida = tempo_d, espera_vazio = espera_v, salva_imagem = salva_i, flip_imagem = flip_i, distancia_minima = dist_m, canais_de_som = canais)

try:    
    main(delay_foto = delay_f, tempo_despedida = tempo_d, espera_vazio = espera_v, salva_imagem = salva_i, flip_imagem = flip_i, distancia_minima = dist_m, canais_de_som = canais)
except Exception as e:
    log_util.log_excecao(str(e))
    restart()
