# Author: Antonin Jousson
# coding: utf-8

from skimage import img_as_uint
from skimage.io import imread, imshow, imsave
from skimage.exposure import equalize_adapthist, rescale_intensity
from skimage.filters import threshold_local, gaussian 
from skimage.morphology import thin
from skimage.util import invert

import argparse
import os

def apply_thresh(img,threshold):
	return img > threshold

def apply_preprocessing(img):

	# Intensity scaling 
	img_intensity_scale = rescale_intensity(img)

	# Adaptive histogram equalizer
	img_equalized = equalize_adapthist(img_intensity_scale)

	# Gaussian smoothing
	img_smoothed = gaussian(img_equalized)

	# Binarization with adaptive thresholding
	thresh_local = threshold_local(img_smoothed, 125, 'mean')
	img_binarized = apply_thresh(img_smoothed,thresh_local)

	# Thinning
	img_thinned = invert(thin(img_binarized))

	return img_thinned

def main():
	parser = argparse.ArgumentParser(description="Preprocess fingerprint image")
	parser.add_argument("image", nargs=1, help = "Input image filepath" , type=str)
	parser.add_argument("--save", action='store_true', help = "Save result image as img_preprocessed.png")
	args = parser.parse_args()

	image = imread(args.image[0], as_grey= True)
	preprocessed_image = apply_preprocessing(image)

	base_image_name = os.path.splitext(args.image[0])[0]
	imsave(base_image_name+"preprocessed.png", img_as_uint(preprocessed_image))


if __name__=="__main__":
	main()
