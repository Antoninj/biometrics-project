# Author: Antonin Jousson
# coding: utf-8

# package level imports
from utils.parser import parse_data
from core import preprocess, extract

# other imports
import os
import json
from skimage.io import imread

# To do : add tqdm module in order to track progress of the script during gallery creation

def load_images(path):
	images_data = []
	images_names = []
	for img in os.listdir(path):
		if not img.startswith('.'):
			images_data.append(imread(path + "/" + img, as_grey= True))
			images_names.append(os.path.splitext(img)[0])

	return images_data,images_names

def save_templates(path, templates, image_names):
	for i,feature_template in enumerate(templates):
		base_image_name = os.path.splitext(image_names[i])[0]
		filename = path+"/"+base_image_name+"_template.json"
		with open(filename, 'w', encoding='utf-8') as outfile:
			json.dump(feature_template, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

def preprocess_batch_images(images):
	return [preprocess.apply_preprocessing(img) for img in images]

def extract_minutiae_batch(preprocessed_images):
	return [extract.extract_minutiae_positions(img) for img in preprocessed_images]

def build_gallery(split_number):
	template_data_path = "data/template_data/"
	gallery_data_path = "data/template_gallery/"

	if not os.path.exists(template_data_path):
		parse_data(split_number)

	for folder in os.listdir(template_data_path):
		if not folder.startswith('.'):
			template_folder_path = template_data_path + folder

			print("Loading template images from {} folder".format(folder))
			images,image_names = load_images(template_folder_path)

			print("Preprocessing template images...")
			preprocessed_images = preprocess_batch_images(images)

			print("Extracting features from preprocessed template images...")
			extracted_features = extract_minutiae_batch(preprocessed_images)

			gallery_folder_path = gallery_data_path + folder
			save_templates(gallery_folder_path, extracted_features, image_names)

	print("Features template gallery successfully created !")

if __name__ == "__main__":

	# Load configuration file
	with open("config/config.json") as cfg:
		config = json.load(cfg)
		
	split = config['split_number']
	build_gallery(split)

