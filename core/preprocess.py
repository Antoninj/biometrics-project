# Author: Antonin Jousson
# coding: utf-8

from skimage import img_as_uint
from skimage.io import imread, imsave
from skimage.exposure import equalize_adapthist, rescale_intensity
from skimage.filters import threshold_local, gaussian
from skimage.filters.rank import enhance_contrast
from skimage.morphology import thin, disk
from skimage.util import invert

import argparse
import os

def apply_thresh(img, threshold):
	return img > threshold

def apply_preprocessing(img):
	# Intensity scaling
	img_intensity_scale = rescale_intensity(img, in_range= "dtype")

	# Contrast enhancing
	img_enhanced_contrast = enhance_contrast(img_intensity_scale, disk(5))

	# Adaptive histogram equalizer
	img_equalized = equalize_adapthist(img_enhanced_contrast)

	# Gaussian smoothing
	img_smoothed = gaussian(img_equalized)

	# Binarization with adaptive thresholding
	thresh_local = threshold_local(img_smoothed, 125, 'mean')
	img_binarized = apply_thresh(img_smoothed,thresh_local)

	# Thinning
	img_thinned = thin(invert(img_binarized))

	return img_thinned

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Preprocess fingerprint image")
	parser.add_argument("filepath", nargs=1, help = "Input image location" , type=str)
	parser.add_argument("-s","--save", action='store_true', help = "Save result image as filename_preprocessed.png")

	args = parser.parse_args()
	image = imread(args.filepath[0], as_grey= True)

	print("Preprocessing image...")
	preprocessed_image = apply_preprocessing(image)

	if args.save:
		print("Saving results...")
		base_image_name = os.path.splitext(args.filepath[0])[0]
		imsave(base_image_name+"_preprocessed.png", img_as_uint(preprocessed_image))
