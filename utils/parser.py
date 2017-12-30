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
			os.makedirs(folder)

def check_folder(folder_name):
	folders = ["template_data"]+["template_gallery"]+["test_data"]
	folders = ["data/"+ f +"/" + folder_name for f in folders]
	for folder in folders:
		if not os.path.exists(folder):
			os.makedirs(folder)

def parse_folder(folder_full_path, folder_name, split_number):
	test_data_indicators = ["_"+str(i)+"." for i in range(1,split_number)]
	for file in os.listdir(folder_full_path):
		filepath = folder_full_path+"/"+file
		extension = os.path.splitext(file)[1]

		if any(indicator in file for indicator in test_data_indicators):
			dest_dict = "data/test_data/"+folder_name
			if extension != ".txt":
				shutil.copy(filepath,dest_dict)
		else:
			dest_dict = "data/template_data/"+folder_name
			if extension != ".txt":
				shutil.copy(filepath,dest_dict)

def parse_data(split_number=4):
	raw_data_folder = "data/raw_data"
	
	print("Checking folders... ")
	for folder_name in os.listdir(raw_data_folder):
		if folder_name != ".DS_Store":
			check_folder(folder_name)

	print("Parsing data...")
	for folder_name in os.listdir(raw_data_folder):
		if folder_name != ".DS_Store":
			folder_full_path = raw_data_folder +"/"+folder_name
			parse_folder(folder_full_path,folder_name,split_number)

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Parse raw data")
	parser.add_argument("-s","--split", nargs=1, help = "Number of files kept for testing (out of 7) for each person" \
	, type=int, default = 4 , choices = (1,2,3,4,5,6,7))
	
	args = parser.parse_args()
	split_number =  args.split

	parse_data(split_number)

