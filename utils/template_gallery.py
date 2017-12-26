# Author: Antonin Jousson
# coding: utf-8

# package level imports
from .core import preprocess, extract
from .utils.parser import parse_data

# other imports
import os
import json

from skimage import img_as_uint
from skimage.io import imread, imsave

def load_images(path):
	images = [imread(img, as_grey= True ) for img in os.listdir(path)]
	return images

def save_images(path, images):
	for img in images:
		base_image_name = os.path.splitext(img)[0]
		imsave(path + base_image_name +"_template.png", img_as_uint(img))

def preprocess_batch_images(images)
	return [preprocess.apply_preprocessing(img) for img in images]

def extract_minutiae_batch(images):
	return [extract.extract_all_minutiae(img) for img in preprocessed_images]

def main():
	template_data_path = "data/template_data/"
	gallery_path = "data/template_gallery/"

	if not os.path.exists(template_data_path):
		parse_data()

	print("Loading template images...")
	images = load_images(template_data_path)

	print("Preprocessing template images...")
	preprocessed_images = preprocess_batch_images(images)

	print("Extracting features from preprocessed template images...")
	extracted_features = extract_minutiae_batch(preprocessed_images)

	save_images(gallery_path, extracted_features)
	print("Template features gallery successfully created !")

if __name__=="__main__":
	main()

