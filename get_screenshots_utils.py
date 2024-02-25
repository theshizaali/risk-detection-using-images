'''
get_screenshots_utils.py

This code is to be used alongside get_screenshots.py
and includes the 3 necessary functions to detect a screenshot.
'''

import cv2
import pytesseract

def check_wordcount(text, threshold):
    screenshot = False
    num_words = len(text.split())
    if num_words >= threshold:
        screenshot = True
    return screenshot


def check_dimensions(image_path):
    # list that holds all the dimensions (height, width) for a screenshot
    dimensions = [(657, 320), (782, 480), (791, 480), (800, 480), (853, 480), (853, 640), (854, 640), (920, 640),
                  (960, 480), (960, 640), (997, 750), (1088, 612), (1096, 640), (1136, 640), (1138, 640), (1139, 640),
                  (1170, 540), (1280, 720), (1294, 750), (1332, 750), (1334, 616), (1334, 667), (1334, 750),(1372, 720),
                  (1440, 720), (1480, 720), (1499, 843), (1520, 720), (1560, 720), (1600, 778), (1606, 843),(1624, 750),
                  (1686, 843), (1728, 1080), (1733, 843), (1792, 828), (1825, 843), (1873, 843), (1919, 1080),
                  (1920, 1080), (1922, 1080), (2001, 1125), (2160, 1080), (2208, 1242), (2220, 1080), (2338, 1080),
                  (2340, 1080), (2436, 1125), (2688, 1242), (2960, 1440)]
    screenshot = False
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    dims = (height, width)
    if dims in dimensions:
        screenshot = True
    return screenshot


def check_crop(image_path):
    screenshot = False
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    eighth = int(height / 8)
    tenth = int(height / 10)

    top = image[0:eighth, 0:width]
    top_text = pytesseract.image_to_string(top)
    top_wc = len(top_text.split())

    bottom = image[height - tenth:height, 0:width]
    bottom_text = pytesseract.image_to_string(bottom)
    bottom_wc = len(bottom_text.split())

    if top_wc + bottom_wc > 0:
        screenshot = True
    return screenshot
