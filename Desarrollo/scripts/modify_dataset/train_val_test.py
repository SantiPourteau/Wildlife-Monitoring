# Splits the raw dataset into train, validation and test datasets
# The original dataset has the following structure: 
#   - The dataset is divided into 3 folders: Cow, Deer and Horse
#   - Each folder contains subfolders with the RGB Images, Thermal Images and Annotations

import os
import shutil
import random

seed = 0
# Path to the raw dataset
path = '../../data_yolo/data_renamed/'

# Path to the new dataset
train_path = '../../data_yolo/train_data/'
val_path = '../../data_yolo/val_data/'
test_path = '../../data_yolo/test_data/'

# Create the new dataset folders
if not os.path.exists(train_path):
    os.makedirs(train_path)
if not os.path.exists(val_path):
    os.makedirs(val_path)
if not os.path.exists(test_path):
    os.makedirs(test_path)

# Create the new dataset folders for each Deer Cow and Horse
if not os.path.exists(train_path + 'Cow/'):
    os.makedirs(train_path + 'Cow/')
if not os.path.exists(train_path + 'Deer/'):
    os.makedirs(train_path + 'Deer/')
if not os.path.exists(train_path + 'Horse/'):
    os.makedirs(train_path + 'Horse/')
if not os.path.exists(val_path + 'Cow/'):
    os.makedirs(val_path + 'Cow/')
if not os.path.exists(val_path + 'Deer/'):
    os.makedirs(val_path + 'Deer/')
if not os.path.exists(val_path + 'Horse/'):
    os.makedirs(val_path + 'Horse/')
if not os.path.exists(test_path + 'Cow/'):
    os.makedirs(test_path + 'Cow/')
if not os.path.exists(test_path + 'Deer/'):
    os.makedirs(test_path + 'Deer/')
if not os.path.exists(test_path + 'Horse/'):
    os.makedirs(test_path + 'Horse/')

# Splits the dataset into train, validation and test datasets
for folder in os.listdir(path):
    if os.path.isdir(path + folder):
        subfolders = os.listdir(path + folder)
        random.shuffle(subfolders)
        train = subfolders[:int(len(subfolders)*0.75)]
        val = subfolders[int(len(subfolders)*0.75):int(len(subfolders)*0.9)]
        test = subfolders[int(len(subfolders)*0.9):]
        for subfolder in subfolders:
            if subfolder in train:
                shutil.copytree(path + folder + '/' + subfolder, train_path + folder + '/' + subfolder)
            elif subfolder in val:
                shutil.copytree(path + folder + '/' + subfolder, val_path + folder + '/' + subfolder)
            elif subfolder in test:
                shutil.copytree(path + folder + '/' + subfolder, test_path + folder + '/' + subfolder)
