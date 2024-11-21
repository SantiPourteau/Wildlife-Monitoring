# Combines the original RGB image and Thermal image into a single image with 4 channels. The first 3 channels are the RGB image and the 4th channel is the thermal image.

import os
import cv2
import numpy as np
import torch 

path = '../../data/data_renamed/'

for animal in os.listdir(path):
    if os.path.isdir(path + animal):
        for scene in os.listdir(path + animal):
            for subfolder in os.listdir(path + animal + '/' + scene):
                if subfolder == 'images':
                    for file in os.listdir(path + animal + '/' + scene + '/' + subfolder):
                        if file.endswith('RGB.jpg'):
                            rgb = cv2.imread(path + animal + '/' + scene + '/' + subfolder + '/' + file)
                            thermal = cv2.imread(path + animal + '/' + scene + '/' + subfolder + '/' + file.replace('RGB', 'Thermal'))
                            thermal = cv2.cvtColor(thermal, cv2.COLOR_BGR2GRAY)
                            
                            combined = cv2.merge((rgb, thermal))
                            # write in a new folder called dataset_4channels
                            if not os.path.exists('../../data/dataset_4channels/images'):
                                os.makedirs('../../data/dataset_4channels/images')
                            file = file.replace('RGB', '4channels')
                            transform = torch.from_numpy(combined)
                            torch.save(transform, '../../data/dataset_4channels/images/' + file + '.pt')

                elif subfolder == 'labels':
                    for file in os.listdir(path + animal + '/' + scene + '/' + subfolder):
                        if file.endswith('RGB.txt'):
                            with open(path + animal + '/' + scene + '/' + subfolder + '/' + file, 'r') as f:
                                lines = f.readlines()
                            #create file if exists
                            if not os.path.exists('../../data/dataset_4channels/labels'):
                                os.makedirs('../../data/dataset_4channels/labels')
                            file = file.replace('RGB', '4channels')
                            with open('../../data/dataset_4channels/labels/' + file, 'w') as f:
                                for line in lines:
                                    f.write(line)
                        else:
                            continue