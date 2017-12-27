# Author: Antonin Jousson
# coding: utf-8

# To do : improve crossing number algorithm and implement post processing function in order to remove
# false positives minutiae detected at the image borders
import os
import numpy as np
import argparse

from skimage import img_as_uint, img_as_bool, img_as_ubyte, img_as_float, img_as_int
from skimage.io import imread, imsave
from skimage.util import invert

grid = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

# Post process the feature arrays by removing false positives located at the borders
def postprocess(features, threshold):
	(x, y) = features.shape

	features[0:5] = 0
	features[x-5:x] = 0

	return features

def locate_all_minutiae(img):

	pass

# Extract all minutiae from the input image
def extract_all_minutiae(img):
	#img = img.astype(np.uint8)
	(x, y) = img.shape
	features_matrix = np.zeros([x,y])
	for i in range(1, x - 1):
		for j in range(1, y - 1):
			features_matrix[i][j] = compute_crossing_number(img, i, j)
	#clean_features_matrix = postprocess(features_matrix,5)
	return features_matrix

# Compute the crossing number value for a given pixel at position (i,j)
def compute_crossing_number(img,i,j):
	# If the current pixel is part of the skeleton image
	if int(img[i][j]) == 0:
		values = [int(img[i + k][j + l]) for k, l in grid]
		crossings = (sum([abs(int(values[k]) - int(values[k + 1])) for k in range(8)]))//2
		return crossings if crossings == 1 else int(0)
	else:
		return int(0)

def main():
	parser = argparse.ArgumentParser(description="Extract minutiae features using a preprocessed fingerprint image")
	parser.add_argument("filepath", nargs=1, help = "Input image location" , type=str)
	parser.add_argument("-s","--save", action='store_true', help = "Save template as img_extracted.csv")
	#parser.add_argument("-d","--dest", action='store_true', help = "Saved image destination folder", default = cwd())

	args = parser.parse_args()
	image = imread(args.filepath[0])
	image = img_as_float(image)
	features_matrix = invert(extract_all_minutiae(image))
	if args.save:
		base_image_name = os.path.splitext(args.filepath[0])[0]
		filename = base_image_name+"_extracted.csv"
		#np.savetxt(filename, features_matrix, delimiter=",")
		imsave(base_image_name+"_extracted.png", img_as_uint(features_matrix))

if __name__=="__main__":
	main()

