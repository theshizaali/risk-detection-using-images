import json
  
# Opening JSON file
with open('screenshots.json') as json_file:
    data = json.load(json_file)

count = 0
for user in data:
	for image in data[user]:
		print(image)
		count+=1


print(count)