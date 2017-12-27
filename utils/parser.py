# Author: Antonin Jousson
# coding: utf-8

import shutil
import os

def check_folders():
	folders = ["template_data"]*4 + ["template_gallery"]*4+["test_data"]*4
	folders = ["data/"+ f for f in folders]
	sub_folders = ["png","bmp","tif1","tif2"]*4
	folders = [folders[i] + "/" +sub_folders[i] for i in range(len(folders))]

	for folder in folders:
		if not os.path.exists(folder):
			print("Creating " + folder + " folder...")
			os.makedirs(folder)

def parse_folder(folder):
	test_data_indicators = ["_"+str(i) for i in range(1,5)]
	for file in os.listdir(folder):
		base_image_name = os.path.splitext(file)[0]
		ext = os.path.splitext(file)[1]
		filepath = folder+"/"+file
		if any(indicator in base_image_name for indicator in test_data_indicators):
			dest_dict = "data/test_data/"+folder
			shutil.copy(filepath,dest_dict)
		else:
			dest_dict = "data/template_data/"+folder
			shutil.copy(filepath,dest_dict)

def parse_data():
	raw_data_folder = "data/raw_data"

	print("Checking folders... ")
	check_folders()
	print("Folders ok")
	print("Parsing data...")
	for folders in os.listdir(raw_data_folder):
		if folders != ".DS_Store":
			folder = raw_data_folder +"/"+folders
			parse_folder(folder)
	print("Data succesfully parsed !")

if __name__=="__main__":
	parse_data()
