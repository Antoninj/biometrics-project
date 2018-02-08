# Author: Antonin Jousson
# coding: utf-8

# To do:
# - Improve person identity parsing with regex of filename

# internal imports
import preprocess, extract

# external imports
import os
import json
import argparse
import math

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
		score = (1-closeness)**(0.01)
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

		s = min(len(flatten_template_features),len(flatten_probe_features))

		flatten_features_zipped = zip(flatten_template_features[0:s],flatten_probe_features[0:s])
		#print(template_core_position,probe_core_position)

		degree_of_closeness = 0
		for features in flatten_features_zipped:
			feature_distance_template = self.compute_minutiae_core_distance(features[0],template_core_position)
			feature_distance_probe = self.compute_minutiae_core_distance(features[1],probe_core_position)

		degree_of_closeness += (abs(feature_distance_template-feature_distance_probe))/(feature_distance_probe)

		return degree_of_closeness

	@staticmethod
	def parse_identity(input_file, genuine_identity):
		return int(input_file[0]) if input_file[1]=="_" else int(input_file[0:2])

	def get_template(self,probe_identity):
		return self.templates[probe_identity]

	def verify_identity(self, filename, genuine_identity = True):
		# Load probe image
		input_image = imread(filename, as_grey= True)

		# Parse probe identity
		probe_identity = self.parse_identity(filename, genuine_identity)
		# Retrieve probe associated template
		template_features = self.get_template(probe_identity)

		# Peprocess probe image
		preprocessed_image = preprocess.apply_preprocessing(input_image)
		#preprocessed_image = img_as_uint(preprocessed_image)

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

	args = parser.parse_args()

	matcher = FingerprintMatcher()
	score = matcher.verify_identity(args.filepath[0])

	print(score)
