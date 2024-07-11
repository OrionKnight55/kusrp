import os
import cv2
import numpy as np
from detection import pano2stereo, realign_bbox
# Ensure that the necessary functions (pano2stereo and realign_bbox) are available in the script

# Define the directories
pano_data_dir = 'data2/image/val'        # Directory containing the panoramic images
label_data_dir = 'data2/label/val'         # Directory containing the labels (in JSON format)
output_dir = 'data2/output/img'         # Directory to save the stereographic images
output_label_dir = 'data2/output/label' # Directory to save the stereographic labels

# Create the output directories if they don't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(output_label_dir):
    os.makedirs(output_label_dir)

# Function to read label files
def read_labels(label_path):
    labels = []
    with open(label_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:
                label = {
                    'class': parts[0],
                    'center_x': float(parts[1]),
                    'center_y': float(parts[2]),
                    'width': float(parts[3]),
                    'height': float(parts[4])
                }
                labels.append(label)
    return labels

# Function to write label files
def write_labels(label_path, labels):
    with open(label_path, 'w') as file:
        for label in labels:
            file.write(f"{label['class']} {label['center_x']} {label['center_y']} {label['width']} {label['height']}\n")

# Loop through all files in the panoramic images directory
for filename in os.listdir(pano_data_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        # Process only image files
        pano_path = os.path.join(pano_data_dir, filename)
        label_path = os.path.join(label_data_dir, os.path.splitext(filename)[0] + '.txt')

        # Read the panoramic image
        pano_img = cv2.imread(pano_path)

        # Read the labels
        if os.path.exists(label_path):
            labels = read_labels(label_path)
        else:
            print(f'Label file not found for {filename}')
            continue

        if pano_img is not None:
            # Convert the panoramic image to stereographic images
            stereo_imgs = pano2stereo(pano_img)

            # Process each stereographic image and its labels
            for i, stereo_img in enumerate(stereo_imgs):
                # Adjust bounding boxes for the stereographic image
                stereo_labels = []
                for label in labels:
                    center_x = label['center_x']
                    center_y = label['center_y']
                    width = label['width']
                    height = label['height']
                    new_center_x, new_center_y, new_width, new_height = realign_bbox(center_x, center_y, width, height, i)
                    stereo_labels.append({
                        'class': label['class'],
                        'center_x': new_center_x,
                        'center_y': new_center_y,
                        'width': new_width,
                        'height': new_height
                    })

                # Save the stereographic image
                base_filename = os.path.splitext(filename)[0]
                stereo_filename = f'{base_filename}_face_{i}.jpg'
                stereo_path = os.path.join(output_dir, stereo_filename)
                cv2.imwrite(stereo_path, stereo_img)

                # Save the labels for the stereographic image
                label_filename = f'{base_filename}_face_{i}.txt'
                label_path = os.path.join(output_label_dir, label_filename)
                write_labels(label_path, stereo_labels)

                print(f'Processed and saved stereographic image and labels for {filename}, face {i}')
        else:
            print(f'Failed to read {filename}')

print('Dataset creation complete.')
