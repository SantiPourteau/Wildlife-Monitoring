# Rename the raw dataset


# Match the RGB and Thermal images and the annotations and rename them so they have the same name for example: Cow_1_RGB.jpg, Cow_1_Thermal.jpg, Cow_1_Annotation.txt
# Create a new folder dataset_rgb and store the images and annotations separated by subfolders called images and labels


import os
import shutil
import re
from collections import defaultdict

path = '../../data_yolo/raw_data/'

rgb_path = '../../data_yolo/dataset_rgb/'

if not os.path.exists(rgb_path):
    os.makedirs(rgb_path)

if not os.path.exists(rgb_path + 'images/'):
    os.makedirs(rgb_path + 'images/')
if not os.path.exists(rgb_path + 'labels/'):
    os.makedirs(rgb_path + 'labels/')
    
# Rename the raw dataset and move images to images folder and labels to labels folder
for folder in os.listdir(path):
    if os.path.isdir(path + folder):
        for file in os.listdir(path + folder):
            if file.endswith('R.jpg') or file.endswith('R.JPG'):
                continue
            elif file.endswith('.jpg') or file.endswith('.JPG'):
                number = file.split('_')[-1].split('.')[0]
                if number == 'R':
                    number = file.split('_')[-2].split('.')[0]
                shutil.copyfile(path + folder + '/' + file, rgb_path + 'images/' + folder + '_' + str(int(number)-1) + '_RGB.jpg')
            elif file.endswith('R.txt'):
                continue
            elif file.endswith('.txt'):
                number = file.split('_')[-1].split('.')[0]
                if number == 'R':
                    number = file.split('_')[-2].split('.')[0]

                shutil.copyfile(path + folder + '/' + file, rgb_path + 'labels/' + folder + '_' + str(int(number)-1) + '_RGB.txt')