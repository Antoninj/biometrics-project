# Author: Antonin Jousson
# coding: utf-8

from core import match
import argparse
import json
import os


def load_config():
	with open("config/config.json") as cfg:
		config = json.load(cfg)
	return config

def parse_input_files():
	config = load_config()
	db = config["db"]
	path = "data/test_data/{}".format(db)
	return [path+"/"+filename for filename in os.listdir(path)]

def verify_all(matcher, filepaths, threshold ):

	scores = [matcher.verify_identity(path, True) for path in filepaths]

	return scores

def run_simulation(matcher, threshold):

	input_filepaths = parse_input_files()
	results = verify_all(matcher, input_filepaths, threshold)
	return results

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = "Script to test the fingerprint recognition system in verification mode")

	parser.add_argument("-t", "--threshold", help = "Matching threshold", type = int, default = 0.7)
	parser.add_argument("-s","--save", help = "Save performance metrics", action='store_true')

	args = parser.parse_args()
	thresh = args.threshold

	matcher = match.FingerprintMatcher()
	verification_results = run_simulation(matcher, thresh)

	print(verification_results)

	if args.save:
		pass

