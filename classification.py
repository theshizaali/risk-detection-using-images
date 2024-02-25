'''
classification.py

Before running the code, be sure to change the input path given on line 28.
This program expects a json file as input which includes the features and risk label for each image.

This program classifies an image as either non-risky (0) or risky (1)
given the image's various features:
user count, message count, image count, screenshot, image sender, and image engagement (can also use extracted text/captions).
'''

import json
import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns
sns.set()
#np.random.seed(0)  # for reproducibility

all_images = open('Feature_Output.json', 'r')
all_images = json.load(all_images)

# put info into a dataframe
df = pandas.DataFrame(all_images)
df = df.transpose()  # reshape dataframe
df.reset_index(inplace=True, drop=True)  # include indices (first column)

print('Shape of original dataframe:', df.shape)

# drop any rows where risk is null
indexNames = df[df['Risk'] == 'NULL'].index
df = df.drop(indexNames)
print('Shape of dataframe with valid risk values:', df.shape)

# drop rows that have remaining null values
indexNames = df[(df['User Count'] == 'NULL') | (df['Message Count'] == 'NULL') | (df['Image Count'] == 'NULL') |
                (df['Image Sender'] == 'NULL') | (df['Image Engagement'] == 'NULL')].index
df = df.drop(indexNames)

print('Shape of dataframe with all other null values dropped:', df.shape)
df.reset_index(inplace=True, drop=True)  # update indices

# convert dataframe types to numeric
df[['Risk', 'User Count', 'Message Count', 'Image Count', 'Image Sender', 'Image Engagement', 'Screenshot']] \
    = df[['Risk', 'User Count', 'Message Count', 'Image Count', 'Image Sender', 'Image Engagement', 'Screenshot']].apply(pandas.to_numeric)
# print(df.info())  # verify types

nonrisky = df[df['Risk'] == 0]
nonrisky.reset_index(inplace=True, drop=True)  # reset indices
risky = df[df['Risk'] == 1]
risky.reset_index(inplace=True, drop=True)  # reset indices
print('There are a total of', len(nonrisky), 'non-risky images and', len(risky), 'risky images')

# plot risky and nonrisky features
# nonrisky['User Count'].plot(kind='hist', title='Non-Risky User Count', xlim=(0, 45))
# plt.show()
# risky['User Count'].plot(kind='hist', title='Risky User Count', xlim=(0, 45))
# plt.show()
#
# nonrisky['Message Count'].plot(kind='line', title='Non-Risky Message Count', ylim=(0, 25000))
# plt.show()
# risky['Message Count'].plot(kind='line', title='Risky Message Count', ylim=(0, 25000))
# plt.show()
#
# nonrisky['Image Count'].plot(kind='line', title='Non-Risky Image Count', ylim=(0, 2500))
# plt.show()
# risky['Image Count'].plot(kind='line', title='Risky Image Count', ylim=(0, 2500))
# plt.show()
#
# nonrisky['Image Sender'].plot(kind='hist', title='Non-Risky Image Sender')
# plt.show()
# risky['Image Sender'].plot(kind='hist', title='Risky Image Sender')
# plt.show()
#
# nonrisky['Image Engagement'].plot(kind='box', title='Non-Risky Image Engagement')
# plt.show()
# risky['Image Engagement'].plot(kind='box', title='Risky Image Engagement')
# plt.show()
#
# nonrisky['Screenshot'].plot(kind='hist', title='Non-Risky Screenshot')
# plt.show()
# risky['Screenshot'].plot(kind='hist', title='Risky Screenshot')
# plt.show()


# train test split
x_train, x_test, y_train, y_test = train_test_split(df[['User Count', 'Message Count', 'Image Count',
                                                        'Image Sender', 'Image Engagement', 'Screenshot']], df['Risk'], test_size=.3)

# transform each column
column_transformer = ColumnTransformer([('minmax', MinMaxScaler(), ['User Count', 'Message Count', 'Image Count', 'Image Sender', 'Image Engagement', 'Screenshot'])])

# transform data
x_train = column_transformer.fit_transform(x_train)
x_test = column_transformer.transform(x_test)

print('\nTrain size:', x_train.shape[0])
print('Test size: ', x_test.shape[0])
print('Split for train:', np.bincount(y_train))
print('Split for test: ', np.bincount(y_test))

pipeline = Pipeline([('clf', RandomForestClassifier())])

model = pipeline.fit(x_train, y_train)

predicted = model.predict(x_test)
print('\nAccuracy:', model.score(x_test, y_test))

print('\nClassification report:')
print(classification_report(y_test, predicted))

# plot heatmap of confusion matrix
matrix = confusion_matrix(y_test, predicted)
print('Confusion matrix:')
print(matrix)
sns.heatmap(matrix.T, square=True, annot=True, fmt='d', cbar=False)
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.show()
