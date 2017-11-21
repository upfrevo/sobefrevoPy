import json

data = {
  "images_processed": 1,
  "images": [
    {
      "classifiers": [
        {
          "name": "default",
          "classes": [
            {
              "score": 0.581,
              "class": "person"
            },
            {
              "score": 0.52,
              "class": "finish coat",
              "type_hierarchy": "/plaster/finish coat"
            },
            {
              "score": 0.52,
              "class": "plaster"
            },
            {
              "score": 0.504,
              "class": "room light",
              "type_hierarchy": "/light source/room light"
            },
            {
              "score": 0.52,
              "class": "light source"
            },
            {
              "score": 0.5,
              "class": "Sheetrock"
            },
            {
              "score": 0.695,
              "class": "reddish orange color"
            },
            {
              "score": 0.592,
              "class": "light brown color"
            }
          ],
          "classifier_id": "default"
        }
      ],
      "image": "./samples/sample1.jpg"
    }
  ],
  "custom_classes": 0
}

key = ""

                
def getPartialKey(classifier, score):
    return classifier.replace(" ", "_").upper();

    
for image in data["images"]:
    for classifier in image["classifiers"]:
            for clazz in classifier["classes"]:
                key += ":" + getPartialKey(clazz["class"], clazz["score"])
                
print(key)

        

