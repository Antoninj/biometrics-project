# Author: Antonin Jousson
# coding: utf-8

from . import preprocess, extract

# other imports
import os
import json
from skimage.io import imread


class FingerprintMatcher(object):

	def __init__(self):

		self.db = self.get_db()
		self.templates = self.load_templates()

	def get_db(self):
		with open("config/config.json") as cfg:
			config = json.load(cfg)
		
		return config["db"]

	def load_templates(self):
		pass

	def compute_similiraty_score(self,template_features,probe_features):
		pass

	def compute_minutiae_distance(self, pos_1, pos_2):
		pass

	def parse_identity(input_file):
		pass

	def get_template(self,input_file):
		pass

	def verify_identity(self, filename, genuine_identity = True):

		input_image = imread(filename, as_grey= True)
		probe_identity = self.parse_identity(filename,genuine_identity)

		template_features = self.get_template(probe_identity)

		preprocessed_image = preprocess.apply_preprocessing(input_image)
		probe_features = extract.extract_minutiae_positions(preprocessed_image)

		similiraty_score = self.compute_similiraty_score(template_features, probe_features)
		
		return similiraty_score
