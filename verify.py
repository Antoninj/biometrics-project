# Author: Antonin Jousson
# coding: utf-8

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

def compute_scores(matcher, filepaths, threshold, genuine  ):
	scores = [matcher.verify_identity(path, genuine) for path in filepaths]
	return scores

def run_simulation(matcher, threshold, genuine):
	input_filepaths = parse_input_files()
	raw_scores = compute_scores(matcher, input_filepaths, threshold, genuine)
	raw_scores = [round(score,3) for score in raw_scores]
	match_scores = [1 if raw_score >= threshold else 0 for raw_score in raw_scores]

	results = {"scores":raw_scores, "match":match_scores}
	results = pandas.DataFrame(data = results)
	return results

def compute_FNMR(results):
    FNMR = 100- (float(results.match.sum())/(len(results.match)))*100
    return FNMR

def compute_FMR(results):
    FMR = (float(results.match.sum())/(len(results.match)))*100
    return FMR

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = "Script to test the fingerprint recognition system in verification mode")

	parser.add_argument("-t", "--threshold", help = "Matching threshold", type = float, default = 0.55)
	parser.add_argument("-s", "--save", help = "Save performance metrics", action='store_true')
	parser.add_argument("-i", "--imposter", help = "Input image is genuine or not", action = "store_false", default = True)

	args = parser.parse_args()
	thresh = args.threshold
	identity_bool = args.imposter

	print("Creating fingerprint matcher...")
	print("Loading template gallery...")
	matcher = match.FingerprintMatcher()
	print("Matching fingerprints...")
	verification_results = run_simulation(matcher, thresh, identity_bool)
	print("Matching done !")

	print("Computing performance metrics...")

	if identity_bool:
		identity = "genuine"
		FNMR = compute_FNMR(verification_results)
		print("FNMR: {}".format(FNMR))
	else:
		identity = "fraud"
		FMR = compute_FMR(verification_results)
		print("FMR: {}".format(FMR))

	if args.save:
		print("Saving results ...")
		output_file = "results/results_{}_{}.csv".format(identity,thresh)
		verification_results.to_csv(output_file, sep='\t', encoding='utf-8')

