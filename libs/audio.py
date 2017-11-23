import pygame, random

canais_ruidos = []
sons_ruidos = []
caminhos_ruidos = []
musica_trilha = pygame.mixer.music
sons_tocados = []

def init(canais):
    pygame.mixer.init(frequency = 44100, size = -16, channels = canais)

def prepare(trilha, ruidos):
    musica_trilha.load(trilha)
    i = 0;
    for ruido in ruidos:
        canais_ruidos.append(pygame.mixer.Channel(i))
        sons_ruidos.append(pygame.mixer.Sound(ruidos[i]))
        caminhos_ruidos.append(ruido)
        i = i + 1

def play_trilha(repete):
    rep = 0;
    if repete == True:
        rep = -1
    musica_trilha.play(rep)

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
    
    play_ruido(indice, False)

def som_tocando(indice):
    result = canais_ruidos[indice].get_busy()
    return result

def stop_all():
    random_tocado = []
    musica_trilha.stop()
    for canal in canais_ruidos:
        canal.stop()
    
#como utilizar
#init(canais = 2)
#prepare(trilha = "frevo.wav", ruidos = ["apito.wav", "clarim.wav"])
#play_trilha(repete = True)
#play_ruido(indice=0, force_play=True)
#play_ruido_random()
#stop_all()
