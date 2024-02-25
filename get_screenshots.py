'''
get_screenshots.py

This code should be used alongside get_screenshots_utils.py,
which contains the 3 necessary functions for detecting a screenshot.
Before running the code, make sure to update the necessary file locations (line 17, 20, 22).

OCR_Output (line 17) should be in the format imagepath: {'OCR': 'extracted text'}.

The JSON file created by this program creates a dictionary in the following format:
imagepath: {'Screenshot': 0 or 1}
'''

import json
from get_screenshots_utils import *

OCR_Output = open('OCR_Output.json', 'r')
all_images = json.load(OCR_Output)  # store json file in dictionary

image_loc = '<SOME PATH>'  # include / at the end of this path for ease

output_path = 'Screenshots_Output.json'
screenshots = {}  # dictionary for the output json file

total_images = 0
total_screenshots = 0

images = list(all_images.keys())  # get users as a list
for image in images:
    total_images += 1
    print('Working on image', total_images)

    image_path = image_loc + image
    text = all_images[image]['OCR']

    wc = check_wordcount(text, 3)  # text has 3 or more words

    dims = False
    if wc:  # don't bother checking dimensions if bad word count
        dims = check_dimensions(image_path)

    crop = False
    if wc and dims:  # don't bother checking if bad word count or dimensions
        crop = check_crop(image_path)

    if wc and dims and crop:  # meets all 3 criteria
        total_screenshots += 1
        entry = {'Screenshot': 1}
    else:  # not a screenshot
        entry = {'Screenshot': 0}

    screenshots[image] = entry  # update whether screenshot or not

print('There were', total_screenshots, 'screenshots detected in', total_images, 'total images.')
print('Output is being sent to', output_path)
with open(output_path, 'w') as outfile:
    json.dump(screenshots, outfile)