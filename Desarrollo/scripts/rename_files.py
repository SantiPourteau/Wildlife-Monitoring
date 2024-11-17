# Rename the raw dataset


# Match the RGB and Thermal images and the annotations and rename them so they have the same name for example: Cow_1_RGB.jpg, Cow_1_Thermal.jpg, Cow_1_Annotation.txt
# Create a new folder data_renamed and store the renamed images and annotations there


import os
import shutil
import re
from collections import defaultdict

path = '../data/raw_data/'

renamed_path = '../data/data_renamed/'

if not os.path.exists(renamed_path):
    os.makedirs(renamed_path)

if not os.path.exists(renamed_path + 'Cow/'):
    os.makedirs(renamed_path + 'Cow/')
if not os.path.exists(renamed_path + 'Deer/'):
    os.makedirs(renamed_path + 'Deer/')
if not os.path.exists(renamed_path + 'Horse/'):
    os.makedirs(renamed_path + 'Horse/')

# Rename the raw dataset
for folder in os.listdir(path):
    if os.path.isdir(path + folder):
        for file in os.listdir(path + folder):
            if file.endswith('R.jpg') or file.endswith('R.JPG'):
                number = file.split('_')[-1].split('.')[0]
                if number == 'R':
                    number = file.split('_')[-2].split('.')[0]
                shutil.copyfile(path + folder + '/' + file, renamed_path + folder + '/' + folder + '_' + str(int(number)) + f'_Thermal.jpg')
            elif file.endswith('.jpg') or file.endswith('.JPG'):
                number = file.split('_')[-1].split('.')[0]
                if number == 'R':
                    number = file.split('_')[-2].split('.')[0]
                shutil.copyfile(path + folder + '/' + file, renamed_path + folder + '/' + folder + '_' + str(int(number)-1) + '_RGB.jpg')
            elif file.endswith('R.txt'):
                number = file.split('_')[-2].split('.')[0]
                shutil.copyfile(path + folder + '/' + file, renamed_path + folder + '/' + folder + '_' + str(int(number)) + '_Thermal_Annotation.txt')
            elif file.endswith('.txt'):
                number = file.split('_')[-1].split('.')[0]
                if number == 'R':
                    number = file.split('_')[-2].split('.')[0]

                shutil.copyfile(path + folder + '/' + file, renamed_path + folder + '/' + folder + '_' + str(int(number)-1) + '_RGB_Annotation.txt')

for animal in ['Cow', 'Deer', 'Horse']:
    source_path = f'../data/data_renamed/{animal}'

    if not source_path.endswith(os.path.sep):
        source_path += os.path.sep

    grouped_files = defaultdict(list)

    number_pattern = re.compile(r'\d+')

    
    for file in os.listdir(source_path):
        if os.path.isfile(os.path.join(source_path, file)):
       
            match = number_pattern.search(file)
            if match:
                number = match.group()
                grouped_files[number].append(file)

    # Create subfolders and move files
    counter = 1
    for number, files in grouped_files.items():
        subfolder_name = f"Imagen_{counter}"
        subfolder_path = os.path.join(source_path, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True) 
        
        for file in files:
            old_path = os.path.join(source_path, file)
            new_path = os.path.join(subfolder_path, file)
            os.rename(old_path, new_path)  
        
        counter += 1
