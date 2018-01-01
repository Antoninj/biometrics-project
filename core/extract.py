# Author: Antonin Jousson
# coding: utf-8

# To do : add minutiae drawing on original image functionality and implement post processing function in order to remove
# false positives minutiae detected at the image borders

from skimage import img_as_uint, img_as_bool, img_as_ubyte, img_as_float, img_as_int
from skimage.io import imread, imsave
from skimage.util import invert
from skimage.draw import ellipse

import os
import numpy as np
import argparse
import json


grid = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

# Post process the feature arrays by removing false positives located at the borders
def postprocess(features, threshold):
	(x, y) = features.shape

	features[0:5] = 0
	features[x-5:x] = 0

	return features

def locate_minutiae_positions(img):

	pass

# Extract all minutiae from the input image
def extract_minutiae_positions(img):
	img_copy = img_as_float(img)
	(x, y) = img.shape
	#features_matrix = np.zeros([x,y])
	positions = {"bifurcation":[],"ending":[]}

	for i in range(1, x - 1):
		for j in range(1, y - 1):
			#features_matrix[i][j] = compute_crossing_number(img, i, j)
			minutiae_type = compute_crossing_number(img_copy, i, j)
			if minutiae_type != "none":
				positions[minutiae_type].append((i,j))
	return positions

# Compute the crossing number value for a given pixel at position (i,j)
def compute_crossing_number(img,i,j):
	# If the current pixel is part of the skeleton image
	if int(img[i][j]) == 0:
		values = [int(img[i + k][j + l]) for k, l in grid]
		crossings = (sum([abs(int(values[k]) - int(values[k + 1])) for k in range(8)]))//2
		if crossings == 1:
			return "ending"
		elif crossings == 3:
			return "bifurcation"
	return "none"

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Extract minutiae features using a preprocessed fingerprint image")
	parser.add_argument("filepath", nargs=1, help = "Input image location", type=str)
	parser.add_argument("-s","--save", action='store_true', help = "Save template as img_extracted.json")
	parser.add_argument("-d","--draw", nargs= 1, help = "Superpose minutiae on original image", type = bool, default = False)

	args = parser.parse_args()
	image = imread(args.filepath[0])
	minutiae_positions = extract_minutiae_positions(image)

	if args.save:
		base_image_name = os.path.splitext(args.filepath[0])[0]
		filename = base_image_name+"_extracted.json"
		with open(filename, 'w', encoding='utf-8') as outfile:
			json.dump(minutiae_positions, outfile,  sort_keys = True, indent = 4, ensure_ascii = False)

