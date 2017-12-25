# Author: Antonin Jousson
# coding: utf-8

#internal imports
import preprocess
import extract

# external imports
import os
import json
import regex 

from skimage import img_as_uint
from skimage.io import imread, imshow, imsave

import argparse

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
	return [extract.extract_minutiae(img) for img in preprocessed_images]

def __main__():
	parser = argparse.ArgumentParser(description="Create template gallery from fingerprint images")
	parser.add_argument("-f","--folder", nargs=1, help = "Input folder location" , type=str)
	args = parser.parse_args()

	data_path = args.folder
	gallery_path = "data/template_gallery/"

	print("Loading images... \n")
	images = load_images(data_path)

	print("Preprocessing images...\n")
	preprocessed_images = preprocess_batch_images(images)

	print("Extracting features... \n")
	extracted_features = extract_minutiae_batch(preprocessed_images)

	save_images(gallery_path, extracted_features)
	print("Template gallery created !")

if __name__=="__main__":
	main()

