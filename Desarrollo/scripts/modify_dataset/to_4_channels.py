# Combines the original RGB image and Thermal image into a single image with 4 channels. The first 3 channels are the RGB image and the 4th channel is the thermal image.

import os
import cv2
import numpy as np
import torch 

path = '../../data_yolo/data_renamed/'
#create folder if not exists
new_file_type = "png"
# new_file_type = "pt"
# new_file_type = "npy"
new_path = '../../data_yolo/dataset_4channels_'+new_file_type
if not os.path.exists(new_path):
    os.makedirs(new_path)
    
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
                            if not os.path.exists(new_path + '/images'):
                                os.makedirs(new_path + '/images')
                            file = file.replace('RGB', '4channels')
                            if new_file_type == "pt":
                                transform = torch.from_numpy(combined)
                                torch.save(transform, new_path + '/images/' + file)
                            elif new_file_type == "png":
                                #save as a png with 4 channels imwrite
                                png_image = cv2.imwrite(new_path + '/images/' + file.replace('jpg', 'png'), combined)
                                # png_image = cv2.imwrite(new_path + '/images/' + file, combined)
                            elif new_file_type == "npy":
                                np.save(new_path + '/images/' + file, combined)
                            else:
                                print("Invalid file type")

                                

                elif subfolder == 'labels':
                    for file in os.listdir(path + animal + '/' + scene + '/' + subfolder):
                        if file.endswith('RGB.txt'):
                            with open(path + animal + '/' + scene + '/' + subfolder + '/' + file, 'r') as f:
                                lines = f.readlines()
                            #create file if exists
                            if not os.path.exists(new_path + '/labels'):
                                os.makedirs(new_path + '/labels')
                            file = file.replace('RGB', '4channels')
                            with open(new_path + '/labels/' + file, 'w') as f:
                                for line in lines:
                                    f.write(line)
                        else:
                            continue