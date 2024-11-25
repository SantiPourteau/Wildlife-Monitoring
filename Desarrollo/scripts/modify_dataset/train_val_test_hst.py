#Folder is called dataset_hst which has two subfolders images and labels, the images and annotations are stored in the respective subfolders.
#The images and annotations have the same name apart from the extension.
#separate the images into train, validation and test datasets and then assign the annotations to the categories.

import os
import random
import shutil

seed = 0
path = '../../data/dataset_hst/images'
train_path = '../../data/dataset_hst/train_data/'
val_path = '../../data/dataset_hst/val_data/'
test_path = '../../data/dataset_hst/test_data/'

if not os.path.exists(train_path):
    os.makedirs(train_path)
if not os.path.exists(val_path):
    os.makedirs(val_path)
if not os.path.exists(test_path):
    os.makedirs(test_path)

#create train/images and train/labels folders
if not os.path.exists(train_path + 'images/'):
    os.makedirs(train_path + 'images/')
if not os.path.exists(train_path + 'labels/'):
    os.makedirs(train_path + 'labels/')
#create val/images and val/labels folders
if not os.path.exists(val_path + 'images/'):
    os.makedirs(val_path + 'images/')
if not os.path.exists(val_path + 'labels/'):
    os.makedirs(val_path + 'labels/')
#create test/images and test/labels folders
if not os.path.exists(test_path + 'images/'):
    os.makedirs(test_path + 'images/')
if not os.path.exists(test_path + 'labels/'):
    os.makedirs(test_path + 'labels/')


# split images into 3 datasets, train, validation and test. 75% of the images are in the train dataset, 15% in the validation dataset and 10% in the test dataset
# then assign each image to the respective folder called train_data, val_data and test_data
# then assign the annotations to the folder that contains the image with the same name


#shuffle the images and 75% of the images are in the train dataset, 15% in the validation dataset and 10% in the test dataset

images = os.listdir(path)
random.shuffle(images)
train = images[:int(len(images)*0.75)]
val = images[int(len(images)*0.75):int(len(images)*0.9)]
test = images[int(len(images)*0.9):]

#assign the images and labels to the respective folders
for image in images:
    if image in train:
        shutil.copyfile(path + '/' + image, train_path + 'images/' + image)
        shutil.copyfile('../../data/dataset_hst/labels/' + image.split('.')[0] + '.txt', train_path + 'labels/' + image.split('.')[0] + '.txt')
    elif image in val:
        shutil.copyfile(path + '/' + image, val_path + 'images/' + image)
        shutil.copyfile('../../data/dataset_hst/labels/' + image.split('.')[0] + '.txt', val_path + 'labels/' + image.split('.')[0] + '.txt')
    elif image in test:
        shutil.copyfile(path + '/' + image, test_path + 'images/' + image)
        shutil.copyfile('../../data/dataset_hst/labels/' + image.split('.')[0] + '.txt', test_path + 'labels/' + image.split('.')[0] + '.txt')