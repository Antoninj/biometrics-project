# Author: Antonin Jousson
# coding: utf-8

# To do:
# - Fix degree of closeness scoring function

# internal imports
import preprocess, extract

# external imports
import os
import json
import argparse
import math
import re

from skimage.io import imread
from skimage import img_as_uint

class FingerprintMatcher(object):

	def __init__(self):
		self.config = self.load_config()
		self.templates = self.load_templates()

	@staticmethod
	def load_config():
		with open("config/config.json") as cfg:
			config = json.load(cfg)
		return config

	def load_templates(self):
		db = self.config["db"]
		path = "data/template_gallery/{}".format(db)
		templates = {}
		for file in os.listdir(path):
			file_identity = self.parse_identity(file,True)
			templates[file_identity] = json.loads(open(path+"/"+file).read())
		return templates

	def compute_matching_score(self,template_features, probe_features):
		closeness = self.compute_degree_of_closeness(template_features, probe_features)
		score = 1-(closeness)
		return score

	@staticmethod
	def compute_minutiae_core_distance(minutiae_position, core_position):
		return math.sqrt((minutiae_position[0]-core_position[0])**2 + (minutiae_position[1]-core_position[1])**2)

	def compute_degree_of_closeness(self, template_features, probe_features):
		keys = ["bifurcation","ending"]

		template_core_position = template_features["core point"]
		probe_core_position = probe_features["core point"]

		flatten_template_features = template_features[keys[0]] + template_features[keys[1]]
		flatten_probe_features = probe_features[keys[0]] + probe_features[keys[1]]

		s = min(len(flatten_template_features), len(flatten_probe_features))
		flatten_features_zipped = zip(flatten_template_features[0:s],flatten_probe_features[0:s])

		degree_of_closeness = 0
		#total = 0
		for features in flatten_features_zipped:
			feature_distance_template = self.compute_minutiae_core_distance(features[0],template_core_position)
			feature_distance_probe = self.compute_minutiae_core_distance(features[1],probe_core_position)
			#total += feature_distance_probe + feature_distance_template
			temp = (abs(feature_distance_template-feature_distance_probe))
			degree_of_closeness += temp

		total = sum([self.compute_minutiae_core_distance(features,probe_core_position) for features in flatten_probe_features])
		return degree_of_closeness/total

	@staticmethod
	def parse_identity(input_file, genuine_identity):
		pattern = re.compile("[0-9]+_")
		match = pattern.search(input_file)
		true_identity = int(input_file[match.start():match.end()-1])
		if genuine_identity:
			return true_identity
		else:
			return true_identity + 1

	def get_template(self,probe_identity):
		return self.templates[probe_identity]

	def verify_identity(self, filename, genuine_identity = True):
		# Load probe image
		input_image = imread(filename, as_grey= True)

		# Parse probe identity
		probe_identity = self.parse_identity(filename, genuine_identity)

		# Retrieve probe corresponding template
		template_features = self.get_template(probe_identity)

		# Peprocess probe image
		preprocessed_image = preprocess.apply_preprocessing(input_image)

		block_size = self.config["block_size"]
		tolerance = self.config["tolerance"]

		# Extract probe spatial features
		probe_features = extract.extract_spatial_features_positions(preprocessed_image, block_size , tolerance)

		# Compute matching score
		similiraty_score = self.compute_matching_score(template_features, probe_features)

		return similiraty_score

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = "Match two fingerprint images")
	parser.add_argument("filepath", nargs = 1, help = "Input image location", type = str)
	parser.add_argument("-i","--imposter", help = "Input image is genuine or not", action = "store_false", default = True)

	args = parser.parse_args()
	genuine_identity = args.imposter
	matcher = FingerprintMatcher()
	score = matcher.verify_identity(args.filepath[0], genuine_identity)

	print(score)
