import os
import random
import shutil

def copy_random_images_and_xmls(image_source_dir, xml_source_dir, target_dir, num_images):
    # Image source directory should exist
    if not os.path.exists(image_source_dir):
        print(f"Image source directory {image_source_dir} does not exist.")
        return

    # XML source directory should exist
    if not os.path.exists(xml_source_dir):
        print(f"XML source directory {xml_source_dir} does not exist.")
        return
    
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Get list of all image files in the source directory
    image_files = [file for file in os.listdir(image_source_dir) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif'))]
    
    # Check if there are enough images in the source directory
    if len(image_files) < num_images:
        print(f"Not enough images in the source directory. Found {len(image_files)} images.")
        return
    
    # Randomly select num_images from the list
    selected_images = random.sample(image_files, num_images)
    
    # Copy selected images and corresponding XML files to the target directory
    for image in selected_images:
        src_image_path = os.path.join(image_source_dir, image)
        dst_image_path = os.path.join(target_dir, image)
        shutil.copy(src_image_path, dst_image_path)
        
        # Check and copy corresponding XML file
        xml_file = os.path.splitext(image)[0] + '.txt'
        src_xml_path = os.path.join(xml_source_dir, xml_file)
        if os.path.exists(src_xml_path):
            dst_xml_path = os.path.join(target_dir, xml_file)
            shutil.copy(src_xml_path, dst_xml_path)
    
    print(f"Copied {num_images} images and their corresponding XML files from {image_source_dir} and {xml_source_dir} to {target_dir}.")

# Example usage
image_source_directory = 'images'  # Change this to your image source directory path
xml_source_directory = 'label/label'      # Change this to your XML source directory path
target_directory = 'labels'              # Change this to your target directory path
number_of_images_to_copy = 700

copy_random_images_and_xmls(image_source_directory, xml_source_directory, target_directory, number_of_images_to_copy)
