# Author: Antonin Jousson
# coding: utf-8

from skimage.io import imread, imsave
from core import match
import argparse
import json
import os
import pandas

def load_config():
	with open("config/config.json") as cfg:
		config = json.load(cfg)
	return config

def parse_input_files():
	config = load_config()
	db = config["db"]
	path = "data/test_data/{}".format(db)
	return [path+"/"+filename for filename in os.listdir(path)]

def compute_scores(matcher, filepaths, threshold ):
	scores = [matcher.verify_identity(path, True) for path in filepaths]
	return scores

def run_simulation(matcher, threshold):
	input_filepaths = parse_input_files()
	raw_scores = compute_scores(matcher, input_filepaths, threshold)
	raw_scores = [round(score,3) for score in raw_scores]
	match_scores = [1 if raw_score >= threshold else 0 for raw_score in raw_scores]

	results = {"scores":raw_scores, "match":match_scores}
	results = pandas.DataFrame(data = results)
	return results

def compute_FNMR(results):
    FNMR = 100- (float(results.match.sum())/(len(results.match)))*100
    return FNMR

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = "Script to test the fingerprint recognition system in verification mode")

	parser.add_argument("-t", "--threshold", help = "Matching threshold", type = int, default = 0.55)
	parser.add_argument("-s","--save", help = "Save performance metrics", action='store_true')
	parser.add_argument("-i","--imposter", help = "Input image is genuine or not", action = "store_false", default = True)

	args = parser.parse_args()
	thresh = args.threshold

	print("Creating fingerprint matcher...")
	matcher = match.FingerprintMatcher()
	print("Loading template gallery...")
	print("Matching fingerprints...")
	verification_results = run_simulation(matcher, thresh)
	print("Matching done !")

	print("Computing performance metrics...")
	FNMR = compute_FNMR(verification_results)

	print("FNMR: {}".format(FNMR))

	if args.imposter:
		genuine = "genuine"
	else:
		genuine = "fraud"

	if args.save:
		print("Saving results ...")
		output_file = "results/results_{}_{}.csv".format(genuine,thresh)
		verification_results.to_csv(output_file, sep='\t', encoding='utf-8')

