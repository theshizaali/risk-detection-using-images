import json
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def text_lowercase(text):
	return text.lower()

def remove_numbers(text):
	result = re.sub(r'\d+', '', text)
	return result

def remove_punctuation(text):
	translator = str.maketrans('', '', string.punctuation)
	return text.translate(translator)

def remove_whitespace(text):
	return  " ".join(text.split())

def remove_stopwords(text):
	stop_words = set(stopwords.words("english"))
	word_tokens = word_tokenize(text)
	filtered_text = [word for word in word_tokens if word not in stop_words]
	for text in filtered_text:
		if len(text) <= 3:
			filtered_text.remove(text)

	return filtered_text

myDict = {}
f = open ('words.json', "r")
data = json.loads(f.read())

count = 0
total = 0
for user in data:
    myDict[user] = []
    for message in data[user]:
        text = data[user][message]
        text = text_lowercase(text)
        text = remove_numbers(text)
        text = remove_punctuation(text)
        text = remove_whitespace(text)
        text = remove_stopwords(text)

        if len(text) == 0:
            print(user)
            print(message)
            print(text)
            print("##########################")
            count += 1
            total += 1
            myDict[user].append(message)

        else :
            total += 1

print("COUNT IS: " + str(count))
print("TOTAL IS: " + str(total))


# Closing file
f.close()
with open("simpleImages.json", "w") as outfile: 
    json.dump(myDict, outfile)
