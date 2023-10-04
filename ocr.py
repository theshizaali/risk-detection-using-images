from PIL import Image 
import pytesseract
import os
from os import listdir
from os.path import isfile, join

'''
export GOOGLE_APPLICATION_CREDENTIALS="OCR-Image-to-String-6063bdf1aeb2.json"
'''

DIR_PATH = "NSF_Users/"

def detect_text(path):
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

'''
arr = os.listdir(DIR_PATH)
users = []

for f in arr:
	if 'Captions_' in f:
		continue
	else:
		users.append(f)

for u in users:
	print(u)
	path = "NSF_Users/" + u
	images = os.listdir(path)
	for image in images:
		if '.mp4' in image:
			continue
		else:
			print(image)

'''
detect_text("NSF_Users/UserID_619/media_165747.jpeg")

'''
print(pytesseract.image_to_string(Image.open(path)))
print(pytesseract.image_to_string(Image.open(path), lang='eng'))
'''