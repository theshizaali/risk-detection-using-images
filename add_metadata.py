'''
add_metadata.py

This program uses CSV files retrieved from MySQL Workbench
to generate features for each image in the dataset which are used in Features_Classification.py.
These features are user count, message count, image count, image sender, and image engagement.

Before running this code, make sure to run the necessary queries for each feature and update file paths.

The JSON file created by this program builds on the previous dictionary,
adding more information about metadata features.
The message and image count features reflect the number of messages in the conversation up to that point,
and this allows for risk detection in the moment as soon as a message has been sent.
'''

import csv
import json

# existing ocr output file
image_json = open('Screenshots_and_Risk_Output.json', 'r')
image_json = json.load(image_json)

################################################################

# csv contains all conversations and s3 location
# select ConversationID, S3Location from Messages where S3Location is not null;
convID_imgpath = open('<MY PATH>', 'r')
convID_imgpath = csv.reader(convID_imgpath)
next(convID_imgpath)

imagepath_to_convID = {}  # image : conversation id
num_imgs = 0
for convID, imagepath in convID_imgpath:
    num_imgs += 1
    imagepath_to_convID[imagepath] = convID
print(num_imgs, 'images read (calculating image path to conversation id)')

################################################################

# csv contains conversation and s3 location for images (ordered by date sent)
# select ConversationID, S3Location from Messages where S3Location is not null order by MessageID desc;
ordered_img = open('<MY PATH>', 'r')
ordered_img = csv.reader(ordered_img)
next(ordered_img)  # ignore first line of csv

imgs_ordered = {}  # conversation: list of images in order
num_convs = 0
num_imgs = 0
for convID, img in ordered_img:
    num_imgs += 1
    try:  # there exists an entry for this conversation
        img_list = imgs_ordered[convID]
        img_list.append(img)
        imgs_ordered[convID] = img_list
    except KeyError:  # no entry for this conversation yet
        num_convs += 1
        img_list = [img]
        imgs_ordered[convID] = img_list
print(num_convs, 'conversations and', num_imgs, 'images read (calculating conversation to image list)')

image_number = {}  # image : image number in conversation
num_convs = 0
num_imgs = 0
for convID in imgs_ordered:
    num_convs += 1
    img_list = imgs_ordered[convID]
    count = 0
    for img in img_list:  # iterate through images in conversation
        num_imgs += 1
        count += 1
        image_number[img] = count
print(num_convs, 'conversations and', num_imgs, 'images read (calculating image to image number)')

################################################################

# csv contains conversation and s3 location for messages (ordered by date sent)
# select ConversationID, S3Location from Messages where ConversationID in
# (select distinct ConversationID from Messages where S3Location is not null) order by MessageID desc;
ordered_msg = open('<MY PATH>', 'r')
ordered_msg = csv.reader(ordered_msg)
next(ordered_msg)  # ignore first line of csv

msgs_ordered = {}  # conversation : list of message's s3 location in order
num_convs = 0
num_msgs = 0
for convID, img in ordered_msg:
    num_msgs += 1
    try:  # there exists an entry for this conversation
        msg_list = msgs_ordered[convID]
        msg_list.append(img)
        msgs_ordered[convID] = msg_list
    except KeyError:  # no entry for this conversation yet
        num_convs += 1
        msg_list = []
        msg_list.append(img)
        msgs_ordered[convID] = msg_list
print(num_convs, 'conversations and', num_msgs, 'messages read (calculating conversation to message list)')

message_number = {}  # image : message number in conversation
num_convs = 0
num_msgs = 0
num_imgs = 0
for convID in msgs_ordered:
    num_convs += 1
    msg_list = msgs_ordered[convID]
    count = 0
    for img in msg_list:  # iterate through messages in conversation
        num_msgs += 1
        count += 1
        if img != 'NULL':  # only consider messages with an image
            num_imgs += 1
            message_number[img] = count
print(num_convs, 'conversations,', num_msgs, 'messages, and', num_imgs, 'images read (calculating image to message number)')

################################################################

# csv contains conversation to number of users in conversation
# select ConversationID, count(ParticipantsID) from Participants group by ConversationID
# having ConversationID in (select distinct ConversationID from Messages where S3Location is not null);
convID_users = open('<MY PATH>', 'r')
convID_users = csv.reader(convID_users)
next(convID_users)  # ignore first line of csv

