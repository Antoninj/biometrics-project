# Author: Antonin Jousson
# coding: utf-8

# To do :
# implement false positives minutiae removal algorithm
# singular core point extraction using poincare index

from skimage import img_as_uint, img_as_bool, img_as_ubyte, img_as_float, img_as_int
from skimage.io import imread, imsave
from skimage.util import invert

import poincare
import utils

from PIL import Image
import os
import numpy as np
import argparse
import json

import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

grid = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

# False positives removal algorithm
def postprocess(features):
	(x, y) = features.shape

	# To do ...

	return features

# Extract all minutiae from the input image
def extract_minutiae_positions(img):
	img_copy = img_as_float(img)
	(x, y) = img.shape
	positions = {"bifurcation":[],"ending":[]}

	for i in range(1, x - 1):
		for j in range(1, y - 1):
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

# singular core point extraction using poincare index algorithm
def extract_core_point_position(img, block_size, tolerance):
	im = Image.fromarray(np.array(img_as_ubyte(img)))
	im = im.convert("L")

	f = lambda x, y: 2 * x * y
	g = lambda x, y: x ** 2 - y ** 2

	angles = utils.calculate_angles(im, block_size, f, g)
	angles = utils.smooth_angles(angles)

	singularities_positions = poincare.calculate_singularities(im, angles, tolerance, block_size)

	return singularities_positions


def combine_spatial_features(minutiae_positions,singular_point_position):
	minutiae_positions["singular point"] = (singular_point_position)

	return minutiae_positions

def extract_spatial_features_positions(img, block_size, tolerance):
	minutiae_positions = extract_minutiae_positions(img)
	singular_point_position = extract_core_point_position(img, block_size, tolerance)
	spatial_features = combine_spatial_features(minutiae_positions, singular_point_position)

	return spatial_features

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Extract minutiae features and core point using a preprocessed fingerprint image")
	parser.add_argument("filepath", nargs=1, help = "Input image location", type=str)
	parser.add_argument("-s","--save", action='store_true', help = "Save template as img_extracted.json")

	args = parser.parse_args()
	image = imread(args.filepath[0])
	#minutiae_positions = extract_minutiae_positions(image)

	spatial_features_positions = extract_spatial_features_positions(image, block_size = 16, tolerance = 1)

	if args.save:
		base_image_name = os.path.splitext(args.filepath[0])[0]
		filename = base_image_name+"_extracted.json"
		with open(filename, 'w') as outfile:
			json.dump(minutiae_positions, outfile,  sort_keys = True, indent = 4, ensure_ascii = False)

