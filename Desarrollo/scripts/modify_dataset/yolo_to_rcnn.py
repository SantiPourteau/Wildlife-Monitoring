#create new labels using the .txt files that are in yolo format (x_center, y_center, width, height) to rcnn format (x_min, y_min, x_max, y_max)
# enter the data_maskrcnn folder and for each subfolder find the .txt files and modify the .txt file to the new format

import os
import shutil
import re
from collections import defaultdict

path = '../../data_maskrcnn/'

subfolders = os.listdir(path)

for dataset in subfolders:
    if os.path.isdir(path + dataset):
        for folder in os.listdir(path + dataset):
            if os.path.isdir(path + dataset + '/' + folder):
                for file in os.listdir(path + dataset + '/' + folder):
                    if file.endswith('.txt'):
                        with open(path + dataset + '/' + folder + '/' + file, 'r') as f:
                            lines = f.readlines()
                        with open(path + dataset + '/' + folder + '/' + file, 'w') as f:
                            for line in lines:
                                x_center, y_center, width, height = map(float, line.split()[1:])
                                x_min = x_center - width/2
                                y_min = y_center - height/2
                                x_max = x_center + width/2
                                y_max = y_center + height/2
                                f.write('0 ' + ' '.join(map(str, [x_min, y_min, x_max, y_max])) + '\n')

#do the same but accessing the test, val and train folders inside each dataset
for dataset in subfolders:
    if os.path.isdir(path + dataset):
        for folder in os.listdir(path + dataset):
            if os.path.isdir(path + dataset + '/' + folder):
                for subfolder in os.listdir(path + dataset + '/' + folder):
                    if os.path.isdir(path + dataset + '/' + folder + '/' + subfolder):
                        for file in os.listdir(path + dataset + '/' + folder + '/' + subfolder):
                            if file.endswith('.txt'):
                                with open(path + dataset + '/' + folder + '/' + subfolder + '/' + file, 'r') as f:
                                    lines = f.readlines()
                                with open(path + dataset + '/' + folder + '/' + subfolder + '/' + file, 'w') as f:
                                    for line in lines:
                                        x_center, y_center, width, height = map(float, line.split()[1:])
                                        x_min = x_center - width/2
                                        y_min = y_center - height/2
                                        x_max = x_center + width/2
                                        y_max = y_center + height/2
                                        f.write('0 ' + ' '.join(map(str, [x_min, y_min, x_max, y_max])) + '\n')



