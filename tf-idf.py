import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')
corpus = []

f1 = open('dictionary_nonrisky_p_captions.json', 'r')
f2 = open('dictionary_nonrisky_o_captions.json', 'r')

risky_p = json.load(f1)
risky_o = json.load(f2)

word_freqs = {}

for user in risky_p:
	for conversation in risky_p[user]:
		for images in risky_p[user][conversation]:
			word_list = risky_p[user][conversation][images]
			word_list = word_list.split(".")
			word_list = word_list[0].split(" ")

		res = []
		for i in word_list:
		    if i not in res:
		        res.append(i)
		word_list = res

		#corpus.append(' '.join(word_list))
		for word in word_list:
			if word not in word_freqs:
				word_freqs[word] = 0
			word_freqs[word] += 1

for user in risky_o:
	for conversation in risky_p[user]:
		for images in risky_p[user][conversation]:
			word_list = risky_p[user][conversation][images]
			word_list = word_list.split(".")
			word_list = word_list[0].split(" ")
		
		res = []
		for i in word_list:
		    if i not in res:
		        res.append(i)
		word_list = res

		#corpus.append(' '.join(word_list))
		for word in word_list:
			if word not in word_freqs:
				word_freqs[word] = 0
			word_freqs[word] += 1

#sorted_word_freqs = sorted(word_freqs.items(), key=lambda x: x[1])
#print(sorted_word_freqs)

################################################################

for user in risky_p:
	for conversation in risky_p[user]:
		for images in risky_p[user][conversation]:
			word_list = risky_p[user][conversation][images]
			word_list = word_list.split(".")
			word_list = word_list[0].split(" ")

		for word in word_list:
			if word_freqs[word] < 4:
				word_list.remove(word)

		corpus.append(' '.join(word_list))
		

for user in risky_o:
	for conversation in risky_p[user]:
		for images in risky_p[user][conversation]:
			word_list = risky_p[user][conversation][images]
			word_list = word_list.split(".")
			word_list = word_list[0].split(" ")

		for word in word_list:
			if word_freqs[word] < 4:
				word_list.remove(word)

		corpus.append(' '.join(word_list))

X = tfidf.fit_transform(corpus)
indices = np.argsort(tfidf.idf_)[::-1]
features = tfidf.get_feature_names()
top_n = 30
top_features = [features[i] for i in indices[:top_n]]
print(top_features)