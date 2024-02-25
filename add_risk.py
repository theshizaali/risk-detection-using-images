'''
add_risk.py

Before running the code, make sure to update the necessary file locations (line 14, 17, 20).
The csv file (line 18) should contain all images with their risk labels.

The JSON file created by this program creates a dictionary in the following format:
imagepath: {'Screenshot': 0 or 1, 'Risk': 0, 1, or 'NULL'}
'''

import json
import csv

jsonfile = open('Screenshots_Output.json', 'r')
all_images = json.load(jsonfile)  # store json file in dictionary

csvfile = open('all_labels.csv', 'r')
csvreader = csv.reader(csvfile)

output_path = 'Screenshots_and_Risk_Output.json'

risk_dict = {}
for risk, path in csvreader:
    if risk != "NULL":
        risk_dict[path] = risk
print(len(risk_dict), 'total entries in the risk dictionary')

newdict = all_images.copy()
total_images = 0
images = list(all_images.keys())  # get users as a list
for image in images:  # iterate through existing json file
    total_images += 1

    risk_status = 'NULL'
    if image in risk_dict:
        risk_status = risk_dict[image]

    risk_entry = {'Risk': risk_status}
    newdict[image].update(risk_entry)

print(total_images, 'total images read')
print('output is being sent to', output_path)
with open(output_path, 'w') as outfile:
    json.dump(newdict, outfile)