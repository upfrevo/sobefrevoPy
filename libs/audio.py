import pygame, random , os
from threading import Timer

canais_ruidos = []
sons_ruidos = []
caminhos_ruidos = []
musica_trilha = pygame.mixer.music
musica_freviana = pygame.mixer.music
sons_tocados = []
timers = []
stop_flag = False

def init(canais):
    pygame.mixer.init(frequency = 44100, size = -16, channels = canais)

def prepare(trilha, ruidos):
    stop_flag = False
    musica_trilha.load(trilha[0])
    musica_trilha.set_volume(trilha[1])

    i = 0;
    for ruido in ruidos:
        canais_ruidos.append(pygame.mixer.Channel(i))
        somRuido = pygame.mixer.Sound(ruidos[i][0])
        somRuido.set_volume(ruidos[i][1])
        sons_ruidos.append(somRuido)
        caminhos_ruidos.append(ruido)
        i = i + 1

def play_trilha(repete):
    rep = 0;
    if repete == True:
        rep = -1
    musica_trilha.play(rep)
    
def play_freviana(tipo):
    musica_freviana.load(get_audio_freviana("audios/Freviana/" + tipo))
    musica_freviana.set_volume(1)
    musica_freviana.play(0)
    
def get_audio_freviana(dir):
    lista = os.listdir(dir)
    return dir + "/" + random.choice(lista);

def get_quantidade_ruidos():
    return len(caminhos_ruidos)

def get_indice_ruido(caminho_ruido):
    i = 0
    for ruido in caminhos_ruidos:
        if ruido == caminho_ruido:
            break
        i = i +1
    return i
        
def play_ruido(indice, force_play):
    if not stop_flag:
        if force_play == True:
            canais_ruidos[indice].stop()
        #sons_tocados.append(indice) 
        #if not som_tocando(indice):
        canais_ruidos[indice].play(sons_ruidos[indice])

def play_ruido_random():
    indice = random.randint(0, get_quantidade_ruidos() - 1)
    
    while indice in sons_tocados:        
        if len(sons_tocados) < len(sons_ruidos) or som_tocando(indice):
            indice = random.randint(0, get_quantidade_ruidos() - 1)
        else:
            sons_tocados.remove(indice)

    sons_tocados.append(indice)    
    timer = random.uniform(0.5, 20)
		
    timers.append(Timer(timer, play_ruido, (indice, True,)).start())
    #play_ruido(indice, False)

def som_tocando(indice):
    result = canais_ruidos[indice].get_busy()
    return result

def stop_all():
    random_tocado = []
    musica_trilha.fadeout(500)
    
    for canal in canais_ruidos:
        canal.stop()

    for som_ruido in sons_ruidos:
        som_ruido.set_volume(0)    
        
def freviana_tocando():
    return musica_freviana.get_busy()

def freviana_tempo():
    return musica_freviana.get_pos()

def trilha_tocando():
    return musica_trilha.get_busy()

def set_volume_trilha(volume):
    musica_trilha.set_volume(volume)

#como utilizar
#init(canais = 2)
#prepare(trilha = "../audios/Musicas/Frio_Grupo_Despojado/fria_grupo_despojado_opbh_frevando_em_paris_01.mp3", ruidos = ["../audios/Ruidos/apito.wav", "../audios/Ruidos/chasdog.wav"])
#play_trilha(repete = True)
#play_ruido_random()
#play_ruido_random()
