# Author: Antonin Jousson
# coding: utf-8

# package level imports
from .parser import parse_data
from core import preprocess, extract

# other imports
import os
import json

from skimage import img_as_uint
from skimage.io import imread, imsave

def load_images(path):
	images = [imread(path + "/" + img, as_grey= True ) for img in os.listdir(path)]
	return images

def save_template(path, templates):
	for feature_template in templates:
		base_image_name = os.path.splitext(feature_template)[0]
		filename = path+"/"+base_image_name+"_template.json"
		with open(filename, 'w', encoding='utf-8') as outfile:
			json.dump(minutiae_positions, outfile,  sort_keys = True, indent = 4, ensure_ascii = False)

def preprocess_batch_images(images):
	return [preprocess.apply_preprocessing(img) for img in images]

def extract_minutiae_batch(preprocessed_images):
	return [extract.extract_minutiae_positions(img) for img in preprocessed_images]

def build_gallery():
	template_data_path = "data/template_data/"

	if not os.path.exists(template_data_path):
		parse_data()

	for folder in os.listdir(template_data_path):
		if folder != ".DS_Store":
			print("Loading template images...")
			folder_path = template_data_path + folder
			images = load_images(folder_path)

			print("Preprocessing template images...")
			preprocessed_images = preprocess_batch_images(images)

			print("Extracting features from preprocessed template images...")
			extracted_features = extract_minutiae_batch(preprocessed_images)

			gallery_path = "data/template_gallery/"+folder
			save_template(gallery_path, extracted_features)
	
	print("Template features gallery successfully created !")

if __name__=="__main__":
	build_gallery()

