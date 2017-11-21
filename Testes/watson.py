import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
from datetime import datetime
import sys
import time, random

test_url = 'https://www.ibm.com/ibm/ginni/images' \
           '/ginni_bio_780x981_v4_03162016.jpg'

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='e4b5f0635c00ae28629571bfadebdb651f00b4f2')



print(str(datetime.now()))

file_path = join(dirname(__file__), './samples/sample2.jpg')
with open(file_path, 'rb') as image_file:
    text_results = visual_recognition.classify(images_file=image_file)
    print(json.dumps(text_results, indent=2))

print(str(datetime.now()))

face_path = join(dirname(__file__), './samples/sample2.jpg')
with open(face_path, 'rb') as image_file:
    face_result = visual_recognition.classify(images_file=image_file)
    print(json.dumps(face_result, indent=2))

print(str(datetime.now()))
