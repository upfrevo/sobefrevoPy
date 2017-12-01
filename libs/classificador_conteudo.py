import os, random, re

dir = ""

def getEfeitoLed(dir, midnight=False):    
    lista_efeitos = os.listdir("efeitos_led/" + dir)
    
    efeito = "efeitos_led/" + dir + "/" + random.choice(lista_efeitos);

    if (midnight == True):
        efeito = "efeitos_led/homem_meia_noite.txt"
    
    return efeito

def getCor(coresClasses):    
    cor = ""
    if coresClasses[0]['score'] >= coresClasses[1]['score']:
         cor = coresClasses[0]['class']   
    else:
         cor = coresClasses[1]['class']
    
    return cor

def getGrupo(grupoClasses):    
    grupo = ""
    if grupoClasses[0]['score'] >= grupoClasses[1]['score'] and grupoClasses[0]['score'] >= grupoClasses[2]['score']:
        grupo = grupoClasses[0]['class']
    elif grupoClasses[1]['score'] >= grupoClasses[2]['score']:
        grupo = grupoClasses[1]['class']
    else:
        grupo = grupoClasses[2]['class']
        
    return grupo

def getObjeto(objetoClasses):
    objeto = ""
    if objetoClasses[0]['score'] >= objetoClasses[1]['score']:
         objeto = objetoClasses[0]['class']   
    else:
         objeto = objetoClasses[1]['class']
    
    return objeto
    
def checkMusica(musica):    
    pos = musica.find("homem_da_meia_noite")
    
    if pos != -1:
        return True
    
    return False

def isIndividual(dir):
    pos = dir.find("Individual")
    
    if pos != -1:
        return True
    
    return False

def isBurburinho(dir):
    pos = dir.find("Burburinhos")
    
    if pos != -1:
        return True
    
    return False

def isGrupo(dir):
    pos = dir.find("Grupo")
    
    if pos != -1:
        return True
    
    return False

def isPar(dir):
    pos = dir.find("Par")
    
    if pos != -1:
        return True
    
    return False

def getRuidos(lista, dir):
    lista_ruidos = []
    
    is_individual = isIndividual(dir)
    is_grupo = isGrupo(dir)    
    
    if (is_individual == True):
        entrevistas = random.sample(lista['entrevistas'], 1);
        for entr in entrevistas:
            lista_ruidos.append(["audios/Entrevistas/" + entr, getVolumeRuido(dir), False])    
    else:
        ruidos = random.sample(lista['ruidos'], 3);        
        for ruido in ruidos:            
            lista_ruidos.append(["audios/Ruidos/" + ruido, getVolumeRuido(dir), False])

        burburinho = random.sample(lista['burburinhos'], 1);        
        lista_ruidos.append(["audios/Burburinhos/" + burburinho[0], getVolumeRuido(dir), True])
    
    return lista_ruidos
            
def getMusica(musicas, dir):
    return "audios/Musicas/" + dir + "/" + random.choice(musicas)

def getRandom(min, max):
    return random.uniform(min, max)

def getVolumeTrilha(dir):    
    volume = 1.0    
    if (isIndividual(dir) == True):        
        volume = getRandom(0.1, 0.2)
        
    return volume

def getVolumeRuido(dir):    
    volume = getRandom(0.5, 0.65)
    if (isIndividual(dir) == True):    
        volume = 1.0
        
    return volume


def getKey(result, randomico):    
    coresKey = ""
    grupoKey = ""
    objetoKey = ""

    if not randomico:
        coresClasses = result['images'][0]['classifiers'][0]['classes']
        grupoClasses = result['images'][0]['classifiers'][1]['classes']
        objetoClasses = result['images'][0]['classifiers'][2]['classes'] 
        coresKey = getCor(coresClasses)            
        grupoKey = getGrupo(grupoClasses)
        objetoKey = getObjeto(objetoClasses)
    else:
        coresKey = random.choice(["Frio", "Quente"])
        grupoKey = random.choice(["Individual","Par","Grupo"])
        objetoKey = random.choice(["Formal", "Despojado"])
        
    dir = "{0}_{1}_{2}".format(coresKey,grupoKey,objetoKey)    
    
    musicas = os.listdir("audios/Musicas/" + dir)
    
    lista = {
        "ruidos": os.listdir("audios/Ruidos/"),
        "entrevistas": os.listdir("audios/Entrevistas/"),
        "burburinhos": os.listdir("audios/Burburinhos/")
    }
    
    musica = [getMusica(musicas, dir), getVolumeTrilha(dir)]
    midnight_man = checkMusica(musica[0])    
    
    efeito_led = getEfeitoLed(dir, midnight_man)    
    
    ruidos = getRuidos(lista, dir)
    
    ruido_comeco = isIndividual(dir)
    
    return [musica, ruidos, efeito_led, ruido_comeco]    
