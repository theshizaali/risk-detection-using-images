"""
OCR.py

Before running this program, be sure to update the necessary paths (line 36 and 38),
prefix of user folders (line 45), and permitted file extensions (line 53).
This program assumes a structure of images in directories like the example below
and creates a JSON file in the following format: imagepath: {'OCR': 'extracted text'}

IGDD_Images
├── User_1
│   ├── media_1.jpg
│   ├── ...
│   └── media_n.jpg
├── User_2
│   ├── media_1.jpg
│   ├── ...
│   └── media_n.jpg
└── User_n
    ├── media_1.jpg
    ├── ...
    └── media_n.jpg
"""

# import statements
import cv2
import re
import os
import pytesseract
import json

# configure pytesseract: options at https://muthu.co/all-tesseract-ocr-options/
# currently: english, neural nets LSTM engine, fully automatic page segmentation
config = ('-l eng --oem 1 --psm 3')

# folder containing user directories of images
IGDDImages_path = '/Volumes/Research/STIR/ML/IGDDImages'

output_path = 'OCR_Output.json'

dictionary = {}  # for the final JSON file
total_users = 0
total_images = 0

for user in os.listdir(IGDDImages_path):  # loop through all users in IGDDImages_path
    if user.startswith('UserID_'):  # ignore extra files that are not users
        total_users += 1
        print('Working on', user + ', user number', total_users)
        user_path = IGDDImages_path + '/' + user  # absolute user path

        # get images in this user's directory
        user_images = 0
        for file in os.listdir(user_path):
            if file.endswith('.jpeg') or file.endswith('.jpg'):  # permitted file extensions
                total_images += 1
                user_images += 1
                image_path = (user_path + '/' + file)  # absolute image path

                # keep track of how far along the program is
                print('Image path:', image_path)
                print('Working on image', user_images, 'for user', total_users, '   total images count:', total_images, '\n')

                image = cv2.imread(image_path)

                # OCR and process extracted text
                text = pytesseract.image_to_string(image, config=config)  # extract text
                text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)  # remove invalid characters
                text = " ".join(text.split())  # remove extra spaces

                # update dictionary for this user
                relative_path = user + '/' + file
                dict_entry = {'OCR': text}
                dictionary[relative_path] = dict_entry

print('\n\nTotal number of users: ', total_users)
print('Total number of images:', total_images)
print('\nThe output is being sent to', output_path)

with open(output_path, 'w') as outfile:
    json.dump(dictionary, outfile)