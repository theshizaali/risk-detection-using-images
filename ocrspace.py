import requests
import json
import os
import time

myDict = {}
DIR_PATH = "Imges/"

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
  payload = {'isOverlayRequired': overlay,
             'apikey': api_key,
             'language': language,
             }
  time.sleep(0.01)
  print("0.01 sleep")

  try:
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    
    myJson = json.loads(r.content)
    print(myJson)
    try:
      parsedText = myJson["ParsedResults"][0]["ParsedText"]
      print(parsedText)
      try:
        return parsedText
      except:
        return "error"

    except:
      return "error occurred"

  except:
    return "request error"
  '''
  try:
    return r.content.decode()
  except:
    return "error"
  '''

def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
  payload = {'url': url,
             'isOverlayRequired': overlay,
             'apikey': api_key,
             'language': language,
             }
  r = requests.post('https://api.ocr.space/parse/image',
                    data=payload,
                    )
  try:
    return r.content.decode()
  except:
    return "error"

arr = os.listdir(DIR_PATH)
users = []

for f in arr:
  if 'Captions_' in f:
    continue
  else:
    users.append(f)

for u in users:
  print(u)
  myList = []
  path = "NSF_Users/" + u
  images = os.listdir(path)
  for image in images:
    if '.mp4' in image:
      continue
    else:
      print(image)
      image_path = path + "/" + image
      #image_path = "NSF_Users/UserID_3314/media_2202028.jpeg"
      test_file = ocr_space_file(filename = image_path, api_key = 'efaa179d0288957')
      print("Printed immediately.")
      time.sleep(173)
      print("Printed after 173 seconds.")
      '''
      res = json.loads(test_file)
      print(res)
      myString = res["ParsedResults"][0]["ParsedText"]
      break
      Dict = {image: myString}
      '''
      Dict = {image: test_file}
      myList.append(Dict)
      
  myDict[u] = myList
  
print(myDict)
with open("text.json", "w") as outfile:  
    json.dump(myDict, outfile) 


'''
# Use examples:
test_file = ocr_space_file(filename='test.jpg',api_key='efaa179d0288957')
#print(test_file)
res = json.loads(test_file)
print(res["ParsedResults"][0]["ParsedText"])
'''
