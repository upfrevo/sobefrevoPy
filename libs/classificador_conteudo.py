import os, random

dir = ""

def getEfeitoLed(dir):    
    lista_efeitos = os.listdir("efeitos_led/" + dir)
    return "efeitos_led/" + dir + "/" + random.choice(lista_efeitos);

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
    

def getKey(result):
    
    coresKey = ""
    grupoKey = ""
    objetoKey = "Despojado"
    coresClasses = result['images'][0]['classifiers'][0]['classes']
    grupoClasses = result['images'][0]['classifiers'][1]['classes']
    
    # get Cores    
    coresKey = getCor(coresClasses)            
    grupoKey = getGrupo(grupoClasses)
        
    dir = "{0}_{1}_{2}".format(coresKey,grupoKey,objetoKey)
    print(dir)
    musicas = os.listdir("audios/Musicas/" + dir)
    lista_ruidos = os.listdir("audios/Ruidos/")
    efeito_led = getEfeitoLed(dir)
    musica = "audios/Musicas/" + dir + "/" + random.choice(musicas)
    ruidos = random.sample(lista_ruidos, 1);
    concat_ruidos = []
    
    for ruido in ruidos:
        concat_ruidos.append("audios/Ruidos/" + ruido)
        
    return [musica, concat_ruidos, efeito_led]    
