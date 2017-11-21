import os, random

# utilizando  o json de resposta

#result = visual_recognition.classify(images_file=image_file, threshold=0, classifier_ids=['Grupo_1351703499','Cores_741726174'])

result = {
   "custom_classes": 5,
   "images": [
      {
         "classifiers": [
            {
               "classes": [
                  {
                     "class": "Frio",
                     "score": 0.0547026
                  },
                  {
                     "class": "Quente",
                     "score": 0.507963
                  }
               ],
               "classifier_id": "Cores_741726174",
               "name": "Cores"
            },
            {
               "classes": [
                  {
                     "class": "Grupo",
                     "score": 0.0645874
                  },
                  {
                     "class": "Individual",
                     "score": 0.086897
                  },
                  {
                     "class": "Par",
                     "score": 0.962037
                  }
               ],
               "classifier_id": "Grupo_1351703499",
               "name": "Grupo"
            }
         ],
         "image": ""
      }
   ],
   "images_processed": 1
}

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
    musicas = os.listdir("audios/Musicas/" + dir)
    
    return random.choice(musicas)

audioKey = getKey(result)
