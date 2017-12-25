# Author: Antonin Jousson
# coding: utf-8

import os
import numpy as np

from skimage import img_as_uint
from skimage.io import imread, imsave
from skimage.util import invert

import argparse

# To do : implement crossing number algorithm and post processing function(false positives minutiae detectedd at the image borders)

grid = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

def postprocess(features):

	pass

def extract_all_minutiae(img):

	img = img.astype(np.uint8)
	(x, y) = img.shape
	minutiae_template = np.empty([x,y])
	for i in range(1, x - 1):
        for j in range(1, y - 1):
            minutiae_type = compute_crossing_number(img, i, j)
            if minutiae_type != 0:
            	minutiae_template[i][j] = minutiae_type

	return minutiae_template

def compute_crossing_number(img,i,j):
	#minutiae_types = ["ending","none","bifurcation"]
	#minutiae_mapping = {i+1:minutiae_types[i] for i in range (3)}

	# If the current pixel is part of the skeleton image
	if img[i][j] == 1:
		values = [pixels[i + k][j + l] for k, l in grid]
		crossings = (sum([abs(values[k] - values[k + 1]) for k in range(8)]))/2
		if crossings in (1,3):
			return crossings
	else:
		return 0

def main():
	parser = argparse.ArgumentParser(description="Extract minutiae features from preprocessed fingerprint image")
	parser.add_argument("-i","--image", nargs=1, help = "Input image location" , type=str)
	parser.add_argument("--save", action='store_true', help = "Save result image as img_extracted.png")
	args = parser.parse_args()

	image = imread(args.image[0], as_grey= True)
	minutiae_features = extract_all_minutiae(image)

	if args.save:
		base_image_name = os.path.splitext(args.image[0])[0]
		imsave(base_image_name+"extracted.png", img_as_uint(preprocessed_image))

if __name__=="__main__":
	main()