convID_to_user_count = {}  # converation : user count
num_convs = 0
for convID, num_users in convID_users:
    num_convs += 1
    convID_to_user_count[convID] = int(num_users)
print(num_convs, 'conversations read (calculating conversation id to users count)')

################################################################

# csv contains conversation to users in conversation
# select ConversationID, Username from Participants where ConversationID in
# (select distinct ConversationID from Messages where S3Location is not null);
convID_users = open('<MY PATH>', 'r')
convID_users = csv.reader(convID_users)
next(convID_users)  # ignore first line of csv

# set up dict for convID to users
convID_to_users = {}
num_users = 0
num_convs = 0
for convID, user in convID_users:
    num_users += 1
    try:  # there exists an entry for this conversation
        user_list = convID_to_users[convID]
        user_list.append(user)
        convID_to_users[convID] = user_list
    except KeyError:  # not yet a dict entry for this conversation
        num_convs += 1
        user_list = [user]
        convID_to_users[convID] = user_list
print(num_convs, 'conversations and', num_users, 'users conversed with (calculating conversation id to users list)')

################################################################

# csv contains image to username of sender
# select ConversationID, S3Location, Username from Messages where S3Location is not null;
image_sender = open('<MY PATH>', 'r')
image_sender = csv.reader(image_sender)
next(image_sender)  # ignore first line of csv

image_to_sender = {}  # image : 0 or 1 depending on if participant sent image
num_imgs = 0
error = 0
for convID, image, sender in image_sender:
    num_imgs += 1
    try:  # there is a user list for this conversation
        users = convID_to_users[convID]
        if sender in users:  # someone else sent it
            participant_sent_image = 0
        else:  # participant sent it
            participant_sent_image = 1
    except KeyError:  # user list does not exist
        #print('no user list for', convID)
        error += 1
        participant_sent_image = 'NULL'
    image_to_sender[image] = participant_sent_image
print(num_imgs, 'images read with', error, 'errors where user list does not exist (calculating image to sender)')

################################################################

# count how many images the participant sent up until that point
image_engagement = {}  # image : engagement level
num_imgs = 0
error = 0
for image in image_to_sender:
    num_imgs += 1

    convID = imagepath_to_convID[image]
    img_idx = image_number[image] - 1
    img_list = imgs_ordered[convID]

    numsent = 0
    err = False
    for i, im in enumerate(img_list):
        if i <= img_idx:
            sent = image_to_sender[im]
            if sent != 'NULL':
                numsent += sent
            else:  # no info on who sent the image
                err = True
    if err:
        engagement = 'NULL'
        error += 1
    else:
        engagement = numsent/image_number[image]
    image_engagement[image] = engagement

print(num_imgs, 'images read with', error, 'errors where image sender is null (calculating image to engagement)\n')

################################################################

# update final dictionary
count = 0
error = 0
for image in image_json:  # just for verified images
    count += 1
    try:
        convID = imagepath_to_convID[image]
        message_count = message_number[image]
        image_count = image_number[image]
        user_count = convID_to_user_count[convID]
        image_sender = image_to_sender[image]
        engagement = image_engagement[image]
    except KeyError:  # the info we want does not exist for this image
        error += 1
        # print('error with image', image)
        message_count = 'NULL'
        image_count = 'NULL'
        user_count = 'NULL'
        image_sender = 'NULL'
        engagement = 'NULL'

    user_count_entry = {'User Count': user_count}
    message_count_entry = {'Message Count': message_count}
    image_count_entry = {'Image Count': image_count}
    image_sender_entry = {'Image Sender': image_sender}
    engagement_entry = {'Image Engagement': engagement}

    image_json[image].update(user_count_entry)
    image_json[image].update(message_count_entry)
    image_json[image].update(image_count_entry)
    image_json[image].update(image_sender_entry)
    image_json[image].update(engagement_entry)

print(count, 'entries updated in total with', error, 'KeyErrors')

output_path = '<MY PATH>'
print('Output is being sent to', output_path)
with open(output_path, 'w') as outfile:
    json.dump(image_json, outfile)


